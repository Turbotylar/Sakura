"""
Secret manager

Abstractions for querying secrets
"""

from abc import ABC, abstractmethod
from functools import partial
from sakura.args import args
import os
import json

class SecretError(Exception):
    """Raised when querying a secret, and it cannot be found"""
    pass


class SecretManager(ABC):
    @abstractmethod
    def get_secret(self, scope: str, name: str) -> str:
        pass

    def reload(self):
        """Reload the secrets if they are memory-cached"""
        pass


class JSONSecretManager(SecretManager):
    def __init__(self, file) -> None:
        self.file = file
        with open(file) as f:
            self.secrets = json.load(f)
    
    def get_secret(self, scope: str, name: str) -> str:
        if scope not in self.secrets:
            raise SecretError(f"Requested scope '{scope}' was not found")
        elif name not in self.secrets[scope]:
            raise SecretError(f"Requested secret '{name}' in scope '{scope}' was not found")
        else:
            return self.secrets[scope][name]

    def reload(self):
        with open(self.file) as f:
            self.secrets = json.load(f)


class EnvironmentSecretManager(SecretManager):
    def get_secret(self, scope: str, name: str) -> str:
        key = f"SAKURA_{scope.upper()}_{name.upper()}"
        value = os.environ.get(key)

        if value is None:
            raise SecretError(f"Requested secret '{name}' in scope '{scope}' was not found")
        return value

SECRET_MANAGERS = {
    "json": partial(JSONSecretManager, args.secret_file),
    "env": EnvironmentSecretManager
}

SECRET_MANAGER = SECRET_MANAGERS[args.secret_store]()

def get_secret(scope: str, name: str) -> str:
    """
    Parameters
        scope   The name of the group, e.g. praw
        name    The name of the secret, e.g. client_id
    Returns
        The requested secret as a string

    Raises
        SecretError     The secret cannot be found
    """

    return SECRET_MANAGER.get_secret(scope, name)