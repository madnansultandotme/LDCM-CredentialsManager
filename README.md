# Local Developer Credentials Manager (LDCM)

A secure, offline-first desktop application for managing and injecting local development credentials.

## Features

- 🔐 AES-256-GCM encrypted secret storage
- 🔑 Argon2 password hashing
- 📁 Project-based organization with environments (dev/staging/test)
- ⚡ One-click secret injection into shell or commands
- 📄 Export to .env, shell, PowerShell, Docker formats
- 🖥️ Modern GUI with light/dark theme toggle (☀️/🌙)
- 💻 Full CLI support for automation
- 🔒 Auto-lock on inactivity
- 💾 100% offline - no cloud dependency

## Installation

### Prerequisites
- Python 3.10+

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd ldcm

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### GUI Application

```bash
python main.py
```

On first launch, create a master password. This encrypts all your secrets locally.

### CLI Commands

```bash
# Initialize vault
python -m src.cli init

# List projects
python -m src.cli projects

# Add a project
python -m src.cli project-add myapp

# Add a secret
python -m src.cli secret-add myapp dev API_KEY
python -m src.cli secret-add myapp dev DB_URL --value "postgres://localhost/db"

# List secrets
python -m src.cli secrets myapp dev
python -m src.cli secrets myapp dev --reveal

# Inject secrets and run command
python -m src.cli inject myapp dev --command "npm start"

# Open terminal with secrets
python -m src.cli inject myapp dev

# Export secrets
python -m src.cli export myapp dev --format env --output .env
python -m src.cli export myapp dev --format powershell
python -m src.cli export myapp dev --format docker
```

## Project Structure

```
ldcm/
├── main.py              # GUI entry point
├── requirements.txt     # Dependencies
├── README.md
├── docs/
│   └── USAGE.md        # Detailed documentation
└── src/
    ├── cli.py          # CLI interface
    ├── config.py       # App configuration & colors
    ├── crypto.py       # Encryption engine (AES-GCM + Argon2)
    ├── database.py     # SQLAlchemy models
    ├── injector.py     # Secret injection engine
    ├── vault.py        # Vault manager
    └── gui/
        ├── app.py      # Main window
        └── screens/
            ├── unlock.py    # Auth screen
            └── dashboard.py # Main dashboard
```

## Security

- Secrets encrypted with AES-256-GCM
- Master password hashed with Argon2
- Encryption key derived using PBKDF2 (100,000 iterations)
- Keys zeroed from memory on lock
- Vault stored at `~/.ldcm/ldcm_vault.db`

## License

MIT
