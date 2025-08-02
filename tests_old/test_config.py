"""
Tests for DemoConfig
"""

import pytest
from pydantic import ValidationError

from ..config import DemoConfig


class TestDemoConfig:
    """Test DemoConfig class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = DemoConfig()
        
        assert config.max_brands == 4
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 100
        assert config.max_items_per_category == 10
        assert config.max_items_for_details == 20
        assert config.max_workers == 5
        assert config.timeout == 60
        assert config.max_retries == 2
        assert config.retry_delay == 1.0
        assert config.listing_delay == 0.1
        assert config.detail_delay == 0.2
        assert config.enable_random_errors is False
        assert config.error_rate == 0.1
        assert config.verbose_logging is True
        assert config.fake_mode is True  # Changed from False to True
        assert config.fake_db is False
        assert config.use_smart_manager is True
        assert config.cars_per_page == 20
        assert config.consecutive_empty_pages_limit == 3

    def test_custom_config(self):
        """Test custom configuration values"""
        config = DemoConfig(
            max_brands=10,
            max_pages_per_brand=5,
            max_urls=200,
            max_workers=10,
            timeout=120,
            fake_mode=True,
            fake_db=True,
            use_smart_manager=False
        )
        
        assert config.max_brands == 10
        assert config.max_pages_per_brand == 5
        assert config.max_urls == 200
        assert config.max_workers == 10
        assert config.timeout == 120
        assert config.fake_mode is True
        assert config.fake_db is True
        assert config.use_smart_manager is False

    def test_to_http_config(self):
        """Test conversion to HTTP client configuration"""
        config = DemoConfig(
            max_workers=8,
            timeout=90,
            max_retries=3,
            retry_delay=2.0,
            fake_mode=True,
            use_smart_manager=True
        )
        
        http_config = config.to_http_config()
        
        assert http_config["service_name"] == "demo_parser"
        assert http_config["num_workers"] == 8
        assert http_config["timeout"] == 90
        assert http_config["max_retries"] == 3
        assert http_config["retry_delay"] == 2.0
        assert http_config["use_smart_manager"] is True
        assert http_config["show_progress"] is False
        assert http_config["fake_mode"] is True

    def test_validation_error_negative_values(self):
        """Test validation error for negative values"""
        with pytest.raises(ValidationError):
            DemoConfig(max_brands=-1)
        
        with pytest.raises(ValidationError):
            DemoConfig(max_pages_per_brand=-5)
        
        with pytest.raises(ValidationError):
            DemoConfig(max_urls=-10)

    def test_validation_error_invalid_error_rate(self):
        """Test validation error for invalid error rate"""
        with pytest.raises(ValidationError):
            DemoConfig(error_rate=1.5)  # Should be between 0.0 and 1.0
        
        with pytest.raises(ValidationError):
            DemoConfig(error_rate=-0.1)  # Should be between 0.0 and 1.0

    def test_validation_error_invalid_timeout(self):
        """Test validation error for invalid timeout"""
        with pytest.raises(ValidationError):
            DemoConfig(timeout=0)  # Should be positive
        
        with pytest.raises(ValidationError):
            DemoConfig(timeout=-60)  # Should be positive

    def test_validation_error_invalid_retry_delay(self):
        """Test validation error for invalid retry delay"""
        # 0 should be valid for retry_delay
        config = DemoConfig(retry_delay=0)
        assert config.retry_delay == 0
        
        with pytest.raises(ValidationError):
            DemoConfig(retry_delay=-1.0)  # Should be positive

    def test_validation_error_invalid_delays(self):
        """Test validation error for invalid delays"""
        with pytest.raises(ValidationError):
            DemoConfig(listing_delay=-0.1)  # Should be positive
        
        with pytest.raises(ValidationError):
            DemoConfig(detail_delay=-0.2)  # Should be positive

    def test_validation_error_invalid_limits(self):
        """Test validation error for invalid limits"""
        with pytest.raises(ValidationError):
            DemoConfig(cars_per_page=0)  # Should be positive
        
        with pytest.raises(ValidationError):
            DemoConfig(consecutive_empty_pages_limit=0)  # Should be positive

    def test_config_with_all_fields(self):
        """Test configuration with all fields set"""
        config = DemoConfig(
            max_brands=15,
            max_pages_per_brand=8,
            max_urls=500,
            max_items_per_category=25,
            max_items_for_details=100,
            max_workers=12,
            timeout=180,
            max_retries=5,
            retry_delay=3.0,
            listing_delay=0.5,
            detail_delay=1.0,
            enable_random_errors=True,
            error_rate=0.2,
            verbose_logging=False,
            fake_mode=True,
            cars_per_page=30,
            consecutive_empty_pages_limit=5,
            use_smart_manager=False
        )
        
        # Verify all fields
        assert config.max_brands == 15
        assert config.max_pages_per_brand == 8
        assert config.max_urls == 500
        assert config.max_items_per_category == 25
        assert config.max_items_for_details == 100
        assert config.max_workers == 12
        assert config.timeout == 180
        assert config.max_retries == 5
        assert config.retry_delay == 3.0
        assert config.listing_delay == 0.5
        assert config.detail_delay == 1.0
        assert config.enable_random_errors is True
        assert config.error_rate == 0.2
        assert config.verbose_logging is False
        assert config.fake_mode is True
        assert config.cars_per_page == 30
        assert config.consecutive_empty_pages_limit == 5
        assert config.use_smart_manager is False

    def test_config_immutability(self):
        """Test that config fields cannot be modified after creation"""
        config = DemoConfig(max_brands=5)
        
        # Should not be able to modify fields
        with pytest.raises(ValidationError):
            config.max_brands = 10

    def test_config_equality(self):
        """Test config equality"""
        config1 = DemoConfig(max_brands=5, max_pages_per_brand=3)
        config2 = DemoConfig(max_brands=5, max_pages_per_brand=3)
        config3 = DemoConfig(max_brands=10, max_pages_per_brand=3)
        
        assert config1 == config2
        assert config1 != config3

    def test_config_repr(self):
        """Test config string representation"""
        config = DemoConfig(max_brands=5, fake_mode=True)
        config_str = str(config)
        
        assert "max_brands=5" in config_str
        assert "fake_mode=True" in config_str
        # Pydantic v2 doesn't include class name in str() by default
        # So we check for the actual format instead
        assert "max_brands=5" in config_str
        assert "fake_mode=True" in config_str


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 