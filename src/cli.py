"""
LDCM Command Line Interface
"""
import argparse
import getpass
import os
import sys
from src.config import DB_NAME, APP_VERSION
from src.vault import VaultManager
from src.injector import InjectionEngine

class CLI:
    def __init__(self):
        db_path = os.path.join(os.path.expanduser("~"), ".ldcm", DB_NAME)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.vault = VaultManager(db_path)
    
    def unlock_vault(self) -> bool:
        """Prompt for password and unlock vault"""
        if not self.vault.is_initialized():
            print("Vault not initialized. Run 'ldcm init' first.")
            return False
        
        password = getpass.getpass("Master Password: ")
        if self.vault.unlock(password):
            return True
        print("Invalid password.")
        return False
    
    def cmd_init(self, args):
        """Initialize a new vault"""
        if self.vault.is_initialized():
            print("Vault already initialized.")
            return
        
        password = getpass.getpass("Create Master Password: ")
        confirm = getpass.getpass("Confirm Password: ")
        
        if password != confirm:
            print("Passwords do not match.")
            return
        
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return
        
        if self.vault.initialize(password):
            print("✓ Vault initialized successfully.")
        else:
            print("Failed to initialize vault.")
    
    def cmd_projects(self, args):
        """List all projects"""
        if not self.unlock_vault():
            return
        
        projects = self.vault.get_projects()
        if not projects:
            print("No projects found. Create one with 'ldcm project add <name>'")
            return
        
        print("\nProjects:")
        print("-" * 40)
        for p in projects:
            envs = self.vault.get_environments(p.id)
            env_names = ", ".join([e.name for e in envs])
            print(f"  {p.id}. {p.name} [{env_names}]")
    
    def cmd_project_add(self, args):
        """Add a new project"""
        if not self.unlock_vault():
            return
        
        project = self.vault.create_project(args.name)
        print(f"✓ Project '{args.name}' created with environments: dev, staging, test")
    
    def cmd_project_delete(self, args):
        """Delete a project"""
        if not self.unlock_vault():
            return
        
        self.vault.delete_project(args.id)
        print(f"✓ Project deleted.")
    
    def cmd_secrets(self, args):
        """List secrets for a project/environment"""
        if not self.unlock_vault():
            return
        
        projects = self.vault.get_projects()
        project = next((p for p in projects if p.name == args.project), None)
        
        if not project:
            print(f"Project '{args.project}' not found.")
            return
        
        envs = self.vault.get_environments(project.id)
        env = next((e for e in envs if e.name == args.env), None)
        
        if not env:
            print(f"Environment '{args.env}' not found.")
            return
        
        secrets = self.vault.get_secrets(env.id)
        if not secrets:
            print(f"No secrets in {args.project}/{args.env}")
            return
        
        print(f"\nSecrets for {args.project}/{args.env}:")
        print("-" * 50)
        for s in secrets:
            value = self.vault.decrypt_secret(s.encrypted_value) if args.reveal else "••••••••"
            print(f"  {s.key}={value}")
    
    def cmd_secret_add(self, args):
        """Add a secret"""
        if not self.unlock_vault():
            return
        
        projects = self.vault.get_projects()
        project = next((p for p in projects if p.name == args.project), None)
        
        if not project:
            print(f"Project '{args.project}' not found.")
            return
        
        envs = self.vault.get_environments(project.id)
        env = next((e for e in envs if e.name == args.env), None)
        
        if not env:
            print(f"Environment '{args.env}' not found.")
            return
        
        value = args.value if args.value else getpass.getpass("Secret Value: ")
        self.vault.add_secret(env.id, args.key, value)
        print(f"✓ Secret '{args.key}' added to {args.project}/{args.env}")
    
    def cmd_secret_delete(self, args):
        """Delete a secret"""
        if not self.unlock_vault():
            return
        
        self.vault.delete_secret(args.id)
        print("✓ Secret deleted.")
    
    def cmd_inject(self, args):
        """Inject secrets into shell or command"""
        if not self.unlock_vault():
            return
        
        projects = self.vault.get_projects()
        project = next((p for p in projects if p.name == args.project), None)
        
        if not project:
            print(f"Project '{args.project}' not found.")
            return
        
        envs = self.vault.get_environments(project.id)
        env = next((e for e in envs if e.name == args.env), None)
        
        if not env:
            print(f"Environment '{args.env}' not found.")
            return
        
        secrets = self.vault.get_secrets(env.id)
        decrypted = {s.key: self.vault.decrypt_secret(s.encrypted_value) for s in secrets}
        
        if args.command:
            result = InjectionEngine.run_with_secrets(decrypted, args.command, args.dir)
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
        else:
            InjectionEngine.inject_shell(decrypted)
            print("✓ Terminal opened with injected secrets.")
    
    def cmd_export(self, args):
        """Export secrets to various formats"""
        if not self.unlock_vault():
            return
        
        projects = self.vault.get_projects()
        project = next((p for p in projects if p.name == args.project), None)
        
        if not project:
            print(f"Project '{args.project}' not found.")
            return
        
        envs = self.vault.get_environments(project.id)
        env = next((e for e in envs if e.name == args.env), None)
        
        if not env:
            print(f"Environment '{args.env}' not found.")
            return
        
        secrets = self.vault.get_secrets(env.id)
        decrypted = {s.key: self.vault.decrypt_secret(s.encrypted_value) for s in secrets}
        
        if args.format == "env":
            if args.output:
                InjectionEngine.generate_env_file(decrypted, args.output)
                print(f"✓ Exported to {args.output}")
            else:
                print('\n'.join([f'{k}={v}' for k, v in decrypted.items()]))
        elif args.format == "shell":
            print(InjectionEngine.generate_shell_export(decrypted))
        elif args.format == "powershell":
            print(InjectionEngine.generate_powershell_export(decrypted))
        elif args.format == "docker":
            print(InjectionEngine.generate_docker_env(decrypted))


def main():
    cli = CLI()
    
    parser = argparse.ArgumentParser(
        prog="ldcm",
        description="Local Developer Credentials Manager - Secure credential management for developers"
    )
    parser.add_argument("--version", action="version", version=f"LDCM v{APP_VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init
    subparsers.add_parser("init", help="Initialize a new vault")
    
    # projects
    subparsers.add_parser("projects", help="List all projects")
    
    # project add
    p_add = subparsers.add_parser("project-add", help="Add a new project")
    p_add.add_argument("name", help="Project name")
    
    # project delete
    p_del = subparsers.add_parser("project-delete", help="Delete a project")
    p_del.add_argument("id", type=int, help="Project ID")
    
    # secrets
    secrets_p = subparsers.add_parser("secrets", help="List secrets")
    secrets_p.add_argument("project", help="Project name")
    secrets_p.add_argument("env", help="Environment (dev/staging/test)")
    secrets_p.add_argument("--reveal", "-r", action="store_true", help="Show secret values")
    
    # secret add
    s_add = subparsers.add_parser("secret-add", help="Add a secret")
    s_add.add_argument("project", help="Project name")
    s_add.add_argument("env", help="Environment")
    s_add.add_argument("key", help="Secret key")
    s_add.add_argument("--value", "-v", help="Secret value (prompted if not provided)")
    
    # secret delete
    s_del = subparsers.add_parser("secret-delete", help="Delete a secret")
    s_del.add_argument("id", type=int, help="Secret ID")
    
    # inject
    inject_p = subparsers.add_parser("inject", help="Inject secrets into shell/command")
    inject_p.add_argument("project", help="Project name")
    inject_p.add_argument("env", help="Environment")
    inject_p.add_argument("--command", "-c", help="Command to run with secrets")
    inject_p.add_argument("--dir", "-d", help="Working directory")
    
    # export
    export_p = subparsers.add_parser("export", help="Export secrets")
    export_p.add_argument("project", help="Project name")
    export_p.add_argument("env", help="Environment")
    export_p.add_argument("--format", "-f", choices=["env", "shell", "powershell", "docker"], default="env")
    export_p.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        "init": cli.cmd_init,
        "projects": cli.cmd_projects,
        "project-add": cli.cmd_project_add,
        "project-delete": cli.cmd_project_delete,
        "secrets": cli.cmd_secrets,
        "secret-add": cli.cmd_secret_add,
        "secret-delete": cli.cmd_secret_delete,
        "inject": cli.cmd_inject,
        "export": cli.cmd_export,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
