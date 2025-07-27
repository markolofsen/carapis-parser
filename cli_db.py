#!/usr/bin/env python3
"""
Demo Parser Database CLI - Simple database management
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import questionary


class DemoDatabaseCLI:
    """Simple database management CLI for demo parser"""

    def __init__(self):
        self.db_path = Path(__file__).parent / "data" / "demo_parser.db"

    async def main_menu(self):
        """Main menu"""
        while True:
            choice = await questionary.select(
                "🗄️ Demo Database Manager",
                choices=[
                    "🔧 Setup Database",
                    "📊 Show Statistics", 
                    "🗑️ Clear All Data",
                    "🔄 Reset Database",
                    "📥 Load Test Data",
                    "🔍 Search Items",
                    "📁 Database Info",
                    "❌ Exit",
                ],
            ).ask_async()

            if choice == "🔧 Setup Database":
                await self.setup_database()
            elif choice == "📊 Show Statistics":
                await self.show_stats()
            elif choice == "🗑️ Clear All Data":
                await self.clear_all()
            elif choice == "🔄 Reset Database":
                await self.reset_database()
            elif choice == "📥 Load Test Data":
                await self.load_test_data()
            elif choice == "🔍 Search Items":
                await self.search_items()
            elif choice == "📁 Database Info":
                await self.show_database_info()
            elif choice == "❌ Exit":
                break

    async def setup_database(self):
        """Setup database"""
        print("🔧 Setting up database...")
        
        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.models import initialize_database, get_database_stats
            
            initialize_database()
            print("✅ Database initialized successfully")
            
            stats = get_database_stats()
            print(f"📊 Database contains {stats.get('total_items', 0)} items")
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")

    async def show_stats(self):
        """Show database statistics"""
        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.database import DemoDatabaseManager
            
            db_manager = DemoDatabaseManager()
            stats = await db_manager.get_statistics_from_db()
            db_info = await db_manager.get_database_info()
            
            print("\n📊 Demo Database Statistics:")
            print("=" * 50)
            print(f"   Database: {db_info.get('database_type', 'unknown')}")
            print(f"   Size: {db_info.get('database_size_mb', 0)} MB")
            print(f"   Total Items: {stats.get('total_items', 0)}")
            print(f"   New Items: {stats.get('new_items', 0)}")
            print(f"   Processed Items: {stats.get('processed_items', 0)}")
            print(f"   Failed Items: {stats.get('failed_items', 0)}")
            print(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
            
            if stats.get('top_brands'):
                print("\n🏷️ Top Brands:")
                for brand, count in stats['top_brands'][:5]:
                    print(f"   {brand}: {count} items")
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")

    async def clear_all(self):
        """Clear all data"""
        if await questionary.confirm("🗑️ Clear ALL demo data?").ask_async():
            try:
                # Import here to avoid Django setup
                from parsers.parser_demo.module.database.database import DemoDatabaseManager
                
                db_manager = DemoDatabaseManager()
                count = await db_manager.clear_all_data()
                print(f"✅ Cleared {count} demo records")
            except Exception as e:
                print(f"❌ Failed to clear data: {e}")

    async def reset_database(self):
        """Reset database (delete and recreate)"""
        if await questionary.confirm("🔄 Reset database? This will DELETE all data!").ask_async():
            try:
                # Import here to avoid Django setup
                from parsers.parser_demo.module.database.models import database, initialize_database
                
                # Close database connection
                if not database.is_closed():
                    database.close()
                
                # Delete database file
                if self.db_path.exists():
                    self.db_path.unlink()
                    print("🗑️ Deleted old database file")
                
                # Recreate database
                initialize_database()
                print("✅ Database reset successfully")
                
            except Exception as e:
                print(f"❌ Database reset failed: {e}")

    async def load_test_data(self):
        """Load test data into database"""
        print("📥 Loading test data...")
        
        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.config import DemoConfig
            from parsers.parser_demo.module.core.parser import DemoParser
            
            # Create demo config
            config = DemoConfig(
                max_brands=3,
                max_pages_per_brand=2,
                fake_mode=True
            )
            
            # Create demo parser
            parser = DemoParser(
                service_id="test_service",
                config=config,
                fake_mode=True
            )
            
            # Initialize parser
            await parser.initialize()
            
            # Parse some listings
            listings_count = await parser.parse_listings(max_brands=2, max_pages_per_brand=1)
            print(f"✅ Loaded {listings_count} listings")
            
            # Parse some details
            details_count = await parser.parse_details(max_urls=5)
            print(f"✅ Loaded {details_count} details")
            
            # Finalize
            await parser.finalize()
            
            print("✅ Test data loaded successfully!")
            
        except Exception as e:
            print(f"❌ Failed to load test data: {e}")

    async def search_items(self):
        """Search items in database"""
        try:
            search_term = await questionary.text("Search term:").ask_async()
            if not search_term:
                return
            
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.models import database, DemoItem
            
            database.connect()
            items = (DemoItem
                    .select()
                    .where(
                        (DemoItem.title.contains(search_term)) |
                        (DemoItem.brand.contains(search_term)) |
                        (DemoItem.item_id.contains(search_term))
                    )
                    .limit(20))
            
            results = [item.to_dict() for item in items]
            database.close()
            
            print(f"\n🔍 Search results for '{search_term}' ({len(results)}):")
            print("=" * 50)
            for i, item in enumerate(results, 1):
                print(f"   {i}. {item.get('title', 'No title')}")
                print(f"      ID: {item.get('item_id', 'No ID')}")
                print(f"      Brand: {item.get('brand', 'Unknown')}")
                print(f"      Status: {item.get('status', 'Unknown')}")
                print()
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Search failed: {e}")

    async def show_database_info(self):
        """Show detailed database information"""
        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.database import DemoDatabaseManager
            
            db_manager = DemoDatabaseManager()
            db_info = await db_manager.get_database_info()
            
            print("\n📁 Database Information:")
            print("=" * 50)
            print(f"   Type: {db_info.get('database_type', 'Unknown')}")
            print(f"   Path: {db_info.get('database_path', 'Unknown')}")
            print(f"   Size: {db_info.get('database_size_mb', 0)} MB")
            
            if db_info.get('tables'):
                print(f"   Tables: {', '.join(db_info['tables'])}")
            
            # Check if file exists
            if self.db_path.exists():
                print(f"   File exists: ✅")
                print(f"   Last modified: {self.db_path.stat().st_mtime}")
            else:
                print(f"   File exists: ❌")
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Failed to get database info: {e}")


async def main():
    """Main entry point"""
    try:
        cli = DemoDatabaseCLI()
        await cli.main_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
