"""
Simple tests for database functionality
"""

import pytest
import sys
import tempfile
import os
import sqlite3
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))


class TestDatabaseSimple:
    """Simple database tests"""

    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

    def test_sqlite_connection(self, temp_db_path):
        """Test basic SQLite connection"""
        connection = sqlite3.connect(temp_db_path)
        cursor = connection.cursor()
        
        # Test basic SQL operations
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO test_table (id, name) VALUES (1, 'test')")
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()
        
        assert result[0] == 1
        assert result[1] == 'test'
        
        connection.close()

    def test_database_tables_creation(self, temp_db_path):
        """Test creating database tables"""
        connection = sqlite3.connect(temp_db_path)
        cursor = connection.cursor()
        
        # Create demo_items table
        cursor.execute("""
            CREATE TABLE demo_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                brand TEXT DEFAULT '',
                category TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                listing_data TEXT DEFAULT '{}',
                detail_data TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                tags TEXT DEFAULT '[]',
                priority INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create demo_statistics table
        cursor.execute("""
            CREATE TABLE demo_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parser_type TEXT NOT NULL,
                total_items INTEGER DEFAULT 0,
                processed_items INTEGER DEFAULT 0,
                failed_items INTEGER DEFAULT 0,
                duration_seconds REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "demo_items" in tables
        assert "demo_statistics" in tables
        
        connection.close()

    def test_demo_items_operations(self, temp_db_path):
        """Test demo_items table operations"""
        connection = sqlite3.connect(temp_db_path)
        cursor = connection.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE demo_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                brand TEXT DEFAULT '',
                category TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                listing_data TEXT DEFAULT '{}',
                detail_data TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                tags TEXT DEFAULT '[]',
                priority INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("""
            INSERT INTO demo_items (item_id, title, brand, category, listing_data)
            VALUES (?, ?, ?, ?, ?)
        """, ("test_item_001", "Test Car", "Toyota", "sedan", '{"price": 25000}'))
        
        # Query test data
        cursor.execute("SELECT * FROM demo_items WHERE item_id = ?", ("test_item_001",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "test_item_001"  # item_id
        assert result[2] == "Test Car"       # title
        assert result[3] == "Toyota"         # brand
        assert result[4] == "sedan"          # category
        
        connection.close()

    def test_demo_statistics_operations(self, temp_db_path):
        """Test demo_statistics table operations"""
        connection = sqlite3.connect(temp_db_path)
        cursor = connection.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE demo_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parser_type TEXT NOT NULL,
                total_items INTEGER DEFAULT 0,
                processed_items INTEGER DEFAULT 0,
                failed_items INTEGER DEFAULT 0,
                duration_seconds REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("""
            INSERT INTO demo_statistics (parser_type, total_items, processed_items, failed_items, duration_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, ("demo_parser", 100, 85, 15, 120.5))
        
        # Query test data
        cursor.execute("SELECT * FROM demo_statistics WHERE parser_type = ?", ("demo_parser",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "demo_parser"    # parser_type
        assert result[2] == 100              # total_items
        assert result[3] == 85               # processed_items
        assert result[4] == 15               # failed_items
        assert result[5] == 120.5            # duration_seconds
        
        connection.close()

    def test_database_integration(self, temp_db_path):
        """Test comprehensive database operations"""
        connection = sqlite3.connect(temp_db_path)
        cursor = connection.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE demo_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                brand TEXT DEFAULT '',
                category TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                listing_data TEXT DEFAULT '{}',
                detail_data TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                tags TEXT DEFAULT '[]',
                priority INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE demo_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parser_type TEXT NOT NULL,
                total_items INTEGER DEFAULT 0,
                processed_items INTEGER DEFAULT 0,
                failed_items INTEGER DEFAULT 0,
                duration_seconds REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert multiple items
        test_items = [
            ("item1", "Item 1", "Brand1", "category1"),
            ("item2", "Item 2", "Brand2", "category2"),
            ("item3", "Item 3", "Brand3", "category3")
        ]
        
        for item_id, title, brand, category in test_items:
            cursor.execute("""
                INSERT INTO demo_items (item_id, title, brand, category)
                VALUES (?, ?, ?, ?)
            """, (item_id, title, brand, category))
        
        # Insert statistics
        cursor.execute("""
            INSERT INTO demo_statistics (parser_type, total_items, processed_items, failed_items, duration_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, ("test_parser", 3, 2, 1, 60.0))
        
        # Query all items
        cursor.execute("SELECT COUNT(*) FROM demo_items")
        item_count = cursor.fetchone()[0]
        assert item_count == 3
        
        # Query statistics
        cursor.execute("SELECT * FROM demo_statistics WHERE parser_type = ?", ("test_parser",))
        stats = cursor.fetchone()
        assert stats[2] == 3  # total_items
        assert stats[3] == 2  # processed_items
        assert stats[4] == 1  # failed_items
        
        connection.close() 