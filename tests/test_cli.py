"""
Tests for Demo CLI
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from parsers.parser_demo.cli import DemoCLI
from parsers.parser_demo.cli_db import DemoDatabaseCLI
from parsers.parser_demo.module.config import DemoConfig


class TestDemoCLI:
    """Test DemoCLI class"""

    def setup_method(self):
        """Setup test method"""
        self.cli = DemoCLI()

    def test_cli_initialization(self):
        """Test CLI initialization"""
        assert self.cli.logger is not None
        assert self.cli.config is not None
        assert isinstance(self.cli.config, DemoConfig)

    @pytest.mark.asyncio
    async def test_parse_listings(self):
        """Test parse_listings method"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_listings.return_value = 10

            result = await self.cli.parse_listings()

            assert result == 10
            mock_parser.parse_listings.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_details(self):
        """Test parse_details method"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_details.return_value = 5

            result = await self.cli.parse_details()

            assert result == 5
            mock_parser.parse_details.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_html(self):
        """Test parse_html method"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_html_pages.return_value = 3

            result = await self.cli.parse_html()

            assert result == 3
            mock_parser.parse_html_pages.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_full_pipeline(self):
        """Test run_full_pipeline method"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_listings.return_value = 10
            mock_parser.parse_details.return_value = 5
            mock_parser.parse_html_pages.return_value = 3

            result = await self.cli.run_full_pipeline()

            assert result["listings"] == 10
            assert result["details"] == 5
            assert result["html"] == 3
            mock_parser.parse_listings.assert_called_once()
            mock_parser.parse_details.assert_called_once()
            mock_parser.parse_html_pages.assert_called_once()

    @pytest.mark.asyncio
    async def test_show_pipeline_info(self):
        """Test show_pipeline_info method"""
        with patch('builtins.print') as mock_print:
            await self.cli.show_pipeline_info()
            
            # Verify that print was called (info was displayed)
            assert mock_print.called

    @pytest.mark.asyncio
    async def test_run_tests(self):
        """Test run_tests method"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            result = await self.cli.run_tests()
            
            assert result is True
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_tests_failure(self):
        """Test run_tests method with failure"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            
            result = await self.cli.run_tests()
            
            assert result is False
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_listings_exception(self):
        """Test parse_listings with exception"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser', 
                  side_effect=Exception("Parser error")):
            result = await self.cli.parse_listings()
            
            assert result == 0

    @pytest.mark.asyncio
    async def test_parse_details_exception(self):
        """Test parse_details with exception"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser', 
                  side_effect=Exception("Parser error")):
            result = await self.cli.parse_details()
            
            assert result == 0

    @pytest.mark.asyncio
    async def test_parse_html_exception(self):
        """Test parse_html with exception"""
        with patch('parsers.parser_demo.module.core.parser.DemoParser', 
                  side_effect=Exception("Parser error")):
            result = await self.cli.parse_html()
            
            assert result == 0


class TestDemoDatabaseCLI:
    """Test DemoDatabaseCLI class"""

    def setup_method(self):
        """Setup test method"""
        self.cli = DemoDatabaseCLI()

    def test_cli_initialization(self):
        """Test CLI initialization"""
        assert self.cli.logger is not None
        assert self.cli.db_manager is not None

    @pytest.mark.asyncio
    async def test_show_statistics(self):
        """Test show_statistics method"""
        with patch.object(self.cli.db_manager, 'get_statistics_from_db') as mock_stats, \
             patch.object(self.cli.db_manager, 'get_database_info') as mock_info, \
             patch('builtins.print') as mock_print:
            
            mock_stats.return_value = {
                'total_items': 100,
                'new_items': 20,
                'processed_items': 80,
                'failed_items': 0,
                'success_rate': 80.0,
                'top_brands': [('Toyota', 25), ('Honda', 20)]
            }
            
            mock_info.return_value = {
                'database_type': 'sqlite3_peewee',
                'database_size_mb': 1.5
            }
            
            await self.cli.show_statistics()
            
            # Verify that print was called (statistics were displayed)
            assert mock_print.called

    @pytest.mark.asyncio
    async def test_clear_all_data(self):
        """Test clear_all_data method"""
        with patch.object(self.cli.db_manager, 'clear_all_data') as mock_clear, \
             patch('builtins.print') as mock_print:
            
            mock_clear.return_value = 50
            
            await self.cli.clear_all_data()
            
            mock_clear.assert_called_once()
            assert mock_print.called

    @pytest.mark.asyncio
    async def test_show_database_info(self):
        """Test show_database_info method"""
        with patch.object(self.cli.db_manager, 'get_database_info') as mock_info, \
             patch('builtins.print') as mock_print:
            
            mock_info.return_value = {
                'database_path': '/path/to/demo_parser.db',
                'database_size_bytes': 1024 * 1024,
                'database_size_mb': 1.0,
                'database_type': 'sqlite3_peewee',
                'tables': ['demo_items', 'demo_statistics']
            }
            
            await self.cli.show_database_info()
            
            # Verify that print was called (info was displayed)
            assert mock_print.called

    @pytest.mark.asyncio
    async def test_show_statistics_exception(self):
        """Test show_statistics with exception"""
        with patch.object(self.cli.db_manager, 'get_statistics_from_db', 
                         side_effect=Exception("Stats error")), \
             patch('builtins.print') as mock_print:
            
            await self.cli.show_statistics()
            
            # Should still call print (error message)
            assert mock_print.called

    @pytest.mark.asyncio
    async def test_clear_all_data_exception(self):
        """Test clear_all_data with exception"""
        with patch.object(self.cli.db_manager, 'clear_all_data', 
                         side_effect=Exception("Clear error")), \
             patch('builtins.print') as mock_print:
            
            await self.cli.clear_all_data()
            
            # Should still call print (error message)
            assert mock_print.called


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 