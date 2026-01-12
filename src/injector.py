import subprocess
import os
import tempfile
from typing import Dict

class InjectionEngine:
    """Handles credential injection into various targets"""
    
    @staticmethod
    def inject_shell(secrets: Dict[str, str], command: str = None, working_dir: str = None) -> subprocess.Popen:
        """Spawn shell/command with injected environment variables"""
        env = os.environ.copy()
        env.update(secrets)
        
        # Use working directory if provided, otherwise current directory
        cwd = working_dir if working_dir else os.getcwd()
        
        if command:
            # Run specific command with secrets in a new terminal window
            if os.name == 'nt':  # Windows
                # Open cmd, change to directory, set env vars, run command
                env_commands = ' & '.join([f'set {key}={value}' for key, value in secrets.items()])
                full_cmd = f'start cmd /K "cd /d {cwd} & {env_commands} & {command}"'
                process = subprocess.Popen(full_cmd, shell=True)
            else:  # Unix/Linux/Mac
                env_commands = ' '.join([f'{key}={value}' for key, value in secrets.items()])
                full_cmd = f'cd {cwd} && {env_commands} {command}'
                process = subprocess.Popen(
                    ['gnome-terminal', '--', 'bash', '-c', full_cmd],
                    env=env
                )
            return process
        else:
            # Open new terminal with secrets at specified directory
            if os.name == 'nt':  # Windows
                env_commands = ' & '.join([f'set {key}={value}' for key, value in secrets.items()])
                subprocess.Popen(
                    f'start cmd /K "cd /d {cwd} & {env_commands}"',
                    shell=True
                )
            else:  # Unix/Linux/Mac
                subprocess.Popen(
                    ['gnome-terminal', f'--working-directory={cwd}'],
                    env=env
                )
            return None
    
    @staticmethod
    def generate_env_file(secrets: Dict[str, str], output_path: str = None, auto_delete: bool = False) -> str:
        """Generate .env file with secrets"""
        if output_path is None:
            output_path = os.path.join(os.getcwd(), '.env')
        
        content = '\n'.join([f'{key}={value}' for key, value in secrets.items()])
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return output_path
    
    @staticmethod
    def generate_docker_env(secrets: Dict[str, str]) -> str:
        """Generate docker-compose compatible env string"""
        return '\n'.join([f'      - {key}={value}' for key, value in secrets.items()])
    
    @staticmethod
    def generate_shell_export(secrets: Dict[str, str]) -> str:
        """Generate shell export commands (for copy/paste)"""
        # Windows CMD format
        return '\n'.join([f'set {key}={value}' for key, value in secrets.items()])
    
    @staticmethod
    def generate_powershell_export(secrets: Dict[str, str]) -> str:
        """Generate PowerShell export commands"""
        return '\n'.join([f'$env:{key}="{value}"' for key, value in secrets.items()])
    
    @staticmethod
    def run_with_secrets(secrets: Dict[str, str], command: str, working_dir: str = None):
        """Run a command with injected secrets"""
        env = os.environ.copy()
        env.update(secrets)
        
        result = subprocess.run(
            command,
            shell=True,
            env=env,
            cwd=working_dir,
            capture_output=True,
            text=True
        )
        return result
