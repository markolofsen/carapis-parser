"""
Simple pytest tests for fake_db functionality (config only)
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestFakeDBConfig:
    """Test fake_db configuration only"""

    def test_fake_db_default(self):
        """Test that fake_db defaults to False"""
        from parsers.parser_demo.module.config import DemoConfig
        
        config = DemoConfig()
        assert config.fake_db is False

    def test_fake_db_enabled(self):
        """Test that fake_db can be enabled"""
        from parsers.parser_demo.module.config import DemoConfig
        
        config = DemoConfig(fake_db=True)
        assert config.fake_db is True

    def test_fake_mode_and_fake_db_combination(self):
        """Test combination of fake_mode and fake_db"""
        from parsers.parser_demo.module.config import DemoConfig
        
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

    def test_config_validation(self):
        """Test that fake_db is properly validated"""
        from parsers.parser_demo.module.config import DemoConfig
        
        # Should work with boolean values
        config = DemoConfig(fake_db=True)
        assert config.fake_db is True

        config = DemoConfig(fake_db=False)
        assert config.fake_db is False

    def test_to_http_config_includes_fake_mode(self):
        """Test that to_http_config includes fake_mode"""
        from parsers.parser_demo.module.config import DemoConfig
        
        config = DemoConfig(fake_mode=True, fake_db=True)
        http_config = config.to_http_config()
        
        assert http_config['fake_mode'] is True
        # Note: fake_db is not included in http_config as it's for database operations 