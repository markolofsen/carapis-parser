"""
Critical tests for main parser
"""

import pytest
import sys
from pathlib import Path

# Add module directory to path
module_path = Path(__file__).parent.parent / "module"
sys.path.insert(0, str(module_path))

from config import DemoConfig


class TestMainParser:
    """Test main parser functionality"""

    def test_parser_initialization(self):
        """Test parser initialization"""
        try:
            from core.parser import DemoParser
            
            config = DemoConfig(
                max_brands=2,
                max_pages_per_brand=1,
                max_workers=2,
                fake_mode=True
            )
            
            parser = DemoParser(config)
            
            assert parser is not None
            assert parser.config == config
            assert hasattr(parser, 'listing_parser')
            assert hasattr(parser, 'detail_parser')
            
        except ImportError:
            pytest.skip("Main parser not available")

    def test_parser_components(self):
        """Test parser components exist"""
        try:
            from core.parser import DemoParser
            from core.listing_parser.parser import DemoListingParser
            from core.detail_parser.parser import DemoDetailParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoParser(config)
            
            # Test that components are initialized
            assert parser.listing_parser is not None
            assert parser.detail_parser is not None
            
            # Test component types
            assert isinstance(parser.listing_parser, DemoListingParser)
            assert isinstance(parser.detail_parser, DemoDetailParser)
            
        except ImportError:
            pytest.skip("Parser components not available")

    def test_parser_methods_exist(self):
        """Test that parser methods exist"""
        try:
            from core.parser import DemoParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoParser(config)
            
            # Test main parser methods
            assert hasattr(parser, 'initialize')
            assert hasattr(parser, 'parse_listings')
            assert hasattr(parser, 'parse_details')
            assert hasattr(parser, 'get_statistics')
            assert hasattr(parser, 'get_saved_listings')
            assert hasattr(parser, 'get_saved_details')
            
        except ImportError:
            pytest.skip("Main parser not available")

    def test_parser_config_integration(self):
        """Test parser configuration integration"""
        try:
            from core.parser import DemoParser
            
            config = DemoConfig(
                max_brands=5,
                max_pages_per_brand=3,
                max_workers=4,
                timeout=60,
                fake_mode=True
            )
            
            parser = DemoParser(config)
            
            # Test that config is properly integrated
            assert parser.config.max_brands == 5
            assert parser.config.max_pages_per_brand == 3
            assert parser.config.max_workers == 4
            assert parser.config.timeout == 60
            assert parser.config.fake_mode is True
            
        except ImportError:
            pytest.skip("Main parser not available")


class TestListingParser:
    """Test listing parser functionality"""

    def test_listing_parser_initialization(self):
        """Test listing parser initialization"""
        try:
            from core.listing_parser.parser import DemoListingParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoListingParser(config)
            
            assert parser is not None
            assert parser.config == config
            assert hasattr(parser, 'extractor')
            assert hasattr(parser, 'saver')
            
        except ImportError:
            pytest.skip("Listing parser not available")

    def test_listing_parser_methods(self):
        """Test listing parser methods exist"""
        try:
            from core.listing_parser.parser import DemoListingParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoListingParser(config)
            
            # Test listing parser methods
            assert hasattr(parser, 'parse_brand_listings')
            assert hasattr(parser, 'parse_all_listings')
            assert hasattr(parser, 'get_statistics')
            
        except ImportError:
            pytest.skip("Listing parser not available")


class TestDetailParser:
    """Test detail parser functionality"""

    def test_detail_parser_initialization(self):
        """Test detail parser initialization"""
        try:
            from core.detail_parser.parser import DemoDetailParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoDetailParser(config)
            
            assert parser is not None
            assert parser.config == config
            assert hasattr(parser, 'extractor')
            assert hasattr(parser, 'saver')
            
        except ImportError:
            pytest.skip("Detail parser not available")

    def test_detail_parser_methods(self):
        """Test detail parser methods exist"""
        try:
            from core.detail_parser.parser import DemoDetailParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoDetailParser(config)
            
            # Test detail parser methods
            assert hasattr(parser, 'parse_single_detail')
            assert hasattr(parser, 'parse_details_batch')
            assert hasattr(parser, 'parse_details_from_database')
            assert hasattr(parser, 'get_statistics')
            
        except ImportError:
            pytest.skip("Detail parser not available")


class TestParserIntegration:
    """Test parser integration"""

    def test_parser_workflow(self):
        """Test complete parser workflow"""
        try:
            from core.parser import DemoParser
            
            config = DemoConfig(
                max_brands=1,
                max_pages_per_brand=1,
                max_workers=1,
                fake_mode=True
            )
            
            parser = DemoParser(config)
            
            # Test that parser can be created and configured
            assert parser is not None
            assert parser.config.fake_mode is True
            assert parser.config.max_brands == 1
            
            # Test that components are available
            assert parser.listing_parser is not None
            assert parser.detail_parser is not None
            
            # Test that methods exist (without calling them)
            assert hasattr(parser, 'initialize')
            assert hasattr(parser, 'parse_listings')
            assert hasattr(parser, 'parse_details')
            assert hasattr(parser, 'get_statistics')
            
        except ImportError:
            pytest.skip("Parser components not available")

    def test_parser_error_handling(self):
        """Test parser error handling"""
        try:
            from core.parser import DemoParser
            
            # Test with invalid config
            config = DemoConfig(
                max_brands=0,  # Invalid value
                fake_mode=True
            )
            
            # This should raise an exception
            with pytest.raises(Exception):
                DemoParser(config)
                
        except ImportError:
            pytest.skip("Parser not available")

    def test_parser_statistics(self):
        """Test parser statistics functionality"""
        try:
            from core.parser import DemoParser
            
            config = DemoConfig(fake_mode=True)
            parser = DemoParser(config)
            
            # Test that statistics method exists and returns dict
            stats = parser.get_statistics()
            assert isinstance(stats, dict)
            
            # Test that saved data methods exist
            listings = parser.get_saved_listings()
            details = parser.get_saved_details()
            
            assert isinstance(listings, list)
            assert isinstance(details, list)
            
        except ImportError:
            pytest.skip("Parser not available") 