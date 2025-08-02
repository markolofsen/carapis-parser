"""
Standalone tests for DemoConfig without importing problematic modules
"""

import pytest
import sys
import os
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

# Import only config, not the whole module
from config import DemoConfig


class TestDemoConfigStandalone:
    """Test DemoConfig standalone"""

    def test_default_config(self):
        """Test default configuration"""
        config = DemoConfig()
        
        assert config.max_brands == 4
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 100
        assert config.max_workers == 5
        assert config.timeout == 60
        assert config.fake_mode is True
        assert config.use_smart_manager is True

    def test_custom_config(self):
        """Test custom configuration"""
        config = DemoConfig(
            max_brands=10,
            max_workers=3,
            timeout=30,
            fake_mode=False
        )
        
        assert config.max_brands == 10
        assert config.max_workers == 3
        assert config.timeout == 30
        assert config.fake_mode is False

    def test_validation_positive_integers(self):
        """Test validation of positive integers"""
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        
        with pytest.raises(Exception):
            DemoConfig(max_workers=-1)
        
        with pytest.raises(Exception):
            DemoConfig(timeout=0)

    def test_validation_positive_floats(self):
        """Test validation of positive floats"""
        with pytest.raises(Exception):
            DemoConfig(retry_delay=-1.0)
        
        with pytest.raises(Exception):
            DemoConfig(listing_delay=-0.5)

    def test_validation_error_rate(self):
        """Test validation of error rate"""
        with pytest.raises(Exception):
            DemoConfig(error_rate=1.5)
        
        with pytest.raises(Exception):
            DemoConfig(error_rate=-0.1)

    def test_to_http_config(self):
        """Test conversion to HTTP config"""
        config = DemoConfig(
            max_workers=3,
            timeout=30,
            max_retries=2,
            retry_delay=1.5,
            use_smart_manager=True,
            fake_mode=False
        )
        
        http_config = config.to_http_config()
        
        assert http_config["service_name"] == "demo_parser"
        assert http_config["num_workers"] == 3
        assert http_config["timeout"] == 30
        assert http_config["max_retries"] == 2
        assert http_config["retry_delay"] == 1.5
        assert http_config["use_smart_manager"] is True
        assert http_config["show_progress"] is False
        assert http_config["fake_mode"] is False

    def test_config_immutability(self):
        """Test that config is immutable"""
        config = DemoConfig()
        
        with pytest.raises(Exception):
            config.max_brands = 10

    def test_config_field_validation(self):
        """Test field validation"""
        # Test positive integer validation
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        
        with pytest.raises(Exception):
            DemoConfig(max_workers=-1)
        
        # Test positive float validation
        with pytest.raises(Exception):
            DemoConfig(retry_delay=-1.0)
        
        # Test error rate validation
        with pytest.raises(Exception):
            DemoConfig(error_rate=1.5)
        
        with pytest.raises(Exception):
            DemoConfig(error_rate=-0.1)

    def test_config_defaults(self):
        """Test config default values"""
        config = DemoConfig()
        
        assert config.max_brands == 4
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 100
        assert config.max_workers == 5
        assert config.timeout == 60
        assert config.fake_mode is True
        assert config.use_smart_manager is True
        assert config.verbose_logging is True
        assert config.enable_random_errors is False
        assert config.error_rate == 0.1 