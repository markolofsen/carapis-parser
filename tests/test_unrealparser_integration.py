"""
Optimized tests for UnrealParser integration
"""
import pytest
import sys
from pathlib import Path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))
from config import DemoConfig

# Test UnrealParser integration
class TestUnrealParserIntegration:
    """Test UnrealParser integration with parser_demo"""
    
    def test_unrealparser_import(self):
        """Test that UnrealParser modules can be imported"""
        try:
            from unreal_parser.config import UnrealParserConfig, ProxyStrategy
            from unreal_http.worker_manager import HttpWorkerManager
            from unreal_browser.manager import BrowserManager
            from unreal_proxy import ProxyRotationManager
            from unreal_parser.manager import UnrealParserManager
            print("✅ All UnrealParser modules imported successfully")
        except ImportError as e:
            pytest.skip(f"UnrealParser modules not available: {e}")

    def test_unrealparser_config_integration(self):
        """Test UnrealParser config integration"""
        try:
            from unreal_parser.config import UnrealParserConfig, ProxyStrategy
            
            # Test creating UnrealParser config
            config = UnrealParserConfig(
                num_workers=5,
                timeout=60,
                proxy_strategy=ProxyStrategy.SUCCESS_RATE,  # Use existing strategy
                debug=True
            )
            
            assert config.num_workers == 5
            assert config.timeout == 60
            assert config.proxy_strategy == ProxyStrategy.SUCCESS_RATE
            assert config.debug is True
            
            print("✅ UnrealParser config integration works")
        except ImportError as e:
            pytest.skip(f"UnrealParser config not available: {e}")

    def test_http_worker_manager_integration(self):
        """Test HttpWorkerManager integration"""
        try:
            from unreal_http.worker_manager import HttpWorkerManager
            from unreal_http.config import HttpClientConfig
            
            demo_config = DemoConfig()
            
            # Create HTTP config from demo config
            http_config = HttpClientConfig(
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                service_name="demo_parser"
            )
            
            # Test worker manager creation
            worker_manager = HttpWorkerManager.create_for_service(
                service_name="demo_parser",
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout
            )
            
            # Check that worker manager was created
            assert worker_manager is not None
            assert hasattr(worker_manager, 'config')
            assert worker_manager.config.num_workers == demo_config.max_workers
            
            print("✅ HttpWorkerManager integration works")
        except ImportError as e:
            pytest.skip(f"HttpWorkerManager not available: {e}")

    def test_browser_manager_integration(self):
        """Test BrowserManager integration"""
        try:
            from unreal_browser.manager import BrowserManager
            from unreal_browser.config import BrowserConfig
            
            demo_config = DemoConfig()
            
            # Create browser config
            browser_config = BrowserConfig(
                headless=True,
                timeout=30
            )
            
            # Test browser manager creation
            browser_manager = BrowserManager(browser_config)
            
            # Check that browser manager was created
            assert browser_manager is not None
            assert hasattr(browser_manager, '_config')  # Use _config instead of config
            
            print("✅ BrowserManager integration works")
        except ImportError as e:
            pytest.skip(f"BrowserManager not available: {e}")

    def test_proxy_manager_integration(self):
        """Test ProxyRotationManager integration"""
        try:
            from unreal_proxy import ProxyRotationManager
            
            # Test proxy manager creation
            proxy_manager = ProxyRotationManager(
                api_url="http://localhost:8000",
                api_key=None,
                resource_name="default-pool"
            )
            
            # Check that proxy manager was created
            assert proxy_manager is not None
            
            print("✅ ProxyRotationManager integration works")
        except ImportError as e:
            pytest.skip(f"ProxyRotationManager not available: {e}")

    def test_unrealparser_manager_integration(self):
        """Test UnrealParserManager integration"""
        try:
            from unreal_parser.manager import UnrealParserManager
            from unreal_parser.config import UnrealParserConfig, ProxyStrategy
            
            # Create config
            config = UnrealParserConfig(
                num_workers=3,
                timeout=60,
                proxy_strategy=ProxyStrategy.SUCCESS_RATE,  # Use existing strategy
                debug=True
            )
            
            # Test manager creation
            manager = UnrealParserManager(config)
            
            # Check that manager was created
            assert manager is not None
            assert hasattr(manager, 'config')
            
            print("✅ UnrealParserManager integration works")
        except ImportError as e:
            pytest.skip(f"UnrealParserManager not available: {e}")

    def test_demo_config_to_unrealparser_mapping(self):
        """Test mapping from DemoConfig to UnrealParser configs"""
        try:
            from unreal_parser.config import UnrealParserConfig
            from unreal_http.config import HttpClientConfig
            from unreal_browser.config import BrowserConfig
            
            demo_config = DemoConfig()
            
            # Test mapping to UnrealParser config
            unreal_config = UnrealParserConfig(
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                max_retries=demo_config.max_retries,
                retry_delay=demo_config.retry_delay
            )
            
            assert unreal_config.num_workers == demo_config.max_workers
            assert unreal_config.timeout == demo_config.timeout
            assert unreal_config.max_retries == demo_config.max_retries
            assert unreal_config.retry_delay == demo_config.retry_delay
            
            # Test mapping to HTTP config
            http_config = HttpClientConfig(
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout,
                service_name="demo_parser"
            )
            
            assert http_config.num_workers == demo_config.max_workers
            assert http_config.timeout == demo_config.timeout
            
            # Test mapping to Browser config
            browser_config = BrowserConfig(
                headless=True,
                timeout=30
            )
            
            assert browser_config.headless is True
            assert browser_config.timeout == 30
            
            print("✅ DemoConfig to UnrealParser mapping works")
        except ImportError as e:
            pytest.skip(f"UnrealParser configs not available: {e}")

    def test_all_integrations(self):
        """Test all integration points together"""
        try:
            from unreal_parser.config import UnrealParserConfig
            from unreal_http.worker_manager import HttpWorkerManager
            from unreal_browser.manager import BrowserManager
            from unreal_proxy import ProxyRotationManager
            
            demo_config = DemoConfig()
            
            # Test all components can be created together
            unreal_config = UnrealParserConfig(
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout
            )
            
            worker_manager = HttpWorkerManager.create_for_service(
                service_name="demo_parser",
                num_workers=demo_config.max_workers,
                timeout=demo_config.timeout
            )
            
            proxy_manager = ProxyRotationManager(
                api_url="http://localhost:8000",
                api_key=None,
                resource_name="default-pool"
            )
            
            # All components should be created successfully
            assert unreal_config is not None
            assert worker_manager is not None
            assert proxy_manager is not None
            
            print("✅ All UnrealParser integrations work together")
        except ImportError as e:
            pytest.skip(f"UnrealParser components not available: {e}") 