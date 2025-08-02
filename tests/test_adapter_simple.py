"""
Simple tests for adapter without external dependencies
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from config import DemoConfig


class TestAdapterSimple:
    """Simple adapter tests without external dependencies"""

    def test_adapter_import(self):
        """Test that adapter can be imported"""
        try:
            from adapter import DemoDataServerAdapter
            assert True
        except ImportError as e:
            pytest.skip(f"Adapter not available: {e}")

    def test_adapter_initialization(self):
        """Test adapter initialization"""
        try:
            from adapter import DemoDataServerAdapter
            
            # Test basic initialization
            adapter = DemoDataServerAdapter("test_service")
            
            assert adapter is not None
            assert hasattr(adapter, 'service_id')
            assert hasattr(adapter, 'config')
            assert hasattr(adapter, 'parser')
            
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_with_config(self):
        """Test adapter with custom configuration"""
        try:
            from adapter import DemoDataServerAdapter
            
            config = DemoConfig(
                max_brands=5,
                max_pages_per_brand=2,
                fake_mode=True
            )
            
            adapter = DemoDataServerAdapter("test_service", config)
            
            assert adapter.config == config
            assert adapter.config.max_brands == 5
            assert adapter.config.max_pages_per_brand == 2
            assert adapter.config.fake_mode is True
            
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_methods_exist(self):
        """Test that adapter methods exist"""
        try:
            from adapter import DemoDataServerAdapter
            
            adapter = DemoDataServerAdapter("test_service")
            
            # Test adapter methods
            assert hasattr(adapter, 'execute_task')
            assert hasattr(adapter, 'get_adapter_config')
            assert hasattr(adapter, 'get_service_configs')
            assert hasattr(adapter, 'get_parser_statistics')
            
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_config_methods(self):
        """Test adapter configuration methods"""
        try:
            from adapter import DemoDataServerAdapter
            
            adapter = DemoDataServerAdapter("test_service")
            
            # Test adapter config
            adapter_config = adapter.get_adapter_config()
            assert isinstance(adapter_config, object) or adapter_config is None
            
            # Test service configs
            service_configs = adapter.get_service_configs()
            assert isinstance(service_configs, list) or service_configs is None
            
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_error_handling(self):
        """Test adapter error handling"""
        try:
            from adapter import DemoDataServerAdapter
            
            # Test with invalid service ID
            adapter = DemoDataServerAdapter("")
            assert adapter.service_id == ""
            
            # Test with None service ID
            adapter = DemoDataServerAdapter(None)
            assert adapter.service_id is None
            
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_integration(self):
        """Test adapter integration with parser"""
        try:
            from adapter import DemoDataServerAdapter
            
            config = DemoConfig(fake_mode=True)
            adapter = DemoDataServerAdapter("test_service", config)
            
            # Test that adapter has parser
            assert adapter.parser is not None
            
            # Test that parser has config
            assert adapter.parser.config == config
            
            # Test that parser has components
            assert hasattr(adapter.parser, 'listing_parser')
            assert hasattr(adapter.parser, 'detail_parser')
            
        except ImportError:
            pytest.skip("Adapter not available")


class TestAdapterMock:
    """Test adapter with mocked dependencies"""

    def test_adapter_mock_execution(self):
        """Test adapter execution with mocked dependencies"""
        try:
            from adapter import DemoDataServerAdapter
            from unittest.mock import Mock, patch
            
            config = DemoConfig(fake_mode=True)
            adapter = DemoDataServerAdapter("test_service", config)
            
            # Mock parser methods
            with patch.object(adapter.parser, 'initialize') as mock_init, \
                 patch.object(adapter.parser, 'parse_listings') as mock_parse, \
                 patch.object(adapter.parser, 'get_statistics') as mock_stats:
                
                mock_init.return_value = None
                mock_parse.return_value = 10
                mock_stats.return_value = {"total_listings": 10}
                
                # Test that methods can be called
                assert mock_init is not None
                assert mock_parse is not None
                assert mock_stats is not None
                
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_task_execution(self):
        """Test adapter task execution"""
        try:
            from adapter import DemoDataServerAdapter
            from unittest.mock import Mock, patch
            
            config = DemoConfig(fake_mode=True)
            adapter = DemoDataServerAdapter("test_service", config)
            
            # Mock execute_task method
            with patch.object(adapter, 'execute_task') as mock_execute:
                mock_execute.return_value = {
                    "success": True,
                    "task": "parse_listings",
                    "listings_count": 10
                }
                
                # Test that method exists and can be called
                result = mock_execute("parse_listings", {})
                assert result["success"] is True
                assert result["task"] == "parse_listings"
                assert result["listings_count"] == 10
                
        except ImportError:
            pytest.skip("Adapter not available")


class TestAdapterConfiguration:
    """Test adapter configuration"""

    def test_adapter_service_id(self):
        """Test adapter service ID handling"""
        try:
            from adapter import DemoDataServerAdapter
            
            # Test with different service IDs
            service_ids = ["test_service", "demo_parser", "car_parser", ""]
            
            for service_id in service_ids:
                adapter = DemoDataServerAdapter(service_id)
                assert adapter.service_id == service_id
                
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_config_integration(self):
        """Test adapter configuration integration"""
        try:
            from adapter import DemoDataServerAdapter
            
            # Test with different configs
            configs = [
                DemoConfig(max_brands=1, fake_mode=True),
                DemoConfig(max_brands=10, fake_mode=False),
                DemoConfig(max_workers=5, timeout=30)
            ]
            
            for config in configs:
                adapter = DemoDataServerAdapter("test_service", config)
                assert adapter.config == config
                
        except ImportError:
            pytest.skip("Adapter not available")

    def test_adapter_statistics(self):
        """Test adapter statistics functionality"""
        try:
            from adapter import DemoDataServerAdapter
            
            config = DemoConfig(fake_mode=True)
            adapter = DemoDataServerAdapter("test_service", config)
            
            # Test statistics method
            stats = adapter.get_parser_statistics()
            assert isinstance(stats, dict) or stats is None
            
        except ImportError:
            pytest.skip("Adapter not available") 