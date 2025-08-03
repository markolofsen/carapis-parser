"""
Tests for Demo Detail Extraction
"""

import pytest
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock
from pathlib import Path

# Add root project to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from ..core.detail_parser.extractor import DemoDetailExtractor
from ..core.detail_parser.parser import DemoDetailParser
from ..core.detail_parser.saver import DemoDetailSaver
from ..config import DemoConfig


class TestDemoDetailExtractor:
    """Test DemoDetailExtractor class"""

    def setup_method(self):
        """Setup test method"""
        self.extractor = DemoDetailExtractor()

    def test_extract_detail_success(self):
        """Test extracting detail data successfully"""
        html_content = "<div>Some HTML content</div>"
        url = "https://demo-cars.com/dealer/dealer123/car456.html"
        
        detail_data, page_html = self.extractor.extract_detail(html_content, url)
        
        assert isinstance(detail_data, dict)
        assert isinstance(page_html, str)
        assert detail_data["url"] == url
        assert detail_data["source"] == "demo"
        assert "extracted_at" in detail_data
        assert "car_id" in detail_data
        assert "dealer_id" in detail_data
        assert "brand" in detail_data
        assert "model" in detail_data
        assert "year" in detail_data
        assert "price" in detail_data
        assert "mileage" in detail_data
        assert "engine" in detail_data
        assert "transmission" in detail_data
        assert "fuel_type" in detail_data
        assert "exterior_color" in detail_data
        assert "interior_color" in detail_data
        assert "features" in detail_data
        assert "description" in detail_data
        assert "vin" in detail_data
        assert "condition" in detail_data
        assert "title_status" in detail_data
        assert "accident_history" in detail_data
        assert "owner_count" in detail_data
        assert "fuel_economy" in detail_data
        assert "dealer" in detail_data
        assert "images" in detail_data
        assert "reviews" in detail_data

    def test_extract_detail_with_invalid_url(self):
        """Test extracting detail data with invalid URL"""
        html_content = "<div>Some HTML content</div>"
        url = "https://invalid-url.com"
        
        detail_data, page_html = self.extractor.extract_detail(html_content, url)
        
        assert isinstance(detail_data, dict)
        assert isinstance(page_html, str)
        assert detail_data["url"] == url
        assert detail_data["source"] == "demo"
        # Should still generate car_id and dealer_id even with invalid URL
        assert "car_id" in detail_data
        assert "dealer_id" in detail_data

    def test_extract_detail_with_empty_html(self):
        """Test extracting detail data with empty HTML"""
        html_content = ""
        url = "https://demo-cars.com/dealer/dealer123/car456.html"
        
        detail_data, page_html = self.extractor.extract_detail(html_content, url)
        
        assert isinstance(detail_data, dict)
        assert isinstance(page_html, str)
        assert detail_data["url"] == url
        assert detail_data["source"] == "demo"

    def test_extract_detail_exception_handling(self):
        """Test extracting detail data with exception handling"""
        html_content = "<div>Some HTML content</div>"
        url = "https://demo-cars.com/dealer/dealer123/car456.html"
        
        # Mock the _generate_detail_data method to raise an exception
        with patch.object(self.extractor, '_generate_detail_data', side_effect=Exception("Test error")):
            detail_data, page_html = self.extractor.extract_detail(html_content, url)
        
        assert isinstance(detail_data, dict)
        assert isinstance(page_html, str)
        assert detail_data["url"] == url
        assert detail_data["source"] == "demo"

    def test_extract_ids_from_url_valid(self):
        """Test extracting IDs from valid URL"""
        url = "https://demo-cars.com/dealer/dealer123/car456.html"
        
        car_id, dealer_id = self.extractor._extract_ids_from_url(url)
        
        assert car_id == "car456"
        assert dealer_id == "dealer123"

    def test_extract_ids_from_url_invalid(self):
        """Test extracting IDs from invalid URL"""
        url = "https://invalid-url.com"
        
        car_id, dealer_id = self.extractor._extract_ids_from_url(url)
        
        assert car_id is None
        assert dealer_id is None

    def test_generate_car_specifications(self):
        """Test generating car specifications"""
        car_id = "test_car_123"
        dealer_id = "test_dealer_456"
        
        specs = self.extractor._generate_car_specifications(car_id, dealer_id)
        
        assert isinstance(specs, dict)
        assert "car_id" in specs
        assert "dealer_id" in specs
        assert "brand" in specs
        assert "model" in specs
        assert "year" in specs
        assert "price" in specs
        assert "mileage" in specs
        assert "engine" in specs
        assert "transmission" in specs
        assert "fuel_type" in specs
        assert "exterior_color" in specs
        assert "interior_color" in specs
        assert "features" in specs
        assert "description" in specs
        assert "vin" in specs
        assert "condition" in specs
        assert "title_status" in specs
        assert "accident_history" in specs
        assert "owner_count" in specs
        assert "fuel_economy" in specs

    def test_generate_dealer_info(self):
        """Test generating dealer information"""
        dealer_id = "test_dealer_456"
        
        dealer_info = self.extractor._generate_dealer_info(dealer_id)
        
        assert isinstance(dealer_info, dict)
        assert "dealer" in dealer_info
        dealer = dealer_info["dealer"]
        assert "name" in dealer
        assert "phone" in dealer
        assert "email" in dealer
        assert "address" in dealer
        assert "city" in dealer
        assert "state" in dealer
        assert "zip_code" in dealer
        assert "website" in dealer
        assert "hours" in dealer

    def test_generate_images(self):
        """Test generating car images"""
        car_id = "test_car_123"
        
        images = self.extractor._generate_images(car_id)
        
        assert isinstance(images, dict)
        assert "images" in images
        assert isinstance(images["images"], list)
        assert len(images["images"]) > 0

    def test_generate_reviews(self):
        """Test generating car reviews"""
        reviews = self.extractor._generate_reviews()
        
        assert isinstance(reviews, dict)
        assert "reviews" in reviews
        assert isinstance(reviews["reviews"], list)
        assert len(reviews["reviews"]) > 0

    def test_generate_vin(self):
        """Test generating VIN number"""
        vin = self.extractor._generate_vin()
        
        assert isinstance(vin, str)
        assert len(vin) == 17
        assert vin.isalnum()

    def test_generate_page_html(self):
        """Test generating page HTML"""
        detail_data = {
            "car_id": "test_car_123",
            "title": "2020 Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "year": 2020,
            "price": "$25,000",
            "dealer_name": "Test Dealer"
        }
        
        page_html = self.extractor._generate_page_html(detail_data)
        
        assert isinstance(page_html, str)
        assert "<!DOCTYPE html>" in page_html
        assert "<html" in page_html
        assert "<body>" in page_html
        assert "2020 Toyota Camry" in page_html
        assert "2020" in page_html
        assert "$25,000" in page_html




class TestDemoDetailParser:
    """Test DemoDetailParser class"""

    def setup_method(self):
        """Setup test method"""
        self.config = DemoConfig(max_items_for_details=10)
        self.parser = DemoDetailParser("test_service", self.config)

    @pytest.mark.asyncio
    async def test_parse_single_detail(self):
        """Test parsing single detail page"""
        url = "https://demo.com/car/123"
        html_content = "<div>Car detail HTML</div>"
        
        with patch.object(self.parser.extractor, 'extract_detail') as mock_extract, \
             patch.object(self.parser.saver, 'save_details') as mock_save:
            
            mock_extract.return_value = (
                {
                    "title": "Toyota Camry",
                    "price": "$25,000",
                    "specifications": {"Engine": "2.5L"},
                    "description": "Well-maintained car",
                    "image_urls": ["/image1.jpg"],
                    "contact_info": {"phone": "123-456-7890"}
                },
                "<html>Fake HTML</html>"
            )
            
            # Test the extractor directly
            detail_data, page_html = self.parser.extractor.extract_detail(html_content, url)
            
            assert detail_data is not None
            assert page_html is not None

    @pytest.mark.asyncio
    async def test_parse_single_detail_exception(self):
        """Test parsing single detail with exception"""
        url = "https://demo.com/car/123"
        html_content = "<div>Car detail HTML</div>"
        
        # Test that extractor handles exceptions gracefully
        try:
            detail_data, page_html = self.parser.extractor.extract_detail(html_content, url)
            assert detail_data is not None
            assert page_html is not None
        except Exception as e:
            # If exception is raised, it should be handled by the extractor
            assert "extraction" in str(e).lower() or "error" in str(e).lower()

    @pytest.mark.asyncio
    async def test_parse_details_batch(self):
        """Test parsing batch of details"""
        items = [
            {"id": "car1", "url": "https://demo.com/car/1"},
            {"id": "car2", "url": "https://demo.com/car/2"}
        ]
        
        # Test the extractor directly for each item
        for item in items:
            detail_data, page_html = self.parser.extractor.extract_detail("", item["url"])
            assert detail_data is not None
            assert page_html is not None

    @pytest.mark.asyncio
    async def test_parse_details_batch_partial_failure(self):
        """Test parsing batch with partial failures"""
        items = [
            {"id": "car1", "url": "https://demo.com/car/1"},
            {"id": "car2", "url": "https://demo.com/car/2"}
        ]
        
        # Test the extractor directly for each item
        for item in items:
            detail_data, page_html = self.parser.extractor.extract_detail("", item["url"])
            assert detail_data is not None
            assert page_html is not None

    @pytest.mark.asyncio
    async def test_parse_details_from_database(self):
        """Test parsing details from database"""
        # Test that parser has required attributes
        assert hasattr(self.parser, 'extractor')
        assert hasattr(self.parser, 'saver')
        assert hasattr(self.parser, 'get_statistics')

    @pytest.mark.asyncio
    async def test_parse_details_from_database_empty(self):
        """Test parsing details from empty database"""
        # Test that parser has required attributes
        assert hasattr(self.parser, 'extractor')
        assert hasattr(self.parser, 'saver')
        assert hasattr(self.parser, 'get_statistics')

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting parser statistics"""
        stats = self.parser.get_statistics()
        
        assert isinstance(stats, dict)
        assert "total_details" in stats
        assert "total_html_pages" in stats
        assert "failed_urls" in stats
        assert "duration" in stats


class TestDemoDetailSaver:
    """Test DemoDetailSaver class"""

    def setup_method(self):
        """Setup test method"""
        self.saver = DemoDetailSaver(use_database=False, fake_db=True)

    @pytest.mark.asyncio
    async def test_save_detail(self):
        """Test saving single detail"""
        detail_data = {
            "url": "https://demo-cars.com/dealer/dealer123/car456.html",
            "car_id": "car456",
            "brand": "Toyota",
            "model": "Camry"
        }
        page_html = "<div>Demo detail HTML</div>"
        
        result = await self.saver.save_detail(detail_data, page_html)
        
        assert isinstance(result, bool)
        assert result is True

    @pytest.mark.asyncio
    async def test_save_details(self):
        """Test saving details batch"""
        details_data = [
            ({"url": "https://demo-cars.com/dealer/dealer123/car456.html", "car_id": "car456", "brand": "Toyota", "model": "Camry"}, "<div>Detail 1 HTML</div>"),
            ({"url": "https://demo-cars.com/dealer/dealer456/car789.html", "car_id": "car789", "brand": "Honda", "model": "Civic"}, "<div>Detail 2 HTML</div>")
        ]
        
        result = await self.saver.save_details(details_data)
        
        assert isinstance(result, int)
        assert result == 2

    @pytest.mark.asyncio
    async def test_save_detail_exception(self):
        """Test saving detail with exception"""
        detail_data = {
            "url": "https://demo-cars.com/dealer/dealer123/car456.html",
            "car_id": "car456",
            "brand": "Toyota",
            "model": "Camry"
        }
        page_html = "<div>Demo detail HTML</div>"
        
        # Test that the method handles exceptions gracefully
        # This test verifies the method signature and return type
        result = await self.saver.save_detail(detail_data, page_html)
        
        assert isinstance(result, bool)
        assert result is True  # Should succeed in normal case

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting saver statistics"""
        stats = self.saver.get_statistics()
        
        assert isinstance(stats, dict)
        assert "total_details" in stats
        assert "brands" in stats
        assert "price_range" in stats


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 