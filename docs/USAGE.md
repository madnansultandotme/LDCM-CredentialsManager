# LDCM Documentation

## Overview

Local Developer Credentials Manager (LDCM) is a secure desktop application for managing development credentials. It provides both a graphical interface and command-line tools.

## Getting Started

### First-Time Setup

1. Launch the application: `python main.py`
2. Create a master password (minimum 8 characters)
3. Your vault is now ready

### Theme Toggle

Click the theme icon in the top-right corner to switch between light and dark modes:
- ☀️ (sun) - Click to switch to light mode
- 🌙 (moon) - Click to switch to dark mode

### Creating Your First Project

**GUI:**
1. Click the `+` button in the Projects sidebar
2. Enter project name
3. Default environments (dev, staging, test) are created automatically

**CLI:**
```bash
python -m src.cli project-add myproject
```

## Managing Secrets

### Adding Secrets

**GUI:**
1. Select a project
2. Select an environment tab (dev/staging/test)
3. Click "Add Secret"
4. Enter key and value

**CLI:**
```bash
# Interactive (prompts for value)
python -m src.cli secret-add myproject dev API_KEY

# Direct value
python -m src.cli secret-add myproject dev API_KEY --value "sk-123456"
```

### Viewing Secrets

**GUI:**
- Click the 👁️ icon to reveal a secret
- Click 📋 to copy to clipboard

**CLI:**
```bash
# Masked values
python -m src.cli secrets myproject dev

# Revealed values
python -m src.cli secrets myproject dev --reveal
```

## Injecting Secrets

### Shell Injection

Opens a new terminal with all secrets loaded as environment variables.

**GUI:**
1. Select project and environment
2. Click "Inject & Run"
3. Choose "Open Terminal with Secrets"

**CLI:**
```bash
python -m src.cli inject myproject dev
```

### Run Command with Secrets

Execute a command with secrets injected.

**GUI:**
1. Click "Inject & Run"
2. Enter command in the text field
3. Click "Run Command"

**CLI:**
```bash
python -m src.cli inject myproject dev --command "npm start"
python -m src.cli inject myproject dev --command "python app.py" --dir ./backend
```

## Exporting Secrets

### .env File

```bash
# To stdout
python -m src.cli export myproject dev --format env

# To file
python -m src.cli export myproject dev --format env --output .env
```

### Shell Export (CMD)

```bash
python -m src.cli export myproject dev --format shell
```

Output:
```
set API_KEY=sk-123456
set DB_URL=postgres://localhost/db
```

### PowerShell Export

```bash
python -m src.cli export myproject dev --format powershell
```

Output:
```powershell
$env:API_KEY="sk-123456"
$env:DB_URL="postgres://localhost/db"
```

### Docker Compose Format

```bash
python -m src.cli export myproject dev --format docker
```

Output:
```yaml
      - API_KEY=sk-123456
      - DB_URL=postgres://localhost/db
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `init` | Initialize a new vault |
| `projects` | List all projects |
| `project-add <name>` | Create a new project |
| `project-delete <id>` | Delete a project |
| `secrets <project> <env>` | List secrets |
| `secret-add <project> <env> <key>` | Add a secret |
| `secret-delete <id>` | Delete a secret |
| `inject <project> <env>` | Inject secrets |
| `export <project> <env>` | Export secrets |

### Common Options

| Option | Description |
|--------|-------------|
| `--reveal, -r` | Show secret values (secrets command) |
| `--value, -v` | Provide value directly (secret-add) |
| `--command, -c` | Command to run (inject) |
| `--dir, -d` | Working directory (inject) |
| `--format, -f` | Export format: env/shell/powershell/docker |
| `--output, -o` | Output file path (export) |

## Security Best Practices

1. Use a strong master password (12+ characters recommended)
2. Lock the vault when not in use
3. Don't commit `.env` files to version control
4. Rotate secrets periodically
5. Use different secrets per environment

## Data Storage

- Vault location: `~/.ldcm/ldcm_vault.db`
- All secrets are encrypted at rest
- Master password is never stored (only its hash)

## Troubleshooting

### "Vault not initialized"
Run `python -m src.cli init` or launch the GUI to create a vault.

### "Invalid password"
The master password is case-sensitive. If forgotten, delete `~/.ldcm/ldcm_vault.db` to reset (all secrets will be lost).

### GUI doesn't launch
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Color Scheme Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Deep Blue | #1F3A93 | Headers, navigation |
| Slate Gray | #2F3D4A | Backgrounds, secondary UI |
| Cyan/Teal | #1ABC9C | Action buttons, highlights |
| Amber | #F39C12 | Warnings |
| Green | #27AE60 | Success, secure status |
| Red | #E74C3C | Errors, delete actions |
