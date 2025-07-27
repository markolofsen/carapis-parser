"""
Demo Parser Module
Reference implementation for web parsing with async architecture
"""

from .utils.logger import get_logger
from .config import DemoConfig
from .database import DemoDatabaseManager, DemoItem, DemoStatistics, initialize_database, get_database_stats
from .adapter import DemoDataServerAdapter
from .core.parser import DemoParser
from .core.listing_parser import DemoListingParser
from .core.detail_parser import DemoDetailParser

__all__ = [
    'get_logger',
    'DemoConfig',
    'DemoDatabaseManager',
    'DemoItem',
    'DemoStatistics',
    'initialize_database',
    'get_database_stats',
    'DemoDataServerAdapter',
    'DemoParser',
    'DemoListingParser',
    'DemoDetailParser'
] 