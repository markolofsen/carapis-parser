#!/usr/bin/env python3
"""
Isolated database tests - works with temporarily commented imports
"""

import os
import sys
import json
import asyncio
import pytest
from datetime import datetime

# Add backend/django to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Import database modules (works when problematic imports are commented)
from ..database.models import DemoItem, DemoStatistics, initialize_database, database
from ..database.database import DemoDatabaseManager


@pytest.fixture
def db_manager():
    """Database manager fixture"""
    try:
        initialize_database()
    except Exception:
        # Database already initialized, continue
        pass
    return DemoDatabaseManager()


@pytest.fixture
def sample_listing_data():
    """Sample listing data for testing"""
    return {
        "id": "isolated_test_123",
        "title": "Isolated Test Car",
        "brand": "Toyota",
        "category": "Sedan",
        "price": "25000",
        "url": "https://test.com/car/123",
        "html_content": "<div>Test HTML</div>",
        "saved_at": 1234567890.0
    }


@pytest.fixture
def sample_detail_data():
    """Sample detail data for testing"""
    return {
        "id": "isolated_test_123",  # Same ID as listing
        "title": "Isolated Test Car Detail",
        "specifications": {
            "engine": "2.0L",
            "transmission": "Automatic",
            "fuel_type": "Gasoline"
        },
        "features": ["ABS", "Air Conditioning", "Bluetooth"],
        "html_content": "<div>Test Detail HTML</div>"
    }


@pytest.mark.asyncio
async def test_save_listing_to_db(db_manager, sample_listing_data):
    """Test saving listing to database"""
    print("Testing save listing to database...")
    
    # Save listing
    result = await db_manager.save_listing_to_db(sample_listing_data)
    assert result is True
    print(f"✅ Save result: {result}")
    
    # Verify data was saved
    saved_item = DemoItem.get(DemoItem.item_id == "isolated_test_123")
    assert saved_item.title == "Isolated Test Car"
    assert saved_item.brand == "Toyota"
    assert saved_item.category == "Sedan"
    assert saved_item.status == "processed"
    print(f"✅ Saved item: {saved_item.title} ({saved_item.brand})")
    
    # Check that listing_data was saved as JSON
    saved_listing_data = json.loads(saved_item.listing_data)
    assert saved_listing_data["id"] == "isolated_test_123"
    assert saved_listing_data["title"] == "Isolated Test Car"
    print(f"✅ JSON data verified")


@pytest.mark.asyncio
async def test_save_detail_to_db(db_manager, sample_listing_data, sample_detail_data):
    """Test saving detail to database"""
    print("Testing save detail to database...")
    
    # First save listing
    await db_manager.save_listing_to_db(sample_listing_data)
    
    # Then save detail
    result = await db_manager.save_detail_to_db(sample_detail_data)
    assert result is True
    print(f"✅ Detail save result: {result}")
    
    # Verify detail was saved
    saved_item = DemoItem.get(DemoItem.item_id == "isolated_test_123")
    assert saved_item.detail_html == "<div>Test Detail HTML</div>"
    assert saved_item.status == "processed"
    print(f"✅ Detail HTML saved: {saved_item.detail_html is not None}")
    
    # Check that detail_data was saved as JSON
    saved_detail_data = json.loads(saved_item.detail_data)
    assert saved_detail_data["specifications"]["engine"] == "2.0L"
    assert saved_detail_data["specifications"]["transmission"] == "Automatic"
    print(f"✅ Detail JSON data verified")


@pytest.mark.asyncio
async def test_save_batch_listings(db_manager):
    """Test saving batch of listings"""
    print("Testing batch save...")
    
    listings_data = [
        {
            "id": "isolated_batch_1",
            "title": "Batch Car 1",
            "brand": "Honda",
            "category": "SUV",
            "price": "30000",
            "url": "https://test.com/car/batch1",
            "html_content": "<div>Batch HTML 1</div>",
            "saved_at": 1234567890.0
        },
        {
            "id": "isolated_batch_2",
            "title": "Batch Car 2",
            "brand": "BMW",
            "category": "Sedan",
            "price": "45000",
            "url": "https://test.com/car/batch2",
            "html_content": "<div>Batch HTML 2</div>",
            "saved_at": 1234567890.0
        }
    ]
    
    # Save batch
    result = await db_manager.save_listings_batch_to_db(listings_data)
    assert result == 2
    print(f"✅ Batch save result: {result} items")
    
    # Verify both items were saved
    saved_items = list(DemoItem.select().where(DemoItem.item_id.in_(["isolated_batch_1", "isolated_batch_2"])))
    assert len(saved_items) == 2
    print(f"✅ Verified {len(saved_items)} items saved")
    
    # Check first item
    item1 = next(item for item in saved_items if item.item_id == "isolated_batch_1")
    assert item1.title == "Batch Car 1"
    assert item1.brand == "Honda"
    
    # Check second item
    item2 = next(item for item in saved_items if item.item_id == "isolated_batch_2")
    assert item2.title == "Batch Car 2"
    assert item2.brand == "BMW"


@pytest.mark.asyncio
async def test_get_items_for_details(db_manager, sample_listing_data):
    """Test getting items for detail parsing"""
    print("Testing get items for details...")
    
    # Save some test data
    await db_manager.save_listing_to_db(sample_listing_data)
    
    # Get items for details
    items = await db_manager.get_items_for_details(limit=10)
    
    # Verify items
    assert len(items) >= 1
    item_ids = [item["item_id"] for item in items]
    assert "isolated_test_123" in item_ids
    print(f"✅ Found {len(items)} items for details")


@pytest.mark.asyncio
async def test_get_items_for_html(db_manager, sample_listing_data):
    """Test getting items for HTML parsing"""
    print("Testing get items for HTML...")
    
    # Save some test data
    await db_manager.save_listing_to_db(sample_listing_data)
    
    # Get items for HTML
    items = await db_manager.get_items_for_html(limit=10)
    
    # Verify items
    assert len(items) >= 1
    item_ids = [item["item_id"] for item in items]
    assert "isolated_test_123" in item_ids
    print(f"✅ Found {len(items)} items for HTML")


@pytest.mark.asyncio
async def test_clear_all_data(db_manager, sample_listing_data):
    """Test clearing all data from database"""
    print("Testing clear all data...")
    
    # Save some test data
    await db_manager.save_listing_to_db(sample_listing_data)
    
    # Verify data exists
    count_before = DemoItem.select().count()
    assert count_before >= 1
    print(f"✅ Items before cleanup: {count_before}")
    
    # Clear all data
    result = await db_manager.clear_all_data()
    assert result >= 1
    print(f"✅ Cleared {result} items")
    
    # Verify data was cleared
    count_after = DemoItem.select().count()
    assert count_after == 0
    print(f"✅ Items after cleanup: {count_after}")


@pytest.mark.asyncio
async def test_get_database_info(db_manager):
    """Test getting database information"""
    print("Testing database info...")
    
    info = await db_manager.get_database_info()
    
    # Verify database info
    assert info["database_type"] == "sqlite3_peewee"
    assert info["tables"] == ["demo_items", "demo_statistics"]
    assert "database_path" in info
    assert "database_size_bytes" in info
    assert "database_size_mb" in info
    
    # Check that database path contains demo_parser.db
    assert "demo_parser.db" in info["database_path"]
    print(f"✅ Database info verified: {info['database_type']}")


@pytest.mark.asyncio
async def test_update_existing_item(db_manager, sample_listing_data):
    """Test updating existing item"""
    print("Testing update existing item...")
    
    # Save initial listing
    await db_manager.save_listing_to_db(sample_listing_data)
    
    # Update with new data
    updated_data = {
        "id": "isolated_test_123",  # Same ID
        "title": "Updated Test Car",
        "brand": "Toyota",
        "html_content": "<div>Updated HTML</div>",
        "saved_at": 1234567890.0
    }
    await db_manager.save_listing_to_db(updated_data)
    
    # Verify item was updated, not duplicated
    items = list(DemoItem.select().where(DemoItem.item_id == "isolated_test_123"))
    assert len(items) == 1
    
    updated_item = items[0]
    assert updated_item.title == "Updated Test Car"
    assert updated_item.listing_html == "<div>Updated HTML</div>"
    print(f"✅ Item updated successfully: {updated_item.title}")


def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    try:
        initialize_database()
    except Exception:
        # Database already initialized, continue
        pass
    
    # Test that database is connected
    assert not database.is_closed()
    print("✅ Database connection verified")
    
    # Test basic query
    count = DemoItem.select().count()
    assert isinstance(count, int)
    print(f"✅ Basic query works: {count} items")


def teardown_module(module):
    """Cleanup after all tests"""
    print("Cleaning up test data...")
    try:
        # Clear all test data
        DemoItem.delete().where(
            DemoItem.item_id.in_([
                "isolated_test_123", 
                "isolated_batch_1", 
                "isolated_batch_2"
            ])
        ).execute()
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"⚠️  Warning: Could not cleanup test data: {e}")


if __name__ == "__main__":
    print("🚀 Starting isolated database tests...")
    pytest.main([__file__, "-v", "-s"]) 