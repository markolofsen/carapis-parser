"""
Tests for Demo Listing Extraction
"""

import pytest
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock
from pathlib import Path

# Add root project to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from ..core.listing_parser.extractor import DemoListingExtractor
from ..core.listing_parser.parser import DemoListingParser
from ..core.listing_parser.saver import DemoListingSaver
from ..config import DemoConfig


class TestDemoListingExtractor:
    """Test DemoListingExtractor class"""

    def setup_method(self):
        """Setup test method"""
        self.extractor = DemoListingExtractor()

    def test_extract_brands_from_html(self):
        """Test extracting brands from HTML"""
        html_content = """
        <div class="brands">
            <a href="/brand/toyota">Toyota</a>
            <a href="/brand/honda">Honda</a>
            <a href="/brand/bmw">BMW</a>
        </div>
        """
        
        brands = self.extractor.extract_brands_from_html(html_content)
        
        assert len(brands) == 3
        assert "Toyota" in brands
        assert "Honda" in brands
        assert "BMW" in brands

    def test_extract_brands_from_html_empty(self):
        """Test extracting brands from empty HTML"""
        html_content = "<div>No brands here</div>"
        
        brands = self.extractor.extract_brands_from_html(html_content)
        
        assert len(brands) == 0

    def test_extract_listing_items_from_html(self):
        """Test extracting listing items from HTML"""
        html_content = """
        <div class="listings">
            <div class="item" data-id="car1">
                <h3>Toyota Camry</h3>
                <span class="price">$25,000</span>
                <span class="mileage">50,000 km</span>
            </div>
            <div class="item" data-id="car2">
                <h3>Honda Accord</h3>
                <span class="price">$22,000</span>
                <span class="mileage">45,000 km</span>
            </div>
        </div>
        """
        
        items = self.extractor.extract_listing_items_from_html(html_content)
        
        assert len(items) == 2
        assert items[0]["id"] == "car1"
        assert items[0]["title"] == "Toyota Camry"
        assert items[0]["price"] == "$25,000"
        assert items[1]["id"] == "car2"
        assert items[1]["title"] == "Honda Accord"

    def test_extract_listing_items_from_html_empty(self):
        """Test extracting listing items from empty HTML"""
        html_content = "<div>No items here</div>"
        
        items = self.extractor.extract_listing_items_from_html(html_content)
        
        assert len(items) == 0

    def test_extract_pagination_info(self):
        """Test extracting pagination information"""
        html_content = """
        <div class="pagination">
            <span class="current">Page 2 of 5</span>
            <a href="/page/1">Previous</a>
            <a href="/page/3">Next</a>
        </div>
        """
        
        pagination = self.extractor.extract_pagination_info(html_content)
        
        assert pagination["current_page"] == 2
        assert pagination["total_pages"] == 5
        assert pagination["has_next"] is True
        assert pagination["has_previous"] is True

    def test_extract_pagination_info_single_page(self):
        """Test extracting pagination info for single page"""
        html_content = "<div>Single page content</div>"
        
        pagination = self.extractor.extract_pagination_info(html_content)
        
        assert pagination["current_page"] == 1
        assert pagination["total_pages"] == 1
        assert pagination["has_next"] is False
        assert pagination["has_previous"] is False


class TestDemoListingParser:
    """Test DemoListingParser class"""

    def setup_method(self):
        """Setup test method"""
        self.config = DemoConfig(max_brands=3, max_pages_per_brand=2)
        self.parser = DemoListingParser(self.config)

    @pytest.mark.asyncio
    async def test_parse_brand_listings(self):
        """Test parsing listings for a specific brand"""
        brand = "Toyota"
        
        with patch.object(self.parser.extractor, 'extract_listing_items_from_html') as mock_extract, \
             patch.object(self.parser.saver, 'save_listing') as mock_save:
            
            mock_extract.return_value = [
                {"id": "car1", "title": "Toyota Camry", "price": "$25,000"},
                {"id": "car2", "title": "Toyota Corolla", "price": "$20,000"}
            ]
            
            result = await self.parser.parse_brand_listings(brand, max_pages=2)
            
            assert result == 2
            assert mock_save.call_count == 2

    @pytest.mark.asyncio
    async def test_parse_brand_listings_empty(self):
        """Test parsing listings for brand with no results"""
        brand = "UnknownBrand"
        
        with patch.object(self.parser.extractor, 'extract_listing_items_from_html') as mock_extract, \
             patch.object(self.parser.saver, 'save_listing') as mock_save:
            
            mock_extract.return_value = []
            
            result = await self.parser.parse_brand_listings(brand, max_pages=2)
            
            assert result == 0
            assert mock_save.call_count == 0

    @pytest.mark.asyncio
    async def test_parse_all_listings(self):
        """Test parsing all listings"""
        with patch.object(self.parser.extractor, 'extract_brands_from_html') as mock_brands, \
             patch.object(self.parser, 'parse_brand_listings') as mock_parse:
            
            mock_brands.return_value = ["Toyota", "Honda", "BMW"]
            mock_parse.return_value = 5
            
            result = await self.parser.parse_all_listings(max_brands=3, max_pages_per_brand=2)
            
            assert result == 15  # 3 brands * 5 items each
            assert mock_parse.call_count == 3

    @pytest.mark.asyncio
    async def test_parse_all_listings_with_limit(self):
        """Test parsing all listings with brand limit"""
        with patch.object(self.parser.extractor, 'extract_brands_from_html') as mock_brands, \
             patch.object(self.parser, 'parse_brand_listings') as mock_parse:
            
            mock_brands.return_value = ["Toyota", "Honda", "BMW", "Audi", "Mercedes"]
            mock_parse.return_value = 5
            
            result = await self.parser.parse_all_listings(max_brands=2, max_pages_per_brand=2)
            
            assert result == 10  # 2 brands * 5 items each
            assert mock_parse.call_count == 2

    @pytest.mark.asyncio
    async def test_parse_all_listings_exception(self):
        """Test parsing all listings with exception"""
        with patch.object(self.parser.extractor, 'extract_brands_from_html', 
                         side_effect=Exception("Extraction error")):
            result = await self.parser.parse_all_listings(max_brands=3, max_pages_per_brand=2)
            
            assert result == 0

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting parser statistics"""
        with patch.object(self.parser.saver, 'get_statistics') as mock_stats:
            mock_stats.return_value = {
                "total_listings": 50,
                "successful_saves": 45,
                "failed_saves": 5
            }
            
            stats = await self.parser.get_statistics()
            
            assert stats["total_listings"] == 50
            assert stats["successful_saves"] == 45
            assert stats["failed_saves"] == 5


class TestDemoListingSaver:
    """Test DemoListingSaver class"""

    def setup_method(self):
        """Setup test method"""
        self.saver = DemoListingSaver()

    @pytest.mark.asyncio
    async def test_save_listing(self):
        """Test saving single listing"""
        listing_data = {
            "id": "demo_123",
            "title": "Demo Car",
            "price": "$25,000",
            "brand": "Toyota",
            "category": "Sedan"
        }
        
        with patch.object(self.saver.db_manager, 'save_listing_to_db') as mock_save:
            mock_save.return_value = True
            
            result = await self.saver.save_listing(listing_data)
            
            assert result is True
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_listings(self):
        """Test saving multiple listings"""
        listings_data = [
            {"id": "demo_123", "title": "Demo Car 1"},
            {"id": "demo_124", "title": "Demo Car 2"}
        ]
        
        with patch.object(self.saver.db_manager, 'save_listings_batch_to_db') as mock_save:
            mock_save.return_value = 2
            
            result = await self.saver.save_listings(listings_data)
            
            assert result == 2
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_listing_exception(self):
        """Test saving listing with exception"""
        listing_data = {"id": "demo_123", "title": "Demo Car"}
        
        with patch.object(self.saver.db_manager, 'save_listing_to_db', 
                         side_effect=Exception("Save error")):
            result = await self.saver.save_listing(listing_data)
            
            assert result is False

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting saver statistics"""
        with patch.object(self.saver.db_manager, 'get_statistics_from_db') as mock_stats:
            mock_stats.return_value = {
                "total_items": 100,
                "new_items": 20,
                "processed_items": 80
            }
            
            stats = await self.saver.get_statistics()
            
            assert stats["total_items"] == 100
            assert stats["new_items"] == 20
            assert stats["processed_items"] == 80


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 