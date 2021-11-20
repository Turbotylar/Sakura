"""Secret manager

Abstractions for querying secrets
"""

from abc import ABC, abstractmethod


class SecretError(Exception):
    """Raised when querying a secret, and it cannot be found"""
    pass

class SecretManager(ABC):
    @abstractmethod
    def get_secret(self, scope, name):
        pass

class JSONSecretManager(SecretManager):
    def __init__(self, file) -> None:
        import json
        with open(file) as f:
            self.secrets = json.load(f)
    
    def get_secret(self, scope, name):
        if scope not in self.secrets:
            raise SecretError(f"Requested scope '{scope}' was not found")
        elif name not in self.secrets[scope]:
            raise SecretError(f"Requested secret '{name}' in scope '{scope}' was not found")
        else:
            return self.secrets[scope][name]


SECRET_MANAGER = JSONSecretManager("config.json")

def get_secret(scope, name) -> str:
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