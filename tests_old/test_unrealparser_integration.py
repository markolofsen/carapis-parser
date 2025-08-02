"""
Tests for UnrealParser integration with parser_demo
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from module.config import DemoConfig


class TestUnrealParserIntegration:
    """Test UnrealParser integration"""

    @pytest.fixture
    def demo_config(self):
        """Demo configuration"""
        return DemoConfig(
            max_brands=2,
            max_pages_per_brand=1,
            max_workers=2,
            timeout=30,
            fake_mode=True
        )

    @pytest.mark.asyncio
    async def test_unrealparser_import(self):
        """Test that unrealparser can be imported"""
        try:
            from unreal_parser import UnrealParserManager, UnrealParserConfig
            from unreal_http import HttpWorkerManager
            from unreal_browser import BrowserManager
            from unreal_proxy import ProxyRotationManager
            assert True
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    @pytest.mark.asyncio
    async def test_unrealparser_config_integration(self, demo_config):
        """Test integration with UnrealParserConfig"""
        try:
            from unreal_parser.config import UnrealParserConfig, ProxyStrategy, LogLevel
            
            # Convert demo config to unrealparser config
            unreal_config = UnrealParserConfig(
                data_proxy_api_url="http://localhost:8000",
                data_proxy_resource_name="demo-pool",
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                max_retries=demo_config.max_retries,
                retry_delay=demo_config.retry_delay,
                proxy_strategy=ProxyStrategy.ROTATION,
                log_level=LogLevel.INFO
            )
            
            assert unreal_config.num_workers == demo_config.max_workers
            assert unreal_config.timeout == demo_config.timeout
            assert unreal_config.max_retries == demo_config.max_retries
            assert unreal_config.retry_delay == demo_config.retry_delay
            
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    @pytest.mark.asyncio
    async def test_http_worker_manager_integration(self, demo_config):
        """Test integration with HttpWorkerManager"""
        try:
            from unreal_http.worker_manager import HttpWorkerManager
            from unreal_http.config import HttpClientConfig
            from unreal_http.managers.proxy import ProxyAssigner
            
            # Create HTTP config from demo config
            http_config = HttpClientConfig(
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                max_retries=demo_config.max_retries,
                retry_delay=demo_config.retry_delay,
                service_name="demo_parser"
            )
            
            # Mock proxy assigner
            mock_proxy_assigner = Mock(spec=ProxyAssigner)
            
            # Create worker manager
            worker_manager = HttpWorkerManager(http_config, mock_proxy_assigner)
            
            assert worker_manager.config == http_config
            assert worker_manager.num_workers == demo_config.max_workers
            assert worker_manager.timeout == demo_config.timeout
            
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    @pytest.mark.asyncio
    async def test_browser_manager_integration(self, demo_config):
        """Test integration with BrowserManager"""
        try:
            from unreal_browser.browser_manager import BrowserManager
            
            # Create browser config
            browser_config = {
                "headless": True,
                "timeout": demo_config.timeout,
                "max_instances": demo_config.max_workers,
                "user_agent": "Demo Parser Bot",
                "viewport_width": 1920,
                "viewport_height": 1080
            }
            
            # Create browser manager
            browser_manager = BrowserManager(browser_config)
            
            assert browser_manager.config == browser_config
            assert browser_manager.timeout == demo_config.timeout
            assert browser_manager.max_instances == demo_config.max_workers
            
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    @pytest.mark.asyncio
    async def test_proxy_manager_integration(self, demo_config):
        """Test integration with ProxyRotationManager"""
        try:
            from unreal_proxy.manager import ProxyRotationManager
            from unreal_proxy.config import ProxyConfig
            
            # Create proxy config
            proxy_config = ProxyConfig(
                api_url="http://localhost:8000",
                resource_name="demo-pool",
                timeout=demo_config.timeout,
                max_retries=demo_config.max_retries
            )
            
            # Create proxy manager
            proxy_manager = ProxyRotationManager(proxy_config)
            
            assert proxy_manager.config == proxy_config
            assert proxy_manager.config.timeout == demo_config.timeout
            assert proxy_manager.config.max_retries == demo_config.max_retries
            
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    @pytest.mark.asyncio
    async def test_unrealparser_manager_integration(self, demo_config):
        """Test integration with UnrealParserManager"""
        try:
            from unreal_parser.manager import UnrealParserManager
            from unreal_parser.config import UnrealParserConfig, ProxyStrategy, LogLevel
            
            # Create unrealparser config
            unreal_config = UnrealParserConfig(
                data_proxy_api_url="http://localhost:8000",
                data_proxy_resource_name="demo-pool",
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                max_retries=demo_config.max_retries,
                retry_delay=demo_config.retry_delay,
                proxy_strategy=ProxyStrategy.ROTATION,
                log_level=LogLevel.INFO
            )
            
            # Create unrealparser manager
            parser_manager = UnrealParserManager(unreal_config)
            
            assert parser_manager.config == unreal_config
            assert parser_manager.config.num_workers == demo_config.max_workers
            assert parser_manager.config.timeout == demo_config.timeout
            
        except ImportError as e:
            pytest.skip(f"UnrealParser not available: {e}")

    def test_demo_config_to_unrealparser_mapping(self, demo_config):
        """Test mapping from DemoConfig to UnrealParser config"""
        # Test that demo config can be mapped to unrealparser config
        http_config = demo_config.to_http_config()
        
        assert http_config["service_name"] == "demo_parser"
        assert http_config["num_workers"] == demo_config.max_workers
        assert http_config["timeout"] == demo_config.timeout
        assert http_config["max_retries"] == demo_config.max_retries
        assert http_config["retry_delay"] == demo_config.retry_delay
        assert http_config["use_smart_manager"] == demo_config.use_smart_manager
        assert http_config["fake_mode"] == demo_config.fake_mode 