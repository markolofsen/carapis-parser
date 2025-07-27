"""
Demo Parser Database Migrations
"""

import sqlite3
from .base_migration import BaseMigration


class Migration001_Initial(BaseMigration):
    """Initial database schema"""
    
    def __init__(self):
        super().__init__("001", "Initial database schema")

    async def up(self, connection: sqlite3.Connection) -> bool:
        """Create initial tables"""
        try:
            cursor = connection.cursor()
            
            # Create demo_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS demo_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    item_id VARCHAR(100) UNIQUE NOT NULL,
                    title VARCHAR(500),
                    url VARCHAR(1000),
                    status VARCHAR(50) DEFAULT 'new',
                    listing_html TEXT,
                    detail_html TEXT,
                    html_content TEXT,
                    listing_data TEXT,
                    detail_data TEXT,
                    brand VARCHAR(100),
                    category VARCHAR(100),
                    price DECIMAL(15, 2),
                    processed_at DATETIME,
                    error_message TEXT
                )
            ''')
            
            # Create demo_statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS demo_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    parser_type VARCHAR(50),
                    total_items INTEGER DEFAULT 0,
                    processed_items INTEGER DEFAULT 0,
                    failed_items INTEGER DEFAULT 0,
                    start_time DATETIME,
                    end_time DATETIME,
                    duration_seconds FLOAT
                )
            ''')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 001 failed: {e}")
            return False

    async def down(self, connection: sqlite3.Connection) -> bool:
        """Drop all tables"""
        try:
            cursor = connection.cursor()
            
            cursor.execute('DROP TABLE IF EXISTS demo_items')
            cursor.execute('DROP TABLE IF EXISTS demo_statistics')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 001 rollback failed: {e}")
            return False


class Migration002_AddIndexes(BaseMigration):
    """Add database indexes for performance"""
    
    def __init__(self):
        super().__init__("002", "Add database indexes")

    async def up(self, connection: sqlite3.Connection) -> bool:
        """Add indexes"""
        try:
            cursor = connection.cursor()
            
            # Add indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_demo_items_status ON demo_items(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_demo_items_brand ON demo_items(brand)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_demo_items_category ON demo_items(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_demo_items_created_at ON demo_items(created_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_demo_items_processed_at ON demo_items(processed_at)')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 002 failed: {e}")
            return False

    async def down(self, connection: sqlite3.Connection) -> bool:
        """Remove indexes"""
        try:
            cursor = connection.cursor()
            
            cursor.execute('DROP INDEX IF EXISTS idx_demo_items_status')
            cursor.execute('DROP INDEX IF EXISTS idx_demo_items_brand')
            cursor.execute('DROP INDEX IF EXISTS idx_demo_items_category')
            cursor.execute('DROP INDEX IF EXISTS idx_demo_items_created_at')
            cursor.execute('DROP INDEX IF EXISTS idx_demo_items_processed_at')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 002 rollback failed: {e}")
            return False


class Migration003_AddMetadataFields(BaseMigration):
    """Add metadata fields to demo_items"""
    
    def __init__(self):
        super().__init__("003", "Add metadata fields")

    async def up(self, connection: sqlite3.Connection) -> bool:
        """Add metadata columns"""
        try:
            cursor = connection.cursor()
            
            # Add metadata columns
            cursor.execute('ALTER TABLE demo_items ADD COLUMN metadata TEXT')
            cursor.execute('ALTER TABLE demo_items ADD COLUMN tags TEXT')
            cursor.execute('ALTER TABLE demo_items ADD COLUMN priority INTEGER DEFAULT 0')
            cursor.execute('ALTER TABLE demo_items ADD COLUMN is_active BOOLEAN DEFAULT 1')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 003 failed: {e}")
            return False

    async def down(self, connection: sqlite3.Connection) -> bool:
        """Remove metadata columns (SQLite doesn't support DROP COLUMN, so we recreate table)"""
        try:
            cursor = connection.cursor()
            
            # Create new table without metadata columns
            cursor.execute('''
                CREATE TABLE demo_items_backup (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    item_id VARCHAR(100) UNIQUE NOT NULL,
                    title VARCHAR(500),
                    url VARCHAR(1000),
                    status VARCHAR(50) DEFAULT 'new',
                    listing_html TEXT,
                    detail_html TEXT,
                    html_content TEXT,
                    listing_data TEXT,
                    detail_data TEXT,
                    brand VARCHAR(100),
                    category VARCHAR(100),
                    price DECIMAL(15, 2),
                    processed_at DATETIME,
                    error_message TEXT
                )
            ''')
            
            # Copy data
            cursor.execute('''
                INSERT INTO demo_items_backup 
                SELECT id, created_at, updated_at, item_id, title, url, status,
                       listing_html, detail_html, html_content, listing_data, detail_data,
                       brand, category, price, processed_at, error_message
                FROM demo_items
            ''')
            
            # Drop old table and rename backup
            cursor.execute('DROP TABLE demo_items')
            cursor.execute('ALTER TABLE demo_items_backup RENAME TO demo_items')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 003 rollback failed: {e}")
            return False


class Migration004_AddConstraints(BaseMigration):
    """Add database constraints"""
    
    def __init__(self):
        super().__init__("004", "Add database constraints")

    async def up(self, connection: sqlite3.Connection) -> bool:
        """Add constraints"""
        try:
            cursor = connection.cursor()
            
            # Enable foreign key constraints
            cursor.execute('PRAGMA foreign_keys = ON')
            
            # Add check constraints (SQLite doesn't support CHECK constraints in ALTER TABLE)
            # We'll add them when creating new tables in future migrations
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 004 failed: {e}")
            return False

    async def down(self, connection: sqlite3.Connection) -> bool:
        """Remove constraints"""
        try:
            cursor = connection.cursor()
            
            # Disable foreign key constraints
            cursor.execute('PRAGMA foreign_keys = OFF')
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Migration 004 rollback failed: {e}")
            return False


# List of all migrations in order
MIGRATIONS = [
    Migration001_Initial(),
    Migration002_AddIndexes(),
    Migration003_AddMetadataFields(),
    Migration004_AddConstraints(),
] 