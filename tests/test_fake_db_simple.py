#!/usr/bin/env python3
"""
Simple test for fake_db functionality
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_fake_db_config():
    """Test fake_db configuration"""
    print("🧪 Testing fake_db configuration...")
    
    try:
        from parsers.parser_demo.module.config import DemoConfig
        
        # Test default config
        config = DemoConfig()
        print(f"✅ Default fake_db: {config.fake_db}")
        assert config.fake_db is False
        
        # Test with fake_db=True
        config = DemoConfig(fake_db=True)
        print(f"✅ fake_db=True: {config.fake_db}")
        assert config.fake_db is True
        
        # Test combination
        config = DemoConfig(fake_mode=True, fake_db=True)
        print(f"✅ fake_mode=True, fake_db=True: {config.fake_mode}, {config.fake_db}")
        assert config.fake_mode is True
        assert config.fake_db is True
        
        print("✅ All fake_db config tests passed!")
        
    except Exception as e:
        print(f"❌ Error testing fake_db config: {e}")
        return False
    
    return True

def test_saver_fake_db():
    """Test saver with fake_db"""
    print("🧪 Testing saver with fake_db...")
    
    try:
        from parsers.parser_demo.module.core.listing_parser.saver import DemoListingSaver
        
        # Test with fake_db=False
        saver = DemoListingSaver(use_database=True, fake_db=False)
        print(f"✅ fake_db=False: use_database={saver.use_database}, db_manager={'exists' if saver.db_manager else 'None'}")
        
        # Test with fake_db=True
        saver = DemoListingSaver(use_database=True, fake_db=True)
        print(f"✅ fake_db=True: use_database={saver.use_database}, db_manager={'exists' if saver.db_manager else 'None'}")
        assert saver.use_database is False  # Should be disabled
        assert saver.db_manager is None
        
        print("✅ All saver fake_db tests passed!")
        
    except Exception as e:
        print(f"❌ Error testing saver fake_db: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting fake_db tests...")
    
    tests = [
        test_fake_db_config,
        test_saver_fake_db,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 