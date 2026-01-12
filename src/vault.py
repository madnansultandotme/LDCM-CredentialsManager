from src.database import Database, Project, Environment, Secret, VaultSettings
from src.crypto import CryptoEngine
from datetime import datetime
import os

class VaultManager:
    def __init__(self, db_path: str):
        self.db = Database(db_path)
        self.crypto = CryptoEngine()
        self._unlocked = False
    
    def is_initialized(self) -> bool:
        """Check if vault has been set up with master password"""
        session = self.db.get_session()
        try:
            return session.query(VaultSettings).first() is not None
        finally:
            session.close()
    
    def initialize(self, master_password: str) -> bool:
        """Initialize vault with master password"""
        if self.is_initialized():
            return False
        password_hash, salt = self.crypto.hash_password(master_password)
        session = self.db.get_session()
        try:
            settings = VaultSettings(master_password_hash=password_hash, salt=salt)
            session.add(settings)
            session.commit()
            self.crypto.derive_key(master_password, salt)
            self._unlocked = True
            return True
        finally:
            session.close()
    
    def unlock(self, master_password: str) -> bool:
        """Unlock vault with master password"""
        session = self.db.get_session()
        try:
            settings = session.query(VaultSettings).first()
            if not settings:
                return False
            if self.crypto.verify_password(master_password, settings.master_password_hash, settings.salt):
                self.crypto.derive_key(master_password, settings.salt)
                self._unlocked = True
                return True
            return False
        finally:
            session.close()
    
    def lock(self):
        """Lock vault and clear encryption key"""
        self.crypto.clear_key()
        self._unlocked = False
    
    @property
    def is_unlocked(self) -> bool:
        return self._unlocked
    
    # Project operations
    def create_project(self, name: str) -> Project:
        session = self.db.get_session()
        try:
            project = Project(name=name)
            session.add(project)
            session.commit()
            session.refresh(project)
            # Create default environments
            for env_name in ['dev', 'staging', 'test']:
                env = Environment(project_id=project.id, name=env_name)
                session.add(env)
            session.commit()
            return project
        finally:
            session.close()
    
    def get_projects(self) -> list:
        session = self.db.get_session()
        try:
            return session.query(Project).all()
        finally:
            session.close()
    
    def delete_project(self, project_id: int):
        session = self.db.get_session()
        try:
            project = session.query(Project).filter_by(id=project_id).first()
            if project:
                session.delete(project)
                session.commit()
        finally:
            session.close()
    
    # Environment operations
    def get_environments(self, project_id: int) -> list:
        session = self.db.get_session()
        try:
            return session.query(Environment).filter_by(project_id=project_id).all()
        finally:
            session.close()
    
    # Secret operations
    def add_secret(self, environment_id: int, key: str, value: str, expires_at=None) -> Secret:
        if not self._unlocked:
            raise ValueError("Vault is locked")
        encrypted_value = self.crypto.encrypt(value)
        session = self.db.get_session()
        try:
            secret = Secret(environment_id=environment_id, key=key, encrypted_value=encrypted_value, expires_at=expires_at)
            session.add(secret)
            session.commit()
            session.refresh(secret)
            return secret
        finally:
            session.close()
    
    def get_secrets(self, environment_id: int) -> list:
        session = self.db.get_session()
        try:
            return session.query(Secret).filter_by(environment_id=environment_id).all()
        finally:
            session.close()
    
    def decrypt_secret(self, encrypted_value: str) -> str:
        if not self._unlocked:
            raise ValueError("Vault is locked")
        return self.crypto.decrypt(encrypted_value)
    
    def update_secret(self, secret_id: int, key: str = None, value: str = None):
        if not self._unlocked:
            raise ValueError("Vault is locked")
        session = self.db.get_session()
        try:
            secret = session.query(Secret).filter_by(id=secret_id).first()
            if secret:
                if key:
                    secret.key = key
                if value:
                    secret.encrypted_value = self.crypto.encrypt(value)
                session.commit()
        finally:
            session.close()
    
    def delete_secret(self, secret_id: int):
        session = self.db.get_session()
        try:
            secret = session.query(Secret).filter_by(id=secret_id).first()
            if secret:
                session.delete(secret)
                session.commit()
        finally:
            session.close()
