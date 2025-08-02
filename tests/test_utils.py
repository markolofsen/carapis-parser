"""
Optimized tests for utilities
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from utils.logger import get_logger


class TestLogger:
    """Test logger utilities"""

    def test_get_logger(self):
        """Test logger creation and basic functionality"""
        logger = get_logger("test_module")
        
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')

    def test_logger_functionality(self):
        """Test that logger methods work without errors"""
        logger = get_logger("test_functionality")
        
        # Test that logger methods work without errors
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        assert True  # If we get here, no exceptions were raised

    def test_logger_with_different_names(self):
        """Test logger with different names"""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not None
        assert logger2 is not None
        
        # Test that both loggers work
        logger1.info("Message from logger1")
        logger2.info("Message from logger2")
        
        assert True  # If we get here, no exceptions were raised

    def test_logger_reuse(self):
        """Test reusing logger with same name"""
        logger1 = get_logger("reuse_test")
        logger2 = get_logger("reuse_test")
        
        assert logger1 is not None
        assert logger2 is not None
        
        # Both should work
        logger1.info("Message 1")
        logger2.info("Message 2")
        
        assert True  # If we get here, no exceptions were raised


class TestConfigIntegration:
    """Test config integration with utilities"""

    def test_config_import(self):
        """Test that config can be imported and used"""
        from config import DemoConfig
        
        config = DemoConfig(max_brands=5, max_workers=3)
        assert config.max_brands == 5
        assert config.max_workers == 3

    def test_config_validation_integration(self):
        """Test config validation integration"""
        from config import DemoConfig
        
        # Test valid config
        config = DemoConfig(max_brands=5, max_workers=3)
        assert config.max_brands == 5
        assert config.max_workers == 3
        
        # Test invalid config
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)

    def test_config_conversion_integration(self):
        """Test config conversion integration"""
        from config import DemoConfig
        
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
        assert http_config["fake_mode"] is False

    def test_config_immutability_integration(self):
        """Test config immutability integration"""
        from config import DemoConfig
        
        config = DemoConfig()
        
        with pytest.raises(Exception):
            config.max_brands = 10 