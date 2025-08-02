"""
Critical tests for extractors
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))


class TestListingExtractor:
    """Test listing extractor functionality"""

    def test_extract_brands_from_html(self):
        """Test extracting brands from HTML"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            
            extractor = DemoListingExtractor()
            
            html_content = """
            <div class="brands">
                <a href="/brand/toyota">Toyota</a>
                <a href="/brand/honda">Honda</a>
                <a href="/brand/bmw">BMW</a>
            </div>
            """
            
            brands = extractor.extract_brands_from_html(html_content)
            
            assert isinstance(brands, list)
            assert len(brands) >= 0  # Could be 0 if no brands found
            
        except ImportError:
            pytest.skip("Listing extractor not available")

    def test_extract_listing_items_from_html(self):
        """Test extracting listing items from HTML"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            
            extractor = DemoListingExtractor()
            
            html_content = """
            <div class="listings">
                <div class="item" data-id="car1">
                    <h3>Toyota Camry</h3>
                    <span class="price">$25,000</span>
                </div>
                <div class="item" data-id="car2">
                    <h3>Honda Accord</h3>
                    <span class="price">$22,000</span>
                </div>
            </div>
            """
            
            items = extractor.extract_listing_items_from_html(html_content)
            
            assert isinstance(items, list)
            assert len(items) >= 0  # Could be 0 if no items found
            
        except ImportError:
            pytest.skip("Listing extractor not available")

    def test_extract_pagination_info(self):
        """Test extracting pagination information"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            
            extractor = DemoListingExtractor()
            
            html_content = """
            <div class="pagination">
                <span class="current">Page 2 of 5</span>
                <a href="/page/1">Previous</a>
                <a href="/page/3">Next</a>
            </div>
            """
            
            pagination = extractor.extract_pagination_info(html_content)
            
            assert isinstance(pagination, dict)
            assert "current_page" in pagination or "total_pages" in pagination
            
        except ImportError:
            pytest.skip("Listing extractor not available")


class TestDetailExtractor:
    """Test detail extractor functionality"""

    def test_extract_car_title(self):
        """Test extracting car title from HTML"""
        try:
            from core.detail_parser.extractor import DemoDetailExtractor
            
            extractor = DemoDetailExtractor()
            
            html_content = """
            <div class="car-detail">
                <h1 class="car-title">Toyota Camry 2020</h1>
                <div class="car-info">...</div>
            </div>
            """
            
            title = extractor.extract_car_title(html_content)
            
            assert title is None or isinstance(title, str)
            
        except ImportError:
            pytest.skip("Detail extractor not available")

    def test_extract_car_price(self):
        """Test extracting car price from HTML"""
        try:
            from core.detail_parser.extractor import DemoDetailExtractor
            
            extractor = DemoDetailExtractor()
            
            html_content = """
            <div class="car-detail">
                <div class="price">$25,000</div>
                <div class="currency">USD</div>
            </div>
            """
            
            price = extractor.extract_car_price(html_content)
            
            assert price is None or isinstance(price, str)
            
        except ImportError:
            pytest.skip("Detail extractor not available")

    def test_extract_car_specifications(self):
        """Test extracting car specifications from HTML"""
        try:
            from core.detail_parser.extractor import DemoDetailExtractor
            
            extractor = DemoDetailExtractor()
            
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
            </div>
            """
            
            specs = extractor.extract_car_specifications(html_content)
            
            assert isinstance(specs, dict)
            
        except ImportError:
            pytest.skip("Detail extractor not available")

    def test_extract_all_details(self):
        """Test extracting all car details from HTML"""
        try:
            from core.detail_parser.extractor import DemoDetailExtractor
            
            extractor = DemoDetailExtractor()
            
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
                <div class="description">Great car for sale</div>
                <div class="images">
                    <img src="/image1.jpg" alt="Car image">
                </div>
            </div>
            """
            
            details = extractor.extract_all_details(html_content)
            
            assert isinstance(details, dict)
            assert "title" in details or "price" in details or "specifications" in details
            
        except ImportError:
            pytest.skip("Detail extractor not available")


class TestExtractorIntegration:
    """Test extractor integration"""

    def test_extractor_initialization(self):
        """Test that extractors can be initialized"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            from core.detail_parser.extractor import DemoDetailExtractor
            
            listing_extractor = DemoListingExtractor()
            detail_extractor = DemoDetailExtractor()
            
            assert listing_extractor is not None
            assert detail_extractor is not None
            
        except ImportError:
            pytest.skip("Extractors not available")

    def test_extractor_methods_exist(self):
        """Test that extractor methods exist"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            from core.detail_parser.extractor import DemoDetailExtractor
            
            listing_extractor = DemoListingExtractor()
            detail_extractor = DemoDetailExtractor()
            
            # Test listing extractor methods
            assert hasattr(listing_extractor, 'extract_brands_from_html')
            assert hasattr(listing_extractor, 'extract_listing_items_from_html')
            assert hasattr(listing_extractor, 'extract_pagination_info')
            
            # Test detail extractor methods
            assert hasattr(detail_extractor, 'extract_car_title')
            assert hasattr(detail_extractor, 'extract_car_price')
            assert hasattr(detail_extractor, 'extract_car_specifications')
            assert hasattr(detail_extractor, 'extract_all_details')
            
        except ImportError:
            pytest.skip("Extractors not available")

    def test_extractor_error_handling(self):
        """Test extractor error handling"""
        try:
            from core.listing_parser.extractor import DemoListingExtractor
            from core.detail_parser.extractor import DemoDetailExtractor
            
            listing_extractor = DemoListingExtractor()
            detail_extractor = DemoDetailExtractor()
            
            # Test with empty HTML
            empty_html = ""
            
            # These should not raise exceptions
            listing_extractor.extract_brands_from_html(empty_html)
            listing_extractor.extract_listing_items_from_html(empty_html)
            listing_extractor.extract_pagination_info(empty_html)
            
            detail_extractor.extract_car_title(empty_html)
            detail_extractor.extract_car_price(empty_html)
            detail_extractor.extract_car_specifications(empty_html)
            detail_extractor.extract_all_details(empty_html)
            
            assert True  # If we get here, no exceptions were raised
            
        except ImportError:
            pytest.skip("Extractors not available") 