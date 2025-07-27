#!/usr/bin/env python3
"""
Simple database tests - stable version
"""

import os
import sys
import json
import asyncio
import pytest
from datetime import datetime

# Add backend/django to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# Import database modules (works when problematic imports are commented)
from module.database.models import DemoItem, DemoStatistics, initialize_database, database
from module.database.database import DemoDatabaseManager


@pytest.fixture(scope="function")
def db_manager():
    """Database manager fixture with proper cleanup"""
    # Initialize database
    try:
        initialize_database()
    except Exception:
        pass
    
    manager = DemoDatabaseManager()
    yield manager
    
    # Cleanup after each test
    try:
        if not database.is_closed():
            database.execute_sql("DELETE FROM demo_items")
            database.execute_sql("DELETE FROM demo_statistics")
            database.commit()
    except Exception:
        pass


@pytest.mark.asyncio
async def test_save_and_retrieve_listing(db_manager):
    """Test saving and retrieving a listing"""
    print("Testing save and retrieve listing...")
    
    # Test data
    listing_data = {
        "id": "simple_test_123",
        "title": "Simple Test Car",
        "brand": "Toyota",
        "category": "Sedan",
        "price": "25000",
        "url": "https://test.com/car/123",
        "html_content": "<div>Test HTML</div>",
        "saved_at": 1234567890.0
    }
    
    # Save listing
    result = await db_manager.save_listing_to_db(listing_data)
    assert result is True
    print(f"✅ Save result: {result}")
    
    # Retrieve and verify
    saved_item = DemoItem.get(DemoItem.item_id == "simple_test_123")
    assert saved_item.title == "Simple Test Car"
    assert saved_item.brand == "Toyota"
    assert saved_item.status == "processed"
    print(f"✅ Retrieved item: {saved_item.title}")


@pytest.mark.asyncio
async def test_save_and_retrieve_detail(db_manager):
    """Test saving and retrieving detail data"""
    print("Testing save and retrieve detail...")
    
    # First save listing
    listing_data = {
        "id": "simple_detail_123",
        "title": "Simple Detail Car",
        "brand": "Honda",
        "category": "SUV",
        "price": "30000",
        "url": "https://test.com/car/detail123",
        "html_content": "<div>Listing HTML</div>",
        "saved_at": 1234567890.0
    }
    await db_manager.save_listing_to_db(listing_data)
    
    # Then save detail
    detail_data = {
        "id": "simple_detail_123",
        "title": "Simple Detail Car - Full Details",
        "specifications": {
            "engine": "2.0L Turbo",
            "transmission": "CVT",
            "fuel_type": "Gasoline"
        },
        "features": ["Apple CarPlay", "Android Auto", "Honda Sensing"],
        "html_content": "<div>Detail HTML</div>"
    }
    
    result = await db_manager.save_detail_to_db(detail_data)
    assert result is True
    print(f"✅ Detail save result: {result}")
    
    # Verify detail was saved
    saved_item = DemoItem.get(DemoItem.item_id == "simple_detail_123")
    assert saved_item.detail_html == "<div>Detail HTML</div>"
    assert saved_item.detail_data is not None
    print(f"✅ Detail data saved successfully")


@pytest.mark.asyncio
async def test_batch_operations(db_manager):
    """Test batch operations"""
    print("Testing batch operations...")
    
    # Batch listings
    listings_data = [
        {
            "id": "batch_1",
            "title": "Batch Car 1",
            "brand": "BMW",
            "category": "Sedan",
            "price": "45000",
            "url": "https://test.com/car/batch1",
            "html_content": "<div>Batch 1 HTML</div>",
            "saved_at": 1234567890.0
        },
        {
            "id": "batch_2",
            "title": "Batch Car 2",
            "brand": "Mercedes",
            "category": "SUV",
            "price": "55000",
            "url": "https://test.com/car/batch2",
            "html_content": "<div>Batch 2 HTML</div>",
            "saved_at": 1234567890.0
        }
    ]
    
    # Save batch
    result = await db_manager.save_listings_batch_to_db(listings_data)
    assert result == 2
    print(f"✅ Batch save result: {result}")
    
    # Verify batch items
    saved_items = list(DemoItem.select().where(DemoItem.item_id.in_(["batch_1", "batch_2"])))
    assert len(saved_items) == 2
    print(f"✅ Verified {len(saved_items)} batch items")


@pytest.mark.asyncio
async def test_database_info(db_manager):
    """Test getting database information"""
    print("Testing database info...")
    
    info = await db_manager.get_database_info()
    
    # Verify basic info
    assert info["database_type"] == "sqlite3_peewee"
    assert info["tables"] == ["demo_items", "demo_statistics"]
    assert "database_path" in info
    assert "demo_parser.db" in info["database_path"]
    print(f"✅ Database info verified: {info['database_type']}")


@pytest.mark.asyncio
async def test_clear_operations(db_manager):
    """Test clear operations"""
    print("Testing clear operations...")
    
    # Add some test data
    listing_data = {
        "id": "clear_test_123",
        "title": "Clear Test Car",
        "brand": "Audi",
        "category": "Sedan",
        "price": "40000",
        "url": "https://test.com/car/clear123",
        "html_content": "<div>Clear Test HTML</div>",
        "saved_at": 1234567890.0
    }
    await db_manager.save_listing_to_db(listing_data)
    
    # Verify data exists
    count_before = DemoItem.select().count()
    assert count_before >= 1
    print(f"✅ Items before clear: {count_before}")
    
    # Clear all data
    result = await db_manager.clear_all_data()
    assert result >= 1
    print(f"✅ Cleared {result} items")
    
    # Verify data was cleared
    count_after = DemoItem.select().count()
    assert count_after == 0
    print(f"✅ Items after clear: {count_after}")


def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    # Initialize database
    try:
        initialize_database()
    except Exception:
        pass
    
    # Test basic operations
    count = DemoItem.select().count()
    assert isinstance(count, int)
    print(f"✅ Database connection works: {count} items")


if __name__ == "__main__":
    print("🚀 Starting simple database tests...")
    pytest.main([__file__, "-v", "-s"]) 