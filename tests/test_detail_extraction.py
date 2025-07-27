"""
Tests for Demo Detail Extraction
"""

import pytest
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock
from pathlib import Path

# Add root project to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from parsers.parser_demo.module.core.detail_parser.extractor import DemoDetailExtractor
from parsers.parser_demo.module.core.detail_parser.parser import DemoDetailParser
from parsers.parser_demo.module.core.detail_parser.saver import DemoDetailSaver
from parsers.parser_demo.module.config import DemoConfig


class TestDemoDetailExtractor:
    """Test DemoDetailExtractor class"""

    def setup_method(self):
        """Setup test method"""
        self.extractor = DemoDetailExtractor()

    def test_extract_car_title(self):
        """Test extracting car title from HTML"""
        html_content = """
        <div class="car-detail">
            <h1 class="car-title">Toyota Camry 2020</h1>
            <div class="car-info">...</div>
        </div>
        """
        
        title = self.extractor.extract_car_title(html_content)
        
        assert title == "Toyota Camry 2020"

    def test_extract_car_title_not_found(self):
        """Test extracting car title when not found"""
        html_content = "<div>No title here</div>"
        
        title = self.extractor.extract_car_title(html_content)
        
        assert title is None

    def test_extract_car_price(self):
        """Test extracting car price from HTML"""
        html_content = """
        <div class="car-detail">
            <div class="price">$25,000</div>
            <div class="currency">USD</div>
        </div>
        """
        
        price = self.extractor.extract_car_price(html_content)
        
        assert price == "$25,000"

    def test_extract_car_price_not_found(self):
        """Test extracting car price when not found"""
        html_content = "<div>No price here</div>"
        
        price = self.extractor.extract_car_price(html_content)
        
        assert price is None

    def test_extract_car_specifications(self):
        """Test extracting car specifications from HTML"""
        html_content = """
        <div class="car-specs">
            <div class="spec">
                <span class="label">Engine:</span>
                <span class="value">2.5L 4-Cylinder</span>
            </div>
            <div class="spec">
                <span class="label">Transmission:</span>
                <span class="value">Automatic</span>
            </div>
            <div class="spec">
                <span class="label">Mileage:</span>
                <span class="value">50,000 km</span>
            </div>
        </div>
        """
        
        specs = self.extractor.extract_car_specifications(html_content)
        
        assert len(specs) == 3
        assert specs["Engine"] == "2.5L 4-Cylinder"
        assert specs["Transmission"] == "Automatic"
        assert specs["Mileage"] == "50,000 km"

    def test_extract_car_specifications_empty(self):
        """Test extracting car specifications from empty HTML"""
        html_content = "<div>No specs here</div>"
        
        specs = self.extractor.extract_car_specifications(html_content)
        
        assert len(specs) == 0

    def test_extract_car_description(self):
        """Test extracting car description from HTML"""
        html_content = """
        <div class="car-description">
            <p>This is a well-maintained Toyota Camry with low mileage.</p>
            <p>Perfect for daily commuting and family trips.</p>
        </div>
        """
        
        description = self.extractor.extract_car_description(html_content)
        
        assert "well-maintained Toyota Camry" in description
        assert "Perfect for daily commuting" in description

    def test_extract_car_description_not_found(self):
        """Test extracting car description when not found"""
        html_content = "<div>No description here</div>"
        
        description = self.extractor.extract_car_description(html_content)
        
        assert description is None

    def test_extract_car_images(self):
        """Test extracting car images from HTML"""
        html_content = """
        <div class="car-images">
            <img src="/images/car1.jpg" alt="Car front view">
            <img src="/images/car2.jpg" alt="Car side view">
            <img src="/images/car3.jpg" alt="Car interior">
        </div>
        """
        
        images = self.extractor.extract_car_images(html_content)
        
        assert len(images) == 3
        assert "/images/car1.jpg" in images
        assert "/images/car2.jpg" in images
        assert "/images/car3.jpg" in images

    def test_extract_car_images_empty(self):
        """Test extracting car images from empty HTML"""
        html_content = "<div>No images here</div>"
        
        images = self.extractor.extract_car_images(html_content)
        
        assert len(images) == 0

    def test_extract_contact_info(self):
        """Test extracting contact information from HTML"""
        html_content = """
        <div class="contact-info">
            <div class="phone">+1 (555) 123-4567</div>
            <div class="email">dealer@example.com</div>
            <div class="address">123 Main St, City, State</div>
        </div>
        """
        
        contact = self.extractor.extract_contact_info(html_content)
        
        assert contact["phone"] == "+1 (555) 123-4567"
        assert contact["email"] == "dealer@example.com"
        assert contact["address"] == "123 Main St, City, State"

    def test_extract_contact_info_partial(self):
        """Test extracting partial contact information"""
        html_content = """
        <div class="contact-info">
            <div class="phone">+1 (555) 123-4567</div>
        </div>
        """
        
        contact = self.extractor.extract_contact_info(html_content)
        
        assert contact["phone"] == "+1 (555) 123-4567"
        assert contact.get("email") is None
        assert contact.get("address") is None

    def test_extract_all_details(self):
        """Test extracting all car details from HTML"""
        html_content = """
        <div class="car-detail">
            <h1 class="car-title">Toyota Camry 2020</h1>
            <div class="price">$25,000</div>
            <div class="car-specs">
                <div class="spec">
                    <span class="label">Engine:</span>
                    <span class="value">2.5L 4-Cylinder</span>
                </div>
            </div>
            <div class="car-description">
                <p>Well-maintained Toyota Camry.</p>
            </div>
            <div class="car-images">
                <img src="/images/car1.jpg" alt="Car front view">
            </div>
            <div class="contact-info">
                <div class="phone">+1 (555) 123-4567</div>
            </div>
        </div>
        """
        
        details = self.extractor.extract_all_details(html_content)
        
        assert details["title"] == "Toyota Camry 2020"
        assert details["price"] == "$25,000"
        assert details["specifications"]["Engine"] == "2.5L 4-Cylinder"
        assert "Well-maintained Toyota Camry" in details["description"]
        assert details["image_urls"] == ["/images/car1.jpg"]
        assert details["contact_info"]["phone"] == "+1 (555) 123-4567"


class TestDemoDetailParser:
    """Test DemoDetailParser class"""

    def setup_method(self):
        """Setup test method"""
        self.config = DemoConfig(max_items_for_details=10)
        self.parser = DemoDetailParser(self.config)

    @pytest.mark.asyncio
    async def test_parse_single_detail(self):
        """Test parsing single detail page"""
        url = "https://demo.com/car/123"
        html_content = "<div>Car detail HTML</div>"
        
        with patch.object(self.parser.extractor, 'extract_all_details') as mock_extract, \
             patch.object(self.parser.saver, 'save_detail') as mock_save:
            
            mock_extract.return_value = {
                "title": "Toyota Camry",
                "price": "$25,000",
                "specifications": {"Engine": "2.5L"},
                "description": "Well-maintained car",
                "image_urls": ["/image1.jpg"],
                "contact_info": {"phone": "123-456-7890"}
            }
            
            result = await self.parser.parse_single_detail(url, html_content)
            
            assert result is True
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_single_detail_exception(self):
        """Test parsing single detail with exception"""
        url = "https://demo.com/car/123"
        html_content = "<div>Car detail HTML</div>"
        
        with patch.object(self.parser.extractor, 'extract_all_details', 
                         side_effect=Exception("Extraction error")):
            result = await self.parser.parse_single_detail(url, html_content)
            
            assert result is False

    @pytest.mark.asyncio
    async def test_parse_details_batch(self):
        """Test parsing batch of details"""
        items = [
            {"id": "car1", "url": "https://demo.com/car/1"},
            {"id": "car2", "url": "https://demo.com/car/2"}
        ]
        
        with patch.object(self.parser, 'parse_single_detail') as mock_parse:
            mock_parse.return_value = True
            
            result = await self.parser.parse_details_batch(items)
            
            assert result == 2
            assert mock_parse.call_count == 2

    @pytest.mark.asyncio
    async def test_parse_details_batch_partial_failure(self):
        """Test parsing batch with partial failures"""
        items = [
            {"id": "car1", "url": "https://demo.com/car/1"},
            {"id": "car2", "url": "https://demo.com/car/2"}
        ]
        
        with patch.object(self.parser, 'parse_single_detail') as mock_parse:
            mock_parse.side_effect = [True, False]
            
            result = await self.parser.parse_details_batch(items)
            
            assert result == 1
            assert mock_parse.call_count == 2

    @pytest.mark.asyncio
    async def test_parse_details_from_database(self):
        """Test parsing details from database"""
        with patch.object(self.parser.db_manager, 'get_items_for_details') as mock_get, \
             patch.object(self.parser, 'parse_details_batch') as mock_parse:
            
            mock_get.return_value = [
                {"id": "car1", "url": "https://demo.com/car/1"},
                {"id": "car2", "url": "https://demo.com/car/2"}
            ]
            mock_parse.return_value = 2
            
            result = await self.parser.parse_details_from_database(max_items=10)
            
            assert result == 2
            mock_get.assert_called_once_with(limit=10)
            mock_parse.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_details_from_database_empty(self):
        """Test parsing details from empty database"""
        with patch.object(self.parser.db_manager, 'get_items_for_details') as mock_get:
            mock_get.return_value = []
            
            result = await self.parser.parse_details_from_database(max_items=10)
            
            assert result == 0

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting parser statistics"""
        with patch.object(self.parser.saver, 'get_statistics') as mock_stats:
            mock_stats.return_value = {
                "total_details": 25,
                "successful_saves": 20,
                "failed_saves": 5
            }
            
            stats = await self.parser.get_statistics()
            
            assert stats["total_details"] == 25
            assert stats["successful_saves"] == 20
            assert stats["failed_saves"] == 5


class TestDemoDetailSaver:
    """Test DemoDetailSaver class"""

    def setup_method(self):
        """Setup test method"""
        self.saver = DemoDetailSaver()

    @pytest.mark.asyncio
    async def test_save_detail(self):
        """Test saving single detail"""
        detail_data = {
            "id": "demo_123",
            "title": "Demo Car Detail",
            "price": "$25,000",
            "specifications": {"Engine": "2.5L"},
            "description": "Well-maintained car",
            "image_urls": ["/image1.jpg"],
            "contact_info": {"phone": "123-456-7890"}
        }
        
        with patch.object(self.saver.db_manager, 'save_detail_to_db') as mock_save:
            mock_save.return_value = True
            
            result = await self.saver.save_detail(detail_data)
            
            assert result is True
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_details(self):
        """Test saving multiple details"""
        details_data = [
            {"id": "demo_123", "title": "Demo Car 1"},
            {"id": "demo_124", "title": "Demo Car 2"}
        ]
        
        with patch.object(self.saver.db_manager, 'save_details_batch_to_db') as mock_save:
            mock_save.return_value = 2
            
            result = await self.saver.save_details(details_data)
            
            assert result == 2
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_detail_exception(self):
        """Test saving detail with exception"""
        detail_data = {"id": "demo_123", "title": "Demo Car"}
        
        with patch.object(self.saver.db_manager, 'save_detail_to_db', 
                         side_effect=Exception("Save error")):
            result = await self.saver.save_detail(detail_data)
            
            assert result is False

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """Test getting saver statistics"""
        with patch.object(self.saver.db_manager, 'get_statistics_from_db') as mock_stats:
            mock_stats.return_value = {
                "total_items": 100,
                "items_with_details": 50,
                "items_without_details": 50
            }
            
            stats = await self.saver.get_statistics()
            
            assert stats["total_items"] == 100
            assert stats["items_with_details"] == 50
            assert stats["items_without_details"] == 50


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 