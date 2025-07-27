"""
Tests for DemoDatabaseManager - Real database operations
"""

import pytest
import json
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Add root project to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

# Import only the database-related modules
from module.database.models import DemoItem, DemoStatistics, initialize_database, database
from module.database.database import DemoDatabaseManager


class TestDemoDatabaseManager:
    """Test DemoDatabaseManager class with real database operations"""

    def setup_method(self):
        """Setup test method - initialize database"""
        # Initialize database for testing
        initialize_database()
        self.db_manager = DemoDatabaseManager()

    def teardown_method(self):
        """Cleanup after each test"""
        # Clear all data after each test
        try:
            if not database.is_closed():
                database.execute_sql("DELETE FROM demo_items")
                database.execute_sql("DELETE FROM demo_statistics")
                database.commit()
        except Exception as e:
            print(f"Warning: Could not cleanup database: {e}")

    @pytest.mark.asyncio
    async def test_save_listing_to_db(self):
        """Test saving single listing to database"""
        listing_data = {
            "id": "demo_123",
            "title": "Demo Car",
            "url": "https://demo.com/car/123",
            "brand": "Toyota",
            "category": "Sedan",
            "html_content": "<div>Demo HTML</div>",
        }

        # Save listing to database
        result = await self.db_manager.save_listing_to_db(listing_data)
        assert result is True

        # Verify data was saved
        saved_item = DemoItem.get(DemoItem.item_id == "demo_123")
        assert saved_item.title == "Demo Car"
        assert saved_item.brand == "Toyota"
        assert saved_item.category == "Sedan"
        assert saved_item.status == "processed"
        assert saved_item.listing_html == "<div>Demo HTML</div>"

        # Check that listing_data was saved as JSON
        saved_listing_data = json.loads(saved_item.listing_data)
        assert saved_listing_data["id"] == "demo_123"
        assert saved_listing_data["title"] == "Demo Car"

    @pytest.mark.asyncio
    async def test_save_listings_batch_to_db(self):
        """Test saving batch of listings to database"""
        listings_data = [
            {
                "id": "demo_123",
                "title": "Demo Car 1",
                "url": "https://demo.com/car/123",
                "brand": "Toyota",
                "category": "Sedan",
                "html_content": "<div>Demo HTML 1</div>",
            },
            {
                "id": "demo_124",
                "title": "Demo Car 2",
                "url": "https://demo.com/car/124",
                "brand": "Honda",
                "category": "SUV",
                "html_content": "<div>Demo HTML 2</div>",
            },
        ]

        # Save batch to database
        result = await self.db_manager.save_listings_batch_to_db(listings_data)
        assert result == 2

        # Verify both items were saved
        saved_items = list(DemoItem.select().where(DemoItem.item_id.in_(["demo_123", "demo_124"])))
        assert len(saved_items) == 2

        # Check first item
        item1 = next(item for item in saved_items if item.item_id == "demo_123")
        assert item1.title == "Demo Car 1"
        assert item1.brand == "Toyota"

        # Check second item
        item2 = next(item for item in saved_items if item.item_id == "demo_124")
        assert item2.title == "Demo Car 2"
        assert item2.brand == "Honda"

    @pytest.mark.asyncio
    async def test_save_detail_to_db(self):
        """Test saving single detail to database"""
        # First create a listing item
        listing_data = {
            "id": "demo_123",
            "title": "Demo Car",
            "url": "https://demo.com/car/123",
            "brand": "Toyota",
        }
        await self.db_manager.save_listing_to_db(listing_data)

        # Now save detail data
        detail_data = {
            "id": "demo_123",  # Same ID as listing
            "title": "Demo Car Detail",
            "url": "https://demo.com/car/123",
            "specifications": {"engine": "2.0L", "transmission": "Automatic"},
            "description": "Demo description",
            "html_content": "<div>Demo Detail HTML</div>",
        }

        result = await self.db_manager.save_detail_to_db(detail_data)
        assert result is True

        # Verify detail was saved
        saved_item = DemoItem.get(DemoItem.item_id == "demo_123")
        assert saved_item.detail_html == "<div>Demo Detail HTML</div>"
        assert saved_item.status == "processed"

        # Check that detail_data was saved as JSON
        saved_detail_data = json.loads(saved_item.detail_data)
        assert saved_detail_data["specifications"]["engine"] == "2.0L"
        assert saved_detail_data["specifications"]["transmission"] == "Automatic"

    @pytest.mark.asyncio
    async def test_save_details_batch_to_db(self):
        """Test saving batch of details to database"""
        # First create listing items
        listings_data = [
            {"id": "demo_123", "title": "Demo Car 1", "url": "https://demo.com/car/123"},
            {"id": "demo_124", "title": "Demo Car 2", "url": "https://demo.com/car/124"},
        ]
        await self.db_manager.save_listings_batch_to_db(listings_data)

        # Now save detail data
        details_data = [
            {
                "id": "demo_123",
                "title": "Demo Car Detail 1",
                "url": "https://demo.com/car/123",
                "specifications": {"engine": "2.0L"},
                "html_content": "<div>Demo Detail HTML 1</div>",
            },
            {
                "id": "demo_124",
                "title": "Demo Car Detail 2",
                "url": "https://demo.com/car/124",
                "specifications": {"engine": "2.5L"},
                "html_content": "<div>Demo Detail HTML 2</div>",
            },
        ]

        result = await self.db_manager.save_details_batch_to_db(details_data)
        assert result == 2

        # Verify details were saved
        saved_items = list(DemoItem.select().where(DemoItem.item_id.in_(["demo_123", "demo_124"])))
        assert len(saved_items) == 2

        # Check that both have detail data
        for item in saved_items:
            assert item.detail_html is not None
            assert item.detail_data is not None
            detail_data = json.loads(item.detail_data)
            assert "specifications" in detail_data

    @pytest.mark.asyncio
    async def test_save_html_content_to_db(self):
        """Test saving HTML content to database"""
        item_id = "demo_123"
        html_content = "<div>Demo HTML Content</div>"
        url = "https://demo.com/car/123"

        result = await self.db_manager.save_html_content_to_db(item_id, html_content, url)
        assert result is True

        # Verify HTML content was saved
        saved_item = DemoItem.get(DemoItem.item_id == item_id)
        assert saved_item.html_content == html_content
        assert saved_item.url == url
        assert saved_item.status == "processed"

    @pytest.mark.asyncio
    async def test_get_statistics_from_db(self):
        """Test getting statistics from database"""
        # Save some test data first
        listings_data = [
            {"id": "demo_123", "title": "Toyota Car", "brand": "Toyota", "html_content": "<div>HTML</div>"},
            {"id": "demo_124", "title": "Honda Car", "brand": "Honda", "html_content": "<div>HTML</div>"},
            {"id": "demo_125", "title": "Toyota Car 2", "brand": "Toyota", "html_content": "<div>HTML</div>"},
        ]
        await self.db_manager.save_listings_batch_to_db(listings_data)

        # Get statistics
        stats = await self.db_manager.get_statistics_from_db()

        # Verify statistics
        assert stats["total_items"] == 3
        assert stats["processed_items"] == 3
        assert stats["failed_items"] == 0
        assert stats["success_rate"] == 100.0
        assert stats["database_type"] == "sqlite3_peewee"

        # Check top brands
        top_brands = stats.get("top_brands", [])
        assert len(top_brands) > 0
        # Toyota should be first with 2 items
        assert top_brands[0][0] == "Toyota"
        assert top_brands[0][1] == 2

    @pytest.mark.asyncio
    async def test_get_items_for_details(self):
        """Test getting items for detail parsing"""
        # Save some test data
        listings_data = [
            {"id": "demo_123", "title": "Car 1", "brand": "Toyota", "html_content": "<div>HTML</div>"},
            {"id": "demo_124", "title": "Car 2", "brand": "Honda", "html_content": "<div>HTML</div>"},
        ]
        await self.db_manager.save_listings_batch_to_db(listings_data)

        # Get items for details
        items = await self.db_manager.get_items_for_details(limit=10)

        # Verify items
        assert len(items) == 2
        item_ids = [item["item_id"] for item in items]
        assert "demo_123" in item_ids
        assert "demo_124" in item_ids

    @pytest.mark.asyncio
    async def test_get_items_for_html(self):
        """Test getting items for HTML parsing"""
        # Save some test data
        listings_data = [
            {"id": "demo_123", "title": "Car 1", "brand": "Toyota", "html_content": "<div>HTML</div>"},
            {"id": "demo_124", "title": "Car 2", "brand": "Honda", "html_content": "<div>HTML</div>"},
        ]
        await self.db_manager.save_listings_batch_to_db(listings_data)

        # Get items for HTML
        items = await self.db_manager.get_items_for_html(limit=10)

        # Verify items
        assert len(items) == 2
        item_ids = [item["item_id"] for item in items]
        assert "demo_123" in item_ids
        assert "demo_124" in item_ids

    @pytest.mark.asyncio
    async def test_clear_all_data(self):
        """Test clearing all data from database"""
        # Save some test data
        listings_data = [
            {"id": "demo_123", "title": "Car 1", "brand": "Toyota", "html_content": "<div>HTML</div>"},
            {"id": "demo_124", "title": "Car 2", "brand": "Honda", "html_content": "<div>HTML</div>"},
        ]
        await self.db_manager.save_listings_batch_to_db(listings_data)

        # Verify data exists
        count_before = DemoItem.select().count()
        assert count_before == 2

        # Clear all data
        result = await self.db_manager.clear_all_data()
        assert result == 2

        # Verify data was cleared
        count_after = DemoItem.select().count()
        assert count_after == 0

    @pytest.mark.asyncio
    async def test_get_database_info(self):
        """Test getting database information"""
        info = await self.db_manager.get_database_info()

        # Verify database info
        assert info["database_type"] == "sqlite3_peewee"
        assert info["tables"] == ["demo_items", "demo_statistics"]
        assert "database_path" in info
        assert "database_size_bytes" in info
        assert "database_size_mb" in info

        # Check that database path contains demo_parser.db
        assert "demo_parser.db" in info["database_path"]

    @pytest.mark.asyncio
    async def test_update_existing_item(self):
        """Test updating existing item"""
        # Save initial listing
        listing_data = {
            "id": "demo_123",
            "title": "Original Title",
            "brand": "Toyota",
            "html_content": "<div>Original HTML</div>",
        }
        await self.db_manager.save_listing_to_db(listing_data)

        # Update with new data
        updated_data = {
            "id": "demo_123",  # Same ID
            "title": "Updated Title",
            "brand": "Toyota",
            "html_content": "<div>Updated HTML</div>",
        }
        await self.db_manager.save_listing_to_db(updated_data)

        # Verify item was updated, not duplicated
        items = list(DemoItem.select().where(DemoItem.item_id == "demo_123"))
        assert len(items) == 1

        updated_item = items[0]
        assert updated_item.title == "Updated Title"
        assert updated_item.listing_html == "<div>Updated HTML</div>"

    @pytest.mark.asyncio
    async def test_database_connection_and_transactions(self):
        """Test database connection and transaction handling"""
        # Test that database is connected
        assert not database.is_closed()

        # Test transaction
        listing_data = {
            "id": "demo_123",
            "title": "Test Car",
            "brand": "Test Brand",
            "html_content": "<div>Test HTML</div>",
        }

        # Save in transaction
        with database.atomic():
            result = await self.db_manager.save_listing_to_db(listing_data)
            assert result is True

        # Verify data was committed
        saved_item = DemoItem.get(DemoItem.item_id == "demo_123")
        assert saved_item.title == "Test Car"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
