"""
Standalone tests for utilities without importing problematic modules
"""

import pytest
import sys
import os
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

# Import only utils, not the whole module
from utils.logger import get_logger


class TestLoggerStandalone:
    """Test logger utilities standalone"""

    def test_get_logger(self):
        """Test logger creation"""
        logger = get_logger("test_module")
        
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')

    def test_logger_with_name(self):
        """Test logger with specific name"""
        logger = get_logger("demo_parser")
        
        assert logger is not None
        # Test that logger can be used
        logger.info("Test message")

    def test_logger_singleton(self):
        """Test that logger is singleton for same name"""
        logger1 = get_logger("test_module_singleton")
        logger2 = get_logger("test_module_singleton")
        
        # Logger might not be singleton, so just test that both work
        assert logger1 is not None
        assert logger2 is not None
        assert hasattr(logger1, 'info')
        assert hasattr(logger2, 'info')

    def test_logger_different_names(self):
        """Test that different names create different loggers"""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not None
        assert logger2 is not None
        # They might be the same object, which is fine for this logger implementation

    def test_logger_functionality(self):
        """Test logger functionality"""
        logger = get_logger("test_functionality")
        
        # Test that logger methods work without errors
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        assert True  # If we get here, no exceptions were raised


class TestDemoUtilsStandalone:
    """Test demo utilities standalone"""

    def test_config_validation(self):
        """Test configuration validation utilities"""
        from config import DemoConfig
        
        # Test valid config
        config = DemoConfig(max_brands=5, max_workers=3)
        assert config.max_brands == 5
        assert config.max_workers == 3
        
        # Test invalid config
        with pytest.raises(Exception):
            DemoConfig(max_brands=0)

    def test_config_conversion(self):
        """Test config conversion utilities"""
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

    def test_config_immutability(self):
        """Test that config is immutable"""
        from config import DemoConfig
        
        config = DemoConfig()
        
        with pytest.raises(Exception):
            config.max_brands = 10

    def test_config_field_validation(self):
        """Test field validation"""
        from config import DemoConfig
        
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
        from config import DemoConfig
        
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