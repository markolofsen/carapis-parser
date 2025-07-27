# 🧪 Tests

## 📋 Overview

This directory contains tests for the `parser_demo` module. Tests are organized by functionality and complexity.

## 🚀 Quick Start

### Run all tests:
```bash
PYTHONPATH=/path/to/backend/django poetry run python -m pytest tests/ -v
```

### Run specific test file:
```bash
PYTHONPATH=/path/to/backend/django poetry run python -m pytest tests/test_database_simple.py -v
```

### Run tests with output:
```bash
PYTHONPATH=/path/to/backend/django poetry run python -m pytest tests/ -v -s
```

## 📁 Test Files

### ✅ Working Tests

#### `test_database_simple.py`
- **Status**: ✅ Working
- **Purpose**: Database functionality tests
- **Tests**: 6 tests for database operations
- **Dependencies**: Minimal, uses direct imports

#### `test_fake_db_simple_pytest.py`
- **Status**: ✅ Working
- **Purpose**: Test fake_db configuration functionality
- **Tests**: 5 tests for fake_db parameter
- **Dependencies**: Only DemoConfig

#### `test_config.py`
- **Status**: ✅ Working
- **Purpose**: Configuration validation tests
- **Tests**: Basic config validation

### ❌ Broken Tests

#### `test_database.py`
- **Status**: ❌ Broken
- **Issue**: Import errors with complex dependencies
- **Problem**: `ModuleNotFoundError: No module named 'parsers'`

#### `test_database_isolated.py`
- **Status**: ❌ Broken
- **Issue**: Import chain problems
- **Problem**: Complex dependency resolution

#### `test_fake_db_pytest.py`
- **Status**: ❌ Broken
- **Issue**: Missing django_revolution dependency
- **Problem**: `ModuleNotFoundError: No module named 'django_revolution'`

## 🔧 Test Categories

### 1. **Database Tests**
- Test database saving functionality
- Test database manager operations
- Test data persistence

### 2. **Configuration Tests**
- Test DemoConfig validation
- Test fake_mode and fake_db parameters
- Test configuration combinations

### 3. **Integration Tests**
- Test parser integration
- Test adapter functionality
- Test end-to-end workflows

## 🚨 Current Issues

### Import Problems
- Complex dependency chain causes import errors
- Missing dependencies (django_revolution)
- Python path issues

### Solutions Implemented
- **Direct imports**: Use direct file imports to bypass module system
- **sys.path manipulation**: Add project root to Python path
- **Isolated tests**: Create tests that don't depend on complex imports
- **Toggle testing mode**: Switch between working and testing modes

## 🛠️ Testing Tools

### Toggle Testing Mode
```bash
# Switch to testing mode (imports commented)
python tests/toggle_testing_mode.py toggle

# Switch to working mode (imports active)
python tests/toggle_testing_mode.py toggle

# Show current mode
python tests/toggle_testing_mode.py show
```

### Test Environment
- **Python**: 3.10.18
- **pytest**: 8.4.1
- **pytest-asyncio**: 1.1.0
- **Poetry**: Dependency management

## 📊 Test Results

### Last Run Results:
- **test_database_simple.py**: 6/6 ✅ PASSED
- **test_fake_db_simple_pytest.py**: 5/5 ✅ PASSED
- **test_config.py**: ✅ PASSED

### Coverage:
- ✅ Database operations
- ✅ Configuration validation
- ✅ fake_db functionality
- ❌ Complex integration tests
- ❌ Adapter tests

## 🔄 Development Workflow

1. **Write tests** in `tests/` directory
2. **Use simple imports** to avoid dependency issues
3. **Test configuration** with `test_fake_db_simple_pytest.py`
4. **Test database** with `test_database_simple.py`
5. **Run tests** with proper PYTHONPATH

## 📝 Adding New Tests

### Template for Simple Tests:
```python
"""
Test description
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestYourFeature:
    """Test your feature"""

    def test_something(self):
        """Test something"""
        from parsers.parser_demo.module.your_module import YourClass
        
        # Your test code here
        assert True
```

### Best Practices:
- Use direct imports when possible
- Add project root to sys.path
- Keep tests simple and focused
- Avoid complex dependency chains
- Use descriptive test names
