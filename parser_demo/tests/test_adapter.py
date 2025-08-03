"""
Tests for DemoDataServerAdapter
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from ..adapter import DemoDataServerAdapter
from ..config import DemoConfig

# Mock ServiceType for testing
class ServiceType:
    LISTING = "listing"
    DETAIL = "detail"
    HTML_PAGES = "html_pages"


class TestDemoDataServerAdapter:
    """Test Demo data server adapter"""

    @pytest.fixture
    def adapter(self):
        return DemoDataServerAdapter("test_service")

    @pytest.fixture
    def config(self):
        return DemoConfig(max_brands=5, max_pages_per_brand=2)

    @pytest.fixture
    def adapter_with_config(self, config):
        return DemoDataServerAdapter("test_service", config)

    def test_adapter_initialization(self, adapter):
        """Test adapter initialization"""
        assert adapter.config is not None
        assert adapter.parser is not None
        assert adapter.logger is not None

    def test_adapter_with_custom_config(self, config):
        """Test adapter with custom configuration"""
        adapter = DemoDataServerAdapter("test_service", config.__dict__)
        assert adapter.config.max_brands == 5
        assert adapter.config.max_pages_per_brand == 2

    def test_get_adapter_config(self, adapter):
        """Test adapter configuration"""
        config = adapter.get_adapter_config()

        assert config["adapter_type"] == "demo"
        assert config["name"] == "Demo Parser Adapter"
        assert config["description"] == "Adapter for demo parser with async architecture"
        assert config["version"] == "1.0.0"

    def test_get_service_configs(self, adapter):
        """Test service configurations"""
        configs = adapter.get_service_configs()

        # Should have 3 services: listing, detail, html
        assert len(configs) == 3
        
        # Check that we have the expected service types
        service_types = [config.service_type for config in configs]
        assert ServiceType.LISTING in service_types
        assert ServiceType.DETAIL in service_types
        assert ServiceType.HTML_PAGES in service_types
        
        # Check service names
        service_names = [config.name for config in configs]
        assert "Demo Listing Service" in service_names
        assert "Demo Detail Service" in service_names
        assert "Demo HTML Service" in service_names

    @pytest.mark.asyncio
    async def test_execute_task_parse_listings(self, adapter):
        """Test executing parse_listings task"""
        task_data = {"max_brands": 3, "max_pages_per_brand": 2}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_listings') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 10
            mock_stats.return_value = {"total_listings": 10}
            
            result = await adapter.execute_task("parse_listings", task_data)
            
            assert result["success"] is True
            assert result["listings_count"] == 10
            assert "statistics" in result
            assert "timestamp" in result
            
            mock_init.assert_called_once()
            mock_parse.assert_called_once_with(3, 2)

    @pytest.mark.asyncio
    async def test_execute_task_parse_details(self, adapter):
        """Test executing parse_details task"""
        task_data = {"max_urls": 50}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_details') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 25
            mock_stats.return_value = {"total_details": 25}
            
            result = await adapter.execute_task("parse_details", task_data)
            
            assert result["success"] is True
            assert result["details_count"] == 25
            assert "statistics" in result
            assert "timestamp" in result
            
            mock_init.assert_called_once()
            mock_parse.assert_called_once_with(50)

    @pytest.mark.asyncio
    async def test_execute_task_parse_html(self, adapter):
        """Test executing parse_html task"""
        task_data = {"max_urls": 30}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_html_pages') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 15
            mock_stats.return_value = {"total_html": 15}
            
            result = await adapter.execute_task("parse_html", task_data)
            
            assert result["success"] is True
            assert result["html_count"] == 15
            assert "statistics" in result
            assert "timestamp" in result
            
            mock_init.assert_called_once()
            mock_parse.assert_called_once_with(30)

    @pytest.mark.asyncio
    async def test_execute_task_unknown_task(self, adapter):
        """Test executing unknown task"""
        result = await adapter.execute_task("unknown_task", {})
        
        assert result["success"] is False
        assert "Unknown task type: unknown_task" in result["error"]

    @pytest.mark.asyncio
    async def test_execute_task_exception(self, adapter):
        """Test executing task with exception"""
        with patch.object(adapter.parser, 'initialize', side_effect=Exception("Test error")):
            result = await adapter.execute_task("parse_listings", {})
            
            assert result["success"] is False
            assert "Test error" in result["error"]

    def test_get_parser_statistics(self, adapter):
        """Test getting parser statistics"""
        with patch.object(adapter.parser, 'get_statistics') as mock_stats:
            mock_stats.return_value = {
                "total_listings": 100,
                "total_details": 50,
                "failed_brands": ["brand1"],
                "failed_urls": ["url1"]
            }
            
            stats = adapter.get_parser_statistics()
            
            assert "statistics" in stats
            assert "success" in stats

    def test_get_parser_statistics_exception(self, adapter):
        """Test getting statistics with exception"""
        with patch.object(adapter.parser, 'get_statistics', side_effect=Exception("Stats error")):
            stats = adapter.get_parser_statistics()
            
            assert "error" in stats
            assert "Stats error" in stats["error"]

    @pytest.mark.asyncio
    async def test_parse_listings_with_default_config(self, adapter):
        """Test parse_listings with default configuration"""
        task_data = {}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_listings') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 5
            mock_stats.return_value = {"total_listings": 5}
            
            result = await adapter._parse_listings(task_data)
            
            # Should use default config values
            mock_parse.assert_called_once_with(2, 1)  # max_brands=2, max_pages=1

    @pytest.mark.asyncio
    async def test_parse_details_with_default_config(self, adapter):
        """Test parse_details with default configuration"""
        task_data = {}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_details') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 20
            mock_stats.return_value = {"total_details": 20}
            
            result = await adapter._parse_details(task_data)
            
            # Should use default config values
            mock_parse.assert_called_once_with(5)  # max_items_for_details=5

    @pytest.mark.asyncio
    async def test_parse_html_with_default_config(self, adapter):
        """Test parse_html with default configuration"""
        task_data = {}
        
        with patch.object(adapter.parser, 'initialize') as mock_init, \
             patch.object(adapter.parser, 'parse_html_pages') as mock_parse, \
             patch.object(adapter.parser, 'get_statistics') as mock_stats:
            
            mock_init.return_value = None
            mock_parse.return_value = 10
            mock_stats.return_value = {"total_html": 10}
            
            result = await adapter._parse_html(task_data)
            
            # Should use default config values
            mock_parse.assert_called_once_with(5)  # max_items_for_html=5


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 