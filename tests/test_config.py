"""
Optimized tests for DemoConfig
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from config import DemoConfig


class TestDemoConfig:
    """Test DemoConfig functionality"""

    def test_default_config(self):
        """Test default configuration values"""
        config = DemoConfig()
        
        # Core settings
        assert config.max_brands == 4
        assert config.max_pages_per_brand == 3
        assert config.max_urls == 100
        assert config.max_workers == 5
        assert config.timeout == 60
        
        # Demo settings
        assert config.fake_mode is True
        assert config.use_smart_manager is True
        assert config.verbose_logging is True
        assert config.enable_random_errors is False
        assert config.error_rate == 0.1

    def test_custom_config(self):
        """Test custom configuration"""
        config = DemoConfig(
            max_brands=10,
            max_workers=3,
            timeout=30,
            fake_mode=False,
            error_rate=0.2
        )
        
        assert config.max_brands == 10
        assert config.max_workers == 3
        assert config.timeout == 30
        assert config.fake_mode is False
        assert config.error_rate == 0.2

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

    def test_all_field_validations(self):
        """Test all field validations in one test"""
        # Valid configs should work
        DemoConfig(max_brands=1, max_workers=1, timeout=1)
        DemoConfig(retry_delay=0.0, listing_delay=0.0)
        DemoConfig(error_rate=0.0)
        DemoConfig(error_rate=1.0)
        
        # Invalid configs should fail
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)
        with pytest.raises(Exception):
            DemoConfig(max_workers=-1)
        with pytest.raises(Exception):
            DemoConfig(retry_delay=-0.1)
        with pytest.raises(Exception):
            DemoConfig(error_rate=1.1) 