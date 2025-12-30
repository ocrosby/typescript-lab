#!/usr/bin/env bash

# Exit immediately on error, unset var, or pipe failure
set -euo pipefail

# -------- Helpers --------
error() {
  echo "❌ $1" >&2
  exit 1
}

info() {
  echo "▶ $1"
}

# -------- Validate input --------
if [ "$#" -ne 1 ]; then
  error "Usage: $0 <project-name>"
fi

PROJECT_NAME="$1"

# -------- Create project --------
info "Creating project directory: $PROJECT_NAME"
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

# -------- Initialize npm --------
info "Initializing npm project"
npm init -y

# -------- Install dependencies --------
info "Installing TypeScript tooling"
npm install --save-dev typescript ts-node @types/node


# -------- Initialize the Git ignore list ----------
info "Creating .gitignore"
cat <<'EOF' > .gitignore
node_modules/
dist/
EOF

# -------- Initialize TypeScript --------
info "Creating tsconfig.json"
cat <<'EOF' > tsconfig.json
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

    // Style Options
    // "noImplicitReturns": true,
    // "noImplicitOverride": true,
    // "noUnusedLocals": true,
    // "noUnusedParameters": true,
    // "noFallthroughCasesInSwitch": true,
    // "noPropertyAccessFromIndexSignature": true,

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
EOF

# -------- Configure npm scripts --------
SCRIPT_MANAGER="../scripts/scripts-manager.js"

if [ ! -f "$SCRIPT_MANAGER" ]; then
  error "scripts-manager.js not found at $SCRIPT_MANAGER"
fi

info "Configuring npm scripts"
node "$SCRIPT_MANAGER" clear
node "$SCRIPT_MANAGER" add dev "ts-node src/index.ts"
node "$SCRIPT_MANAGER" add build "tsc"
node "$SCRIPT_MANAGER" add typecheck "tsc --noEmit"
node "$SCRIPT_MANAGER" add start "node dist/index.js"

mkdir -p src/
echo 'console.log("demo");' > src/index.ts

info "✅ Project '$PROJECT_NAME' created successfully"
