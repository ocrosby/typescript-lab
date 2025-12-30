#!/usr/bin/env node
/**
 * scripts-manager.js
 *
 * Usage:
 *   node scripts-manager.js clear
 *   node scripts-manager.js add <scriptName> "<command>"
 *
 * Examples:
 *   node scripts-manager.js clear
 *   node scripts-manager.js add dev "ts-node src/index.ts"
 *   node scripts-manager.js add build "tsc"
 */

const fs = require("fs");
const path = require("path");

const PACKAGE_JSON = path.join(process.cwd(), "package.json");

function fail(message) {
  console.error(`❌ ${message}`);
  process.exit(1);
}

function loadPackageJson() {
  if (!fs.existsSync(PACKAGE_JSON)) {
    fail("package.json not found in the current directory.");
  }

  try {
    return JSON.parse(fs.readFileSync(PACKAGE_JSON, "utf8"));
  } catch {
    fail("package.json is not valid JSON.");
  }
}

function savePackageJson(pkg) {
  fs.writeFileSync(PACKAGE_JSON, JSON.stringify(pkg, null, 2) + "\n", "utf8");
}

function clearScripts(pkg) {
  pkg.scripts = {};
  savePackageJson(pkg);
  console.log("✅ All scripts cleared.");
}

function addScript(pkg, name, command) {
  if (!pkg.scripts) {
    pkg.scripts = {};
  }

  pkg.scripts[name] = command;
  savePackageJson(pkg);
  console.log(`✅ Script added: "${name}": "${command}"`);
}

/* -------------------- CLI -------------------- */

const [, , action, scriptName, scriptCommand] = process.argv;
const pkg = loadPackageJson();

switch (action) {
  case "clear":
    clearScripts(pkg);
    break;

  case "add":
    if (!scriptName || !scriptCommand) {
      fail('Usage: add <scriptName> "<command>"');
    }
    addScript(pkg, scriptName, scriptCommand);
    break;

  default:
    console.log(`
Usage:
  node scripts-manager.js clear
  node scripts-manager.js add <scriptName> "<command>"

Examples:
  node scripts-manager.js clear
  node scripts-manager.js add dev "ts-node src/index.ts"
`);
    process.exit(1);
}
