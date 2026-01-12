from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    environments = relationship("Environment", back_populates="project", cascade="all, delete-orphan")

class Environment(Base):
    __tablename__ = 'environments'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(100), nullable=False)
    project = relationship("Project", back_populates="environments")
    secrets = relationship("Secret", back_populates="environment", cascade="all, delete-orphan")

class Secret(Base):
    __tablename__ = 'secrets'
    id = Column(Integer, primary_key=True)
    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False)
    key = Column(String(255), nullable=False)
    encrypted_value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    environment = relationship("Environment", back_populates="secrets")

class VaultSettings(Base):
    __tablename__ = 'vault_settings'
    id = Column(Integer, primary_key=True)
    master_password_hash = Column(String(255), nullable=False)
    salt = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
