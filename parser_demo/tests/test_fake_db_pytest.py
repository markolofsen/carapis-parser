"""
Pytest tests for fake_db functionality
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestFakeDB:
    """Test fake_db functionality"""

    def test_fake_db_default(self):
        """Test that fake_db defaults to False"""
        from ..config import DemoConfig
        
        config = DemoConfig()
        assert config.fake_db is False

    def test_fake_db_enabled(self):
        """Test that fake_db can be enabled"""
        from ..config import DemoConfig
        
        config = DemoConfig(fake_db=True)
        assert config.fake_db is True

    def test_fake_mode_and_fake_db_combination(self):
        """Test combination of fake_mode and fake_db"""
        from ..config import DemoConfig
        
        # Both enabled
        config = DemoConfig(fake_mode=True, fake_db=True)
        assert config.fake_mode is True
        assert config.fake_db is True

        # Only fake_mode enabled
        config = DemoConfig(fake_mode=True, fake_db=False)
        assert config.fake_mode is True
        assert config.fake_db is False

        # Only fake_db enabled
        config = DemoConfig(fake_mode=False, fake_db=True)
        assert config.fake_mode is False
        assert config.fake_db is True

        # Both disabled
        config = DemoConfig(fake_mode=False, fake_db=False)
        assert config.fake_mode is False
        assert config.fake_db is False

    def test_listing_saver_fake_db(self):
        """Test DemoListingSaver with fake_db"""
        from ..core.listing_parser.saver import DemoListingSaver
        
        # Test with fake_db=False (default)
        saver = DemoListingSaver(use_database=True, fake_db=False)
        assert saver.use_database is True
        assert saver.fake_db is False
        assert saver.db_manager is not None

        # Test with fake_db=True
        saver = DemoListingSaver(use_database=True, fake_db=True)
        assert saver.use_database is False  # Should be disabled when fake_db=True
        assert saver.fake_db is True
        assert saver.db_manager is None

    def test_detail_saver_fake_db(self):
        """Test DemoDetailSaver with fake_db"""
        from ..core.detail_parser.saver import DemoDetailSaver
        
        # Test with fake_db=False (default)
        saver = DemoDetailSaver(use_database=True, fake_db=False)
        assert saver.use_database is True
        assert saver.fake_db is False
        assert saver.db_manager is not None

        # Test with fake_db=True
        saver = DemoDetailSaver(use_database=True, fake_db=True)
        assert saver.use_database is False  # Should be disabled when fake_db=True
        assert saver.fake_db is True
        assert saver.db_manager is None

    def test_config_validation(self):
        """Test that fake_db is properly validated"""
        from ..config import DemoConfig
        
        # Should work with boolean values
        config = DemoConfig(fake_db=True)
        assert config.fake_db is True

        config = DemoConfig(fake_db=False)
        assert config.fake_db is False 