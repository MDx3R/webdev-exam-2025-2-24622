import os
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from typing import Literal

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel


ALLOWED_TAGS = [
    "p",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "h1",
    "h2",
    "h3",
]


class RunEnvironment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    TEST = "test"


class AuthConfig(BaseModel):
    SECRET_KEY: str = "secret-key"


class DatabaseConfig(BaseModel):
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DBMS: Literal["sqlite", "postgresql", "mysql"] = "sqlite"
    SQLITE_MEMORY: bool = False

    @property
    def database_url(self) -> str:
        if self.DBMS == "sqlite":
            if self.SQLITE_MEMORY:
                return "sqlite:///:memory:"
            db_file = self.DB_NAME or "default"
            return f"sqlite:///{db_file}.db"

        return (
            f"{self.DBMS}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class FileStoreConfig(BaseModel):
    TYPE: str = "local"
    ACCESS: str = "uploads"


class Config(BaseModel):
    ENV: RunEnvironment
    AUTH: AuthConfig
    DB: DatabaseConfig
    FILE: FileStoreConfig

    @classmethod
    def load(cls) -> "Config":
        path = cls.fetch_config_path()
        return cls.load_from_path(path)

    @staticmethod
    def load_from_path(path: str | Path) -> "Config":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found at: {path}")

        with path.open("r") as f:
            data = yaml.safe_load(f)

        return Config.model_validate(data)

    @staticmethod
    def fetch_config_path() -> Path:
        default = "config/config.yaml"

        parser = ArgumentParser(description="Load config path")
        parser.add_argument("--config", type=str, help="Path to config file")
        args, _ = parser.parse_known_args()

        load_dotenv()
        return Path(args.config or os.getenv("CONFIG_PATH") or default)
