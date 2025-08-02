"""
Base Migration Class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseMigration(ABC):
    """Base class for database migrations"""

    def __init__(self, version: str, description: str):
        self.version = version
        self.description = description
        self.created_at = datetime.now()

    @abstractmethod
    async def up(self, connection) -> bool:
        """Apply migration (upgrade)"""
        pass

    @abstractmethod
    async def down(self, connection) -> bool:
        """Rollback migration (downgrade)"""
        pass

    def __str__(self):
        return f"Migration {self.version}: {self.description}"

    def __repr__(self):
        return f"<{self.__class__.__name__}(version='{self.version}', description='{self.description}')>" 