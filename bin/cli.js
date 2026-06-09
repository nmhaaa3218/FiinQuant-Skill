#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// Helper to expand ~ in paths
function expandHome(filepath) {
  if (filepath.startsWith('~/') || filepath === '~') {
    return path.join(os.homedir(), filepath.slice(1));
  }
  return filepath;
}

// Print Helpers
function printHeader(title) {
  console.log(`\n============================================================`);
  console.log(`  ${title}`);
  console.log(`============================================================\n`);
}

function printSuccess(message) {
  console.log(`  [OK] ${message}`);
}

function printWarning(message) {
  console.log(`  [!] ${message}`);
}

// Deep copy helper for directories
function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Parse args
const args = process.argv.slice(2);
const options = {
  claude: false,
  cursor: false,
  gemini: false,
  codex: false,
  antigravity: false,
  agy: false,
  kiro: false,
  opencode: false,
  adal: false,
  customPath: null,
  username: process.env.FIIN_USERNAME || null,
  password: process.env.FIIN_PASSWORD || null
};

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--claude') options.claude = true;
  else if (arg === '--cursor') options.cursor = true;
  else if (arg === '--gemini') options.gemini = true;
  else if (arg === '--codex') options.codex = true;
  else if (arg === '--antigravity') options.antigravity = true;
  else if (arg === '--agy') options.agy = true;
  else if (arg === '--kiro') options.kiro = true;
  else if (arg === '--opencode') options.opencode = true;
  else if (arg === '--adal') options.adal = true;
  else if (arg === '--path') {
    options.customPath = args[++i];
  } else if (arg === '--username' || arg === '-u') {
    options.username = args[++i];
  } else if (arg === '--password' || arg === '-p') {
    options.password = args[++i];
  }
}

// Determine destination directory
let skillDestPath = expandHome('~/.skills/fiinquant');
if (options.customPath) {
  skillDestPath = path.resolve(expandHome(options.customPath));
} else if (options.kiro) {
  skillDestPath = expandHome('~/.kiro/skills/fiinquant');
} else if (options.adal) {
  skillDestPath = path.resolve(expandHome('.adal/skills/fiinquant'));
} else if (options.opencode) {
  skillDestPath = path.resolve(expandHome('.agents/skills/fiinquant'));
}

printHeader('FiinQuant Skill NPM Installer');

// Step 1: Install Python dependencies
console.log('[1/4] Installing Python FiinQuantX Library...');

function runPip(cmdStr) {
  try {
    execSync(cmdStr, { stdio: 'inherit' });
    return true;
  } catch (e) {
    return false;
  }
}

// Try standard install
const pipInstallCmd = 'python3 -m pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx --user';
let success = runPip(pipInstallCmd);

if (!success) {
  printWarning('Standard installation blocked. Retrying with --break-system-packages (PEP 668)...');
  success = runPip(`${pipInstallCmd} --break-system-packages`);
}

if (!success) {
  printWarning('Failed to install fiinquantx. Please install manually later.');
} else {
  printSuccess('fiinquantx package installed.');
  
  // Downgrade signalrcore
  console.log('  Patching signalrcore compatibility version...');
  runPip('python3 -m pip uninstall signalrcore -y --break-system-packages 2>/dev/null || true');
  runPip('python3 -m pip install "signalrcore>=0.9,<1.0" --user --break-system-packages');
  printSuccess('signalrcore version downgraded.');
}

// Step 2: Deploy Skill Files
console.log('\n[2/4] Deploying Skill Files...');
const sourceSkillsPath = path.join(__dirname, '..', 'skills', 'fiinquant');

if (fs.existsSync(sourceSkillsPath)) {
  try {
    copyDir(sourceSkillsPath, skillDestPath);
    printSuccess(`Skill files deployed to ${skillDestPath}`);
  } catch (e) {
    printWarning(`Failed to deploy local files: ${e.message}`);
  }
} else {
  printWarning(`Source files not found at ${sourceSkillsPath}. Skipping deployment.`);
}

// Step 3: Write Credentials
console.log('\n[3/4] Configuring Credentials...');
if (options.username && options.password) {
  try {
    fs.mkdirSync(skillDestPath, { recursive: true });
    fs.writeFileSync(
      path.join(skillDestPath, '.env'),
      `FIIN_USERNAME=${options.username}\nFIIN_PASSWORD=${options.password}\n`,
      'utf8'
    );
    printSuccess('Credentials saved to .env file.');
  } catch (e) {
    printWarning(`Failed to save credentials: ${e.message}`);
  }
} else {
  printSuccess('No credentials provided. Skipping .env creation.');
}

// Step 4: Register Skill/MCP Server in Agent Harnesses
console.log('\n[4/4] Registering MCP Server with Host Systems...');

const mcpScriptPath = path.join(skillDestPath, 'scripts', 'fiinquant_search.py');

// Register Cursor
if (options.cursor) {
  let settingsPath = '';
  if (process.platform === 'darwin') {
    settingsPath = expandHome('~/Library/Application Support/Cursor/User/settings.json');
  } else if (process.platform === 'win32') {
    settingsPath = path.join(process.env.APPDATA || '', 'Cursor', 'User', 'settings.json');
  } else {
    settingsPath = expandHome('~/.config/Cursor/User/settings.json');
  }

  console.log(`  Registering with Cursor settings at: ${settingsPath}`);
  try {
    let settings = {};
    if (fs.existsSync(settingsPath)) {
      settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    } else {
      fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
    }

    if (!settings['mcp.multiModeServers']) {
      settings['mcp.multiModeServers'] = {};
    }

    settings['mcp.multiModeServers']['fiinquant-docs'] = {
      type: 'stdio',
      command: 'python3',
      args: [mcpScriptPath, '--mcp'],
      enabled: true
    };

    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), 'utf8');
    printSuccess('Registered with Cursor MCP servers successfully.');
  } catch (e) {
    printWarning(`Failed to register with Cursor: ${e.message}`);
  }
}

// Register Claude Desktop
if (options.claude) {
  let claudePath = '';
  if (process.platform === 'darwin') {
    claudePath = expandHome('~/Library/Application Support/Claude/claude_desktop_config.json');
  } else {
    claudePath = path.join(process.env.APPDATA || '', 'Claude', 'claude_desktop_config.json');
  }

  console.log(`  Registering with Claude Desktop config at: ${claudePath}`);
  try {
    let config = {};
    if (fs.existsSync(claudePath)) {
      config = JSON.parse(fs.readFileSync(claudePath, 'utf8'));
    } else {
      fs.mkdirSync(path.dirname(claudePath), { recursive: true });
    }

    if (!config.mcpServers) {
      config.mcpServers = {};
    }

    config.mcpServers['fiinquant-docs'] = {
      command: 'python3',
      args: [mcpScriptPath, '--mcp']
    };

    fs.writeFileSync(claudePath, JSON.stringify(config, null, 2), 'utf8');
    printSuccess('Registered with Claude Desktop config successfully.');
  } catch (e) {
    printWarning(`Failed to register with Claude: ${e.message}`);
  }
}

// Register Antigravity
if (options.antigravity || options.agy) {
  const agPath = expandHome('~/.config/antigravity/config.json');
  console.log(`  Registering with Antigravity config at: ${agPath}`);
  try {
    let config = {};
    if (fs.existsSync(agPath)) {
      config = JSON.parse(fs.readFileSync(agPath, 'utf8'));
    } else {
      fs.mkdirSync(path.dirname(agPath), { recursive: true });
    }

    if (!config.skills) {
      config.skills = [];
    }

    // Avoid duplication
    config.skills = config.skills.filter(s => s.name !== 'fiinquant');
    config.skills.push({
      name: 'fiinquant',
      location: skillDestPath
    });

    fs.writeFileSync(agPath, JSON.stringify(config, null, 2), 'utf8');
    printSuccess('Registered with Antigravity skills successfully.');
  } catch (e) {
    printWarning(`Failed to register with Antigravity: ${e.message}`);
  }
}

// Register OpenCode
if (options.opencode) {
  const opPath = expandHome('~/.config/opencode/opencode.json');
  console.log(`  Registering with OpenCode config at: ${opPath}`);
  try {
    let config = {};
    if (fs.existsSync(opPath)) {
      config = JSON.parse(fs.readFileSync(opPath, 'utf8'));
    } else {
      fs.mkdirSync(path.dirname(opPath), { recursive: true });
    }

    if (!config.skills) {
      config.skills = [];
    }

    config.skills = config.skills.filter(s => s.name !== 'fiinquant');
    config.skills.push({
      name: 'fiinquant',
      location: skillDestPath
    });

    fs.writeFileSync(opPath, JSON.stringify(config, null, 2), 'utf8');
    printSuccess('Registered with OpenCode skills successfully.');
  } catch (e) {
    printWarning(`Failed to register with OpenCode: ${e.message}`);
  }
}

console.log('\n============================================================');
console.log('  Installation Complete!');
console.log('============================================================');
console.log(`\nSkill has been set up successfully at: ${skillDestPath}`);
console.log(`You can search the docs using:`);
console.log(`  python3 ${mcpScriptPath} "WebSocket realtime"`);
console.log(`\nRestart your agent and ask: 'I want to use the fiinquant skill' to start coding!`);
