"""
Comprehensive coverage tests for parser_demo
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from config import DemoConfig


class TestCoverage:
    """Comprehensive coverage tests"""

    def test_all_config_fields(self):
        """Test all configuration fields"""
        config = DemoConfig()
        
        # Core parsing settings
        assert hasattr(config, 'max_brands')
        assert hasattr(config, 'max_pages_per_brand')
        assert hasattr(config, 'max_urls')
        assert hasattr(config, 'max_items_per_category')
        assert hasattr(config, 'max_items_for_details')
        
        # HTTP client settings
        assert hasattr(config, 'max_workers')
        assert hasattr(config, 'timeout')
        assert hasattr(config, 'max_retries')
        assert hasattr(config, 'retry_delay')
        
        # Timing settings
        assert hasattr(config, 'listing_delay')
        assert hasattr(config, 'detail_delay')
        
        # Demo data settings
        assert hasattr(config, 'enable_random_errors')
        assert hasattr(config, 'error_rate')
        
        # Logging settings
        assert hasattr(config, 'verbose_logging')
        
        # Testing settings
        assert hasattr(config, 'fake_mode')
        assert hasattr(config, 'fake_db')
        
        # HTTP client settings
        assert hasattr(config, 'use_smart_manager')
        
        # Car-specific settings
        assert hasattr(config, 'cars_per_page')
        assert hasattr(config, 'consecutive_empty_pages_limit')

    def test_all_config_methods(self):
        """Test all configuration methods"""
        config = DemoConfig()
        
        # Test to_http_config method
        http_config = config.to_http_config()
        assert isinstance(http_config, dict)
        assert "service_name" in http_config
        assert "num_workers" in http_config
        assert "timeout" in http_config
        assert "max_retries" in http_config
        assert "retry_delay" in http_config
        assert "use_smart_manager" in http_config
        assert "show_progress" in http_config
        assert "fake_mode" in http_config

    def test_config_edge_cases(self):
        """Test configuration edge cases"""
        # Test minimum valid values
        config = DemoConfig(
            max_brands=1,
            max_pages_per_brand=1,
            max_urls=1,
            max_items_per_category=1,
            max_items_for_details=1,
            max_workers=1,
            timeout=1,
            max_retries=1,
            retry_delay=0.0,
            listing_delay=0.0,
            detail_delay=0.0,
            error_rate=0.0,
            cars_per_page=1,
            consecutive_empty_pages_limit=1
        )
        
        assert config.max_brands == 1
        assert config.max_pages_per_brand == 1
        assert config.max_urls == 1
        assert config.max_workers == 1
        assert config.timeout == 1
        assert config.max_retries == 1
        assert config.retry_delay == 0.0
        assert config.listing_delay == 0.0
        assert config.detail_delay == 0.0
        assert config.error_rate == 0.0
        assert config.cars_per_page == 1
        assert config.consecutive_empty_pages_limit == 1

    def test_config_maximum_values(self):
        """Test configuration maximum values"""
        # Test maximum valid values
        config = DemoConfig(
            max_brands=1000,
            max_pages_per_brand=1000,
            max_urls=10000,
            max_items_per_category=1000,
            max_items_for_details=1000,
            max_workers=100,
            timeout=3600,
            max_retries=10,
            retry_delay=60.0,
            listing_delay=10.0,
            detail_delay=10.0,
            error_rate=1.0,
            cars_per_page=100,
            consecutive_empty_pages_limit=100
        )
        
        assert config.max_brands == 1000
        assert config.max_pages_per_brand == 1000
        assert config.max_urls == 10000
        assert config.max_items_per_category == 1000
        assert config.max_items_for_details == 1000
        assert config.max_workers == 100
        assert config.timeout == 3600
        assert config.max_retries == 10
        assert config.retry_delay == 60.0
        assert config.listing_delay == 10.0
        assert config.detail_delay == 10.0
        assert config.error_rate == 1.0
        assert config.cars_per_page == 100
        assert config.consecutive_empty_pages_limit == 100

    def test_config_boolean_fields(self):
        """Test configuration boolean fields"""
        config = DemoConfig(
            enable_random_errors=True,
            verbose_logging=False,
            fake_mode=True,
            fake_db=True,
            use_smart_manager=False
        )
        
        assert config.enable_random_errors is True
        assert config.verbose_logging is False
        assert config.fake_mode is True
        assert config.fake_db is True
        assert config.use_smart_manager is False

    def test_config_validation_coverage(self):
        """Test configuration validation coverage"""
        # Test all validation rules
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        with pytest.raises(Exception):
            DemoConfig(max_pages_per_brand=0)
        with pytest.raises(Exception):
            DemoConfig(max_urls=0)
        with pytest.raises(Exception):
            DemoConfig(max_items_per_category=0)
        with pytest.raises(Exception):
            DemoConfig(max_items_for_details=0)
        with pytest.raises(Exception):
            DemoConfig(max_workers=0)
        with pytest.raises(Exception):
            DemoConfig(timeout=0)
        with pytest.raises(Exception):
            DemoConfig(max_retries=0)
        with pytest.raises(Exception):
            DemoConfig(retry_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(listing_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(detail_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(error_rate=-0.1)
        with pytest.raises(Exception):
            DemoConfig(error_rate=1.1)
        with pytest.raises(Exception):
            DemoConfig(cars_per_page=0)
        with pytest.raises(Exception):
            DemoConfig(consecutive_empty_pages_limit=0)

    def test_config_immutability_coverage(self):
        """Test configuration immutability coverage"""
        config = DemoConfig()
        
        # Test that all fields are immutable
        with pytest.raises(Exception):
            config.max_brands = 10
        with pytest.raises(Exception):
            config.max_pages_per_brand = 10
        with pytest.raises(Exception):
            config.max_urls = 10
        with pytest.raises(Exception):
            config.max_items_per_category = 10
        with pytest.raises(Exception):
            config.max_items_for_details = 10
        with pytest.raises(Exception):
            config.max_workers = 10
        with pytest.raises(Exception):
            config.timeout = 10
        with pytest.raises(Exception):
            config.max_retries = 10
        with pytest.raises(Exception):
            config.retry_delay = 1.0
        with pytest.raises(Exception):
            config.listing_delay = 1.0
        with pytest.raises(Exception):
            config.detail_delay = 1.0
        with pytest.raises(Exception):
            config.enable_random_errors = True
        with pytest.raises(Exception):
            config.error_rate = 0.5
        with pytest.raises(Exception):
            config.verbose_logging = True
        with pytest.raises(Exception):
            config.fake_mode = False
        with pytest.raises(Exception):
            config.fake_db = True
        with pytest.raises(Exception):
            config.use_smart_manager = True
        with pytest.raises(Exception):
            config.cars_per_page = 10
        with pytest.raises(Exception):
            config.consecutive_empty_pages_limit = 10

    def test_http_config_coverage(self):
        """Test HTTP configuration coverage"""
        config = DemoConfig(
            max_workers=5,
            timeout=60,
            max_retries=3,
            retry_delay=2.0,
            use_smart_manager=True,
            fake_mode=False
        )
        
        http_config = config.to_http_config()
        
        # Test all HTTP config fields
        assert http_config["service_name"] == "demo_parser"
        assert http_config["num_workers"] == 5
        assert http_config["timeout"] == 60
        assert http_config["max_retries"] == 3
        assert http_config["retry_delay"] == 2.0
        assert http_config["use_smart_manager"] is True
        assert http_config["show_progress"] is False
        assert http_config["fake_mode"] is False

    def test_comprehensive_coverage(self):
        """Test comprehensive coverage of all functionality"""
        # Test default configuration
        default_config = DemoConfig()
        assert default_config.max_brands == 4
        assert default_config.fake_mode is True
        
        # Test custom configuration
        custom_config = DemoConfig(
            max_brands=10,
            fake_mode=False,
            enable_random_errors=True,
            error_rate=0.5
        )
        assert custom_config.max_brands == 10
        assert custom_config.fake_mode is False
        assert custom_config.enable_random_errors is True
        assert custom_config.error_rate == 0.5
        
        # Test HTTP configuration conversion
        http_config = custom_config.to_http_config()
        assert http_config["service_name"] == "demo_parser"
        assert http_config["num_workers"] == custom_config.max_workers
        assert http_config["timeout"] == custom_config.timeout
        assert http_config["fake_mode"] == custom_config.fake_mode
        
        # Test validation
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        
        # Test immutability
        with pytest.raises(Exception):
            custom_config.max_brands = 20 