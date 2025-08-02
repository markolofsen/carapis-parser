#!/usr/bin/env python3
"""
Toggle testing mode - switch between working and testing modes
"""

import os
import sys
from pathlib import Path


def toggle_testing_mode():
    """Toggle between testing and working modes"""
    
    # Path to module/__init__.py
    init_file = Path(__file__).parent.parent / "module" / "__init__.py"
    
    if not init_file.exists():
        print(f"❌ File not found: {init_file}")
        return False
    
    # Read current content
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Check current mode
    is_testing_mode = "# from .adapter import DemoDataServerAdapter  # Temporarily commented for pytest" in content
    
    if is_testing_mode:
        # Switch to working mode
        print("🔄 Switching to WORKING mode...")
        
        # Replace commented imports with active imports
        new_content = content.replace(
            "# from .adapter import DemoDataServerAdapter  # Temporarily commented for pytest",
            "from .adapter import DemoDataServerAdapter"
        ).replace(
            "# from .core.parser import DemoParser  # Temporarily commented for pytest",
            "from .core.parser import DemoParser"
        ).replace(
            "# from .core.listing_parser import DemoListingParser  # Temporarily commented for pytest",
            "from .core.listing_parser import DemoListingParser"
        ).replace(
            "# from .core.detail_parser import DemoDetailParser  # Temporarily commented for pytest",
            "from .core.detail_parser import DemoDetailParser"
        ).replace(
            "# 'DemoDataServerAdapter',  # Temporarily commented for pytest",
            "'DemoDataServerAdapter'"
        ).replace(
            "# 'DemoParser',  # Temporarily commented for pytest",
            "'DemoParser'"
        ).replace(
            "# 'DemoListingParser',  # Temporarily commented for pytest",
            "'DemoListingParser'"
        ).replace(
            "# 'DemoDetailParser'  # Temporarily commented for pytest",
            "'DemoDetailParser'"
        )
        
        mode = "WORKING"
        
    else:
        # Switch to testing mode
        print("🔄 Switching to TESTING mode...")
        
        # Replace active imports with commented imports
        new_content = content.replace(
            "from .adapter import DemoDataServerAdapter",
            "# from .adapter import DemoDataServerAdapter  # Temporarily commented for pytest"
        ).replace(
            "from .core.parser import DemoParser",
            "# from .core.parser import DemoParser  # Temporarily commented for pytest"
        ).replace(
            "from .core.listing_parser import DemoListingParser",
            "# from .core.listing_parser import DemoListingParser  # Temporarily commented for pytest"
        ).replace(
            "from .core.detail_parser import DemoDetailParser",
            "# from .core.detail_parser import DemoDetailParser  # Temporarily commented for pytest"
        ).replace(
            "'DemoDataServerAdapter'",
            "# 'DemoDataServerAdapter',  # Temporarily commented for pytest"
        ).replace(
            "'DemoParser'",
            "# 'DemoParser',  # Temporarily commented for pytest"
        ).replace(
            "'DemoListingParser'",
            "# 'DemoListingParser',  # Temporarily commented for pytest"
        ).replace(
            "'DemoDetailParser'",
            "# 'DemoDetailParser'  # Temporarily commented for pytest"
        )
        
        mode = "TESTING"
    
    # Write new content
    with open(init_file, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Switched to {mode} mode")
    print(f"📁 Modified: {init_file}")
    
    if mode == "TESTING":
        print("\n🧪 Now you can run tests:")
        print("   poetry run python -m pytest tests/test_database_simple.py -v -s")
    else:
        print("\n🚀 Now you can run CLI:")
        print("   poetry run python cli.py")
    
    return True


def show_current_mode():
    """Show current mode without changing it"""
    
    init_file = Path(__file__).parent.parent / "module" / "__init__.py"
    
    if not init_file.exists():
        print(f"❌ File not found: {init_file}")
        return False
    
    with open(init_file, 'r') as f:
        content = f.read()
    
    is_testing_mode = "# from .adapter import DemoDataServerAdapter  # Temporarily commented for pytest" in content
    
    if is_testing_mode:
        print("🧪 Current mode: TESTING")
        print("   - Problematic imports are commented out")
        print("   - Tests can run with pytest")
        print("   - CLI will not work")
    else:
        print("🚀 Current mode: WORKING")
        print("   - All imports are active")
        print("   - CLI works normally")
        print("   - Tests will fail with import errors")
    
    return True


def main():
    """Main function"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['toggle', 'switch', 'change']:
            toggle_testing_mode()
        elif command in ['show', 'status', 'current']:
            show_current_mode()
        elif command in ['test', 'testing']:
            # Force testing mode
            print("🔄 Forcing TESTING mode...")
            # Implementation would go here
            print("⚠️  Use 'toggle' to switch modes")
        elif command in ['work', 'working']:
            # Force working mode
            print("🔄 Forcing WORKING mode...")
            # Implementation would go here
            print("⚠️  Use 'toggle' to switch modes")
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
    else:
        show_current_mode()
        print("\n💡 Use 'toggle' to switch modes")


def print_usage():
    """Print usage information"""
    print("\n📖 Usage:")
    print("   python toggle_testing_mode.py [command]")
    print("\n🔧 Commands:")
    print("   toggle/switch/change  - Switch between testing and working modes")
    print("   show/status/current  - Show current mode (default)")
    print("   test/testing         - Show testing mode info")
    print("   work/working         - Show working mode info")


if __name__ == "__main__":
    main() 