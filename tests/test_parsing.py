"""
Optimized tests for parsing functionality
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from config import DemoConfig


class TestParsingConfig:
    """Test parsing configuration"""

    def test_parsing_config_defaults(self):
        """Test parsing configuration defaults"""
        config = DemoConfig()
        
        # Parsing settings
        assert config.max_brands == 4
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 100
        assert config.max_items_per_category == 10
        assert config.max_items_for_details == 20
        
        # Timing settings
        assert config.listing_delay == 0.1
        assert config.detail_delay == 0.2
        
        # Car-specific settings
        assert config.cars_per_page == 20
        assert config.consecutive_empty_pages_limit == 3

    def test_parsing_config_custom(self):
        """Test custom parsing configuration"""
        config = DemoConfig(
            max_brands=10,
            max_pages_per_brand=5,
            max_urls=200,
            max_items_per_category=15,
            max_items_for_details=30,
            listing_delay=0.5,
            detail_delay=1.0,
            cars_per_page=25,
            consecutive_empty_pages_limit=5
        )
        
        assert config.max_brands == 10
        assert config.max_pages_per_brand == 5
        assert config.max_urls == 200
        assert config.max_items_per_category == 15
        assert config.max_items_for_details == 30
        assert config.listing_delay == 0.5
        assert config.detail_delay == 1.0
        assert config.cars_per_page == 25
        assert config.consecutive_empty_pages_limit == 5

    def test_parsing_config_validation(self):
        """Test parsing configuration validation"""
        # Test valid configurations
        DemoConfig(max_brands=1, max_pages_per_brand=1, max_urls=1)
        DemoConfig(listing_delay=0.0, detail_delay=0.0)
        DemoConfig(cars_per_page=1, consecutive_empty_pages_limit=1)
        
        # Test invalid configurations
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        with pytest.raises(Exception):
            DemoConfig(max_pages_per_brand=0)
        with pytest.raises(Exception):
            DemoConfig(max_urls=0)
        with pytest.raises(Exception):
            DemoConfig(listing_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(detail_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(cars_per_page=0)
        with pytest.raises(Exception):
            DemoConfig(consecutive_empty_pages_limit=0)


class TestParsingIntegration:
    """Test parsing integration"""

    def test_parsing_with_fake_mode(self):
        """Test parsing configuration with fake mode"""
        config = DemoConfig(
            fake_mode=True,
            max_brands=2,
            max_pages_per_brand=1,
            max_workers=2
        )
        
        assert config.fake_mode is True
        assert config.max_brands == 2
        assert config.max_pages_per_brand == 1
        assert config.max_workers == 2

    def test_parsing_with_error_simulation(self):
        """Test parsing configuration with error simulation"""
        config = DemoConfig(
            enable_random_errors=True,
            error_rate=0.2
        )
        
        assert config.enable_random_errors is True
        assert config.error_rate == 0.2

    def test_parsing_with_http_config(self):
        """Test parsing HTTP configuration"""
        config = DemoConfig(
            max_workers=3,
            timeout=30,
            max_retries=2,
            retry_delay=1.5,
            use_smart_manager=True
        )
        
        http_config = config.to_http_config()
        
        assert http_config["num_workers"] == 3
        assert http_config["timeout"] == 30
        assert http_config["max_retries"] == 2
        assert http_config["retry_delay"] == 1.5
        assert http_config["use_smart_manager"] is True

    def test_parsing_comprehensive_config(self):
        """Test comprehensive parsing configuration"""
        config = DemoConfig(
            # Parsing settings
            max_brands=5,
            max_pages_per_brand=3,
            max_urls=150,
            max_items_per_category=12,
            max_items_for_details=25,
            
            # HTTP settings
            max_workers=4,
            timeout=45,
            max_retries=3,
            retry_delay=2.0,
            
            # Timing settings
            listing_delay=0.3,
            detail_delay=0.6,
            
            # Demo settings
            fake_mode=True,
            enable_random_errors=False,
            error_rate=0.0,
            use_smart_manager=True,
            
            # Car settings
            cars_per_page=22,
            consecutive_empty_pages_limit=4
        )
        
        # Test all settings
        assert config.max_brands == 5
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 150
        assert config.max_items_per_category == 12
        assert config.max_items_for_details == 25
        assert config.max_workers == 4
        assert config.timeout == 45
        assert config.max_retries == 3
        assert config.retry_delay == 2.0
        assert config.listing_delay == 0.3
        assert config.detail_delay == 0.6
        assert config.fake_mode is True
        assert config.enable_random_errors is False
        assert config.error_rate == 0.0
        assert config.use_smart_manager is True
        assert config.cars_per_page == 22
        assert config.consecutive_empty_pages_limit == 4

    def test_parsing_config_immutability(self):
        """Test parsing configuration immutability"""
        config = DemoConfig()
        
        with pytest.raises(Exception):
            config.max_brands = 10
        with pytest.raises(Exception):
            config.max_workers = 5
        with pytest.raises(Exception):
            config.fake_mode = False 