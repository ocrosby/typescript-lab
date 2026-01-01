#!/usr/bin/env python3
"""ts_project.py

A Click-based CLI to:
1) scaffold a TypeScript project (npm init, deps, tsconfig, etc.)
2) manage package.json scripts (clear / add)

This replaces:
- scripts-manager.js
- create-ts-project.sh

Design goals:
- SOLID / DRY / CLEAN
- All functions/methods kept small with cyclomatic complexity < 7
- Consistent module and function docstrings

Usage (via uv):
  uv run tsproj create my-project
  uv run tsproj scripts clear --project-dir my-project
  uv run tsproj scripts add dev "ts-node src/index.ts" --project-dir my-project
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import click


# -----------------------------
# Errors
# -----------------------------


class TsProjError(RuntimeError):
    """Base error for tsproj CLI failures."""


class CommandError(TsProjError):
    """Raised when an external command fails."""


class PackageJsonError(TsProjError):
    """Raised when package.json is missing or invalid."""


# -----------------------------
# Constants / Templates
# -----------------------------


GITIGNORE_CONTENT = """\
node_modules/
dist/
"""

TSCONFIG_CONTENT = """\
{
  // Visit https://aka.ms/tsconfig to read more about this file
  "compilerOptions": {
    // File Layout
    "rootDir": "./src",
    "outDir": "./dist",

    // Environment Settings
    // See also https://aka.ms/tsconfig/module
    "module": "nodenext",
    "target": "esnext",

    // For nodejs:
    "lib": ["esnext"],
    "types": ["node"],
    // and npm install -D @types/node

    // Other Outputs
    "sourceMap": true,
    "declaration": true,
    "declarationMap": true,

    // Stricter Typechecking Options
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    // Recommended Options
    "strict": true,
    "jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noUncheckedSideEffectImports": true,
    "moduleDetection": "force",
    "skipLibCheck": true
  }
}
"""

DEFAULT_INDEX_TS = 'console.log("demo");\n'

DEFAULT_SCRIPTS: Dict[str, str] = {
    "dev": "ts-node src/index.ts",
    "build": "tsc",
    "typecheck": "tsc --noEmit",
    "start": "node dist/index.js",
}

DEFAULT_DEV_DEPS = ["typescript", "ts-node", "@types/node"]


# -----------------------------
# Core services
# -----------------------------


@dataclass(frozen=True)
class CommandRunner:
    """Runs external commands with consistent error handling."""

    def run(self, args: list[str], cwd: Path) -> None:
        """Run a command in a given working directory.

        Args:
            args: Command and arguments (e.g. ["npm", "init", "-y"]).
            cwd: Working directory.

        Raises:
            CommandError: If the command returns non-zero exit status.
        """
        try:
            subprocess.run(args, cwd=str(cwd), check=True)
        except subprocess.CalledProcessError as exc:
            raise CommandError(f"Command failed: {' '.join(args)}") from exc


@dataclass(frozen=True)
class FileWriter:
    """Writes common project files safely."""

    def write_text(self, path: Path, content: str) -> None:
        """Write a UTF-8 text file, creating parents as needed.

        Args:
            path: File path.
            content: Text content.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@dataclass(frozen=True)
class PackageJsonManager:
    """Reads and updates package.json."""

    def load(self, project_dir: Path) -> Dict[str, Any]:
        """Load package.json from a directory.

        Args:
            project_dir: Directory containing package.json.

        Returns:
            Parsed JSON object.

        Raises:
            PackageJsonError: If missing or invalid JSON.
        """
        pkg_path = self._get_package_json_path(project_dir)
        return self._parse_package_json(pkg_path)

    def save(self, project_dir: Path, pkg: Dict[str, Any]) -> None:
        """Save package.json to a directory.

        Args:
            project_dir: Directory containing package.json.
            pkg: JSON dict to write.
        """
        pkg_path = self._get_package_json_path(project_dir)
        pkg_path.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")

    def clear_scripts(self, project_dir: Path) -> None:
        """Remove all scripts from package.json.

        Args:
            project_dir: Directory containing package.json.
        """
        pkg = self.load(project_dir)
        pkg["scripts"] = {}
        self.save(project_dir, pkg)

    def add_script(self, project_dir: Path, name: str, command: str) -> None:
        """Add or overwrite a script entry in package.json.

        Args:
            project_dir: Directory containing package.json.
            name: Script name.
            command: Script command.
        """
        pkg = self.load(project_dir)
        scripts = self._ensure_scripts(pkg)
        scripts[name] = command
        pkg["scripts"] = scripts
        self.save(project_dir, pkg)

    def _get_package_json_path(self, project_dir: Path) -> Path:
        """Return the path to package.json, raising if missing.

        Args:
            project_dir: Directory expected to contain package.json.

        Returns:
            Path to package.json.

        Raises:
            PackageJsonError: If package.json is missing.
        """
        pkg_path = project_dir / "package.json"
        if not pkg_path.exists():
            raise PackageJsonError(f"package.json not found in: {project_dir}")
        return pkg_path

    def _parse_package_json(self, pkg_path: Path) -> Dict[str, Any]:
        """Parse package.json and return the dict.

        Args:
            pkg_path: Path to package.json.

        Returns:
            Parsed JSON dict.

        Raises:
            PackageJsonError: If package.json is invalid JSON.
        """
        try:
            return json.loads(pkg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PackageJsonError("package.json is not valid JSON") from exc

    def _ensure_scripts(self, pkg: Dict[str, Any]) -> Dict[str, str]:
        """Return the scripts object, ensuring it exists.

        Args:
            pkg: Parsed package.json dict.

        Returns:
            scripts dict.
        """
        scripts = pkg.get("scripts")
        if scripts is None:
            return {}
        if isinstance(scripts, dict):
            return scripts  # type: ignore[return-value]
        return {}


@dataclass(frozen=True)
class TsProjectScaffolder:
    """Coordinates creation of a TypeScript project."""

    runner: CommandRunner
    files: FileWriter
    pkgjson: PackageJsonManager

    def create_project(self, project_dir: Path, force: bool = False) -> None:
        """Create a new TypeScript project scaffold.

        Args:
            project_dir: Directory to create the project in.
            force: If True, allow existing directory path (directory must exist and be a dir).

        Raises:
            TsProjError: If directory state is invalid or commands fail.
        """
        self._ensure_project_dir(project_dir, force)
        self._initialize_npm(project_dir)
        self._install_dev_dependencies(project_dir)
        self._write_project_files(project_dir)
        self._configure_npm_scripts(project_dir)

    def _ensure_project_dir(self, project_dir: Path, force: bool) -> None:
        """Ensure the project directory can be used.

        Args:
            project_dir: Target directory.
            force: Whether existing directory is allowed.
        """
        self._validate_project_dir(project_dir, force)
        self._create_project_dir_if_missing(project_dir)

    def _validate_project_dir(self, project_dir: Path, force: bool) -> None:
        """Validate directory state.

        Args:
            project_dir: Target directory.
            force: Whether existing directory is allowed.

        Raises:
            TsProjError: If directory exists and force is false, or path exists but isn't a dir.
        """
        if project_dir.exists() and not force:
            raise TsProjError(
                f"Directory already exists: {project_dir}. Use --force to reuse."
            )
        if project_dir.exists() and not project_dir.is_dir():
            raise TsProjError(f"Path exists and is not a directory: {project_dir}")

    def _create_project_dir_if_missing(self, project_dir: Path) -> None:
        """Create directory if it does not exist.

        Args:
            project_dir: Target directory.
        """
        if not project_dir.exists():
            project_dir.mkdir(parents=True, exist_ok=False)

    def _initialize_npm(self, project_dir: Path) -> None:
        """Initialize an npm project.

        Args:
            project_dir: Working directory.
        """
        self.runner.run(["npm", "init", "-y"], cwd=project_dir)

    def _install_dev_dependencies(self, project_dir: Path) -> None:
        """Install TypeScript tooling dependencies.

        Args:
            project_dir: Working directory.
        """
        self.runner.run(
            ["npm", "install", "--save-dev", *DEFAULT_DEV_DEPS],
            cwd=project_dir,
        )

    def _write_project_files(self, project_dir: Path) -> None:
        """Write baseline project files.

        Args:
            project_dir: Working directory.
        """
        self._write_gitignore(project_dir)
        self._write_tsconfig(project_dir)
        self._write_index_ts(project_dir)

    def _write_gitignore(self, project_dir: Path) -> None:
        """Write .gitignore.

        Args:
            project_dir: Working directory.
        """
        self.files.write_text(project_dir / ".gitignore", GITIGNORE_CONTENT)

    def _write_tsconfig(self, project_dir: Path) -> None:
        """Write tsconfig.json.

        Args:
            project_dir: Working directory.
        """
        self.files.write_text(project_dir / "tsconfig.json", TSCONFIG_CONTENT)

    def _write_index_ts(self, project_dir: Path) -> None:
        """Write src/index.ts.

        Args:
            project_dir: Working directory.
        """
        self.files.write_text(project_dir / "src" / "index.ts", DEFAULT_INDEX_TS)

    def _configure_npm_scripts(self, project_dir: Path) -> None:
        """Configure npm scripts in package.json.

        Args:
            project_dir: Working directory.
        """
        self.pkgjson.clear_scripts(project_dir)
        self._add_default_scripts(project_dir)

    def _add_default_scripts(self, project_dir: Path) -> None:
        """Add default scripts to package.json.

        Args:
            project_dir: Working directory.
        """
        for name, cmd in DEFAULT_SCRIPTS.items():
            self.pkgjson.add_script(project_dir, name, cmd)


# -----------------------------
# CLI wiring
# -----------------------------


def _resolve_dir(value: str) -> Path:
    """Resolve a directory path to an absolute Path.

    Args:
        value: Path-like string.

    Returns:
        Absolute resolved Path.
    """
    return Path(value).expanduser().resolve()


def _handle_error(exc: TsProjError) -> None:
    """Convert internal errors to Click exceptions.

    Args:
        exc: Internal error.

    Raises:
        click.ClickException: Always.
    """
    raise click.ClickException(str(exc)) from exc


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """tsproj: scaffold TypeScript projects and manage package.json scripts."""


@cli.command("create")
@click.argument("project_name", type=str)
@click.option("--force", is_flag=True, help="Allow existing directory (use with care).")
def create_cmd(project_name: str, force: bool) -> None:
    """Create a new TypeScript project scaffold.

    Example:
      uv run tsproj create my-project
    """
    project_dir = _resolve_dir(project_name)
    scaffolder = TsProjectScaffolder(
        runner=CommandRunner(),
        files=FileWriter(),
        pkgjson=PackageJsonManager(),
    )

    try:
        click.echo(f"▶ Creating project directory: {project_dir}")
        scaffolder.create_project(project_dir, force=force)
        click.echo(f"✅ Project '{project_dir.name}' created successfully")
    except TsProjError as exc:
        _handle_error(exc)


@cli.group("scripts")
def scripts_group() -> None:
    """Manage npm scripts in package.json."""


@scripts_group.command("clear")
@click.option(
    "--project-dir",
    type=click.Path(file_okay=False, dir_okay=True, exists=True, path_type=Path),
    default=".",
    show_default=True,
    help="Directory containing package.json.",
)
def scripts_clear_cmd(project_dir: Path) -> None:
    """Clear all scripts from package.json.

    Example:
      uv run tsproj scripts clear --project-dir my-project
    """
    mgr = PackageJsonManager()
    try:
        mgr.clear_scripts(project_dir)
        click.echo("✅ All scripts cleared.")
    except TsProjError as exc:
        _handle_error(exc)


@scripts_group.command("add")
@click.argument("script_name", type=str)
@click.argument("script_command", type=str)
@click.option(
    "--project-dir",
    type=click.Path(file_okay=False, dir_okay=True, exists=True, path_type=Path),
    default=".",
    show_default=True,
    help="Directory containing package.json.",
)
def scripts_add_cmd(script_name: str, script_command: str, project_dir: Path) -> None:
    """Add (or overwrite) a script in package.json.

    Example:
      uv run tsproj scripts add dev "ts-node src/index.ts" --project-dir my-project
    """
    mgr = PackageJsonManager()
    try:
        mgr.add_script(project_dir, script_name, script_command)
        click.echo(f'✅ Script added: "{script_name}": "{script_command}"')
    except TsProjError as exc:
        _handle_error(exc)


if __name__ == "__main__":
    cli()
