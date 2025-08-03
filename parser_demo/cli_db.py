#!/usr/bin/env python3
"""
Demo Parser Database CLI - Simple database management
"""

import asyncio
import os
import sys
import argparse
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
            # Import local database manager
            from .database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            print("✅ Database initialized successfully")

            # Get basic database info
            info = await db_manager.get_database_info()
            print(f"📊 Database path: {info.get('database_path', 'Unknown')}")
            print(f"📊 Database size: {info.get('database_size', 'Unknown')}")

        except Exception as e:
            print(f"❌ Database setup failed: {e}")

    async def dry_run_setup(self) -> dict:
        """Setup database in dry mode"""
        print("🚀 DRY RUN: Setting up database...")

        try:
            # Import local database manager
            from .database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            print("✅ DRY RUN: Database initialized successfully")

            # Get basic database info
            info = await db_manager.get_database_info()
            print(f"📊 DRY RUN: Database path: {info.get('database_path', 'Unknown')}")

            return {"success": True, "database_path": info.get('database_path', 'Unknown')}
        except Exception as e:
            print(f"❌ DRY RUN: Database setup failed: {e}")
            return {"success": False, "error": str(e)}

    async def show_stats(self):
        """Show database statistics"""
        try:
            # Import local database manager
            from .database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            info = await db_manager.get_database_info()

            print("\n📊 Demo Database Statistics:")
            print("=" * 50)
            print(f"   Database: {info.get('database_type', 'SQLite')}")
            print(f"   Path: {info.get('database_path', 'Unknown')}")
            print(f"   Size: {info.get('database_size', 'Unknown')}")

            print("=" * 50)

        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")

    async def dry_run_stats(self) -> dict:
        """Show database statistics in dry mode"""
        print("🚀 DRY RUN: Getting database statistics...")

        try:
            # Import local database manager
            from .database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            info = await db_manager.get_database_info()

            print("📊 DRY RUN: Demo Database Statistics:")
            print(f"   Database: {info.get('database_type', 'SQLite')}")
            print(f"   Path: {info.get('database_path', 'Unknown')}")
            print(f"   Size: {info.get('database_size', 'Unknown')}")

            return {"success": True, "db_info": info}
        except Exception as e:
            print(f"❌ DRY RUN: Failed to get statistics: {e}")
            return {"success": False, "error": str(e)}

    async def clear_all(self):
        """Clear all data"""
        if await questionary.confirm("🗑️ Clear ALL demo data?").ask_async():
            try:
                # Import local database manager
                from .database.database import DemoDatabaseManager

                db_manager = DemoDatabaseManager()
                # For now, just show that clearing is not implemented
                print("✅ Database clearing not implemented yet")
            except Exception as e:
                print(f"❌ Failed to clear data: {e}")

    async def dry_run_clear(self) -> dict:
        """Clear all data in dry mode"""
        print("🚀 DRY RUN: Clearing all demo data...")

        try:
            # Import local database manager
            from .database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            # For now, just show that clearing is not implemented
            print("✅ DRY RUN: Database clearing not implemented yet")
            return {"success": True, "cleared_count": 0}
        except Exception as e:
            print(f"❌ DRY RUN: Failed to clear data: {e}")
            return {"success": False, "error": str(e)}

    async def reset_database(self):
        """Reset database (delete and recreate)"""
        if await questionary.confirm(
            "🔄 Reset database? This will DELETE all data!"
        ).ask_async():
            try:
                # Import local database manager
                from .database.database import DemoDatabaseManager

                db_manager = DemoDatabaseManager()
                print("✅ Database reset not implemented yet")

            except Exception as e:
                print(f"❌ Database reset failed: {e}")

    async def dry_run_reset(self) -> dict:
        """Reset database in dry mode"""
        print("🚀 DRY RUN: Resetting database...")

        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.models import (
                database,
                initialize_database,
            )

            # Close database connection
            if not database.is_closed():
                database.close()

            # Delete database file
            if self.db_path.exists():
                self.db_path.unlink()
                print("🗑️ DRY RUN: Deleted old database file")

            # Recreate database
            initialize_database()
            print("✅ DRY RUN: Database reset successfully")

            return {"success": True}
        except Exception as e:
            print(f"❌ DRY RUN: Database reset failed: {e}")
            return {"success": False, "error": str(e)}

    async def load_test_data(self):
        """Load test data into database"""
        print("📥 Loading test data...")

        try:
            # Import local modules
            from .config import DemoConfig
            from .core.parser import DemoParser

            # Create demo config
            config = DemoConfig(max_brands=3, max_pages_per_brand=2, fake_mode=True)

            # Create demo parser
            parser = DemoParser(
                service_id="test_service", config=config, fake_mode=True
            )

            # Initialize parser
            await parser.initialize()

            # Parse some listings
            listings_count = await parser.parse_listings(
                max_brands=2, max_pages_per_brand=1
            )
            print(f"✅ Loaded {listings_count} listings")

            # Parse some details
            details_count = await parser.parse_details(max_urls=5)
            print(f"✅ Loaded {details_count} details")

            # Finalize
            await parser.finalize()

            print("✅ Test data loaded successfully!")

        except Exception as e:
            print(f"❌ Failed to load test data: {e}")

    async def dry_run_load_test_data(
        self, max_brands: int = 2, max_pages: int = 1, max_urls: int = 5
    ) -> dict:
        """Load test data in dry mode"""
        print(
            f"🚀 DRY RUN: Loading test data ({max_brands} brands, {max_pages} pages, {max_urls} URLs)..."
        )

        try:
            # Import local modules
            from .config import DemoConfig
            from .core.parser import DemoParser

            # Create demo config
            config = DemoConfig(
                max_brands=max_brands, max_pages_per_brand=max_pages, fake_mode=True
            )

            # Create demo parser
            parser = DemoParser(
                service_id="test_service", config=config, fake_mode=True
            )

            # Initialize parser
            await parser.initialize()

            # Parse some listings
            listings_count = await parser.parse_listings(
                max_brands=max_brands, max_pages_per_brand=max_pages
            )
            print(f"✅ DRY RUN: Loaded {listings_count} listings")

            # Parse some details
            details_count = await parser.parse_details(max_urls=max_urls)
            print(f"✅ DRY RUN: Loaded {details_count} details")

            # Finalize
            await parser.finalize()

            print("✅ DRY RUN: Test data loaded successfully!")

            return {
                "success": True,
                "listings_count": listings_count,
                "details_count": details_count,
            }
        except Exception as e:
            print(f"❌ DRY RUN: Failed to load test data: {e}")
            return {"success": False, "error": str(e)}

    async def search_items(self):
        """Search items in database"""
        try:
            search_term = await questionary.text("Search term:").ask_async()
            if not search_term:
                return

            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.models import database, DemoItem

            database.connect()
            items = (
                DemoItem.select()
                .where(
                    (DemoItem.title.contains(search_term))
                    | (DemoItem.brand.contains(search_term))
                    | (DemoItem.item_id.contains(search_term))
                )
                .limit(20)
            )

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

    async def dry_run_search(self, search_term: str = "test") -> dict:
        """Search items in dry mode"""
        print(f"🚀 DRY RUN: Searching for '{search_term}'...")

        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.models import database, DemoItem

            database.connect()
            items = (
                DemoItem.select()
                .where(
                    (DemoItem.title.contains(search_term))
                    | (DemoItem.brand.contains(search_term))
                    | (DemoItem.item_id.contains(search_term))
                )
                .limit(20)
            )

            results = [item.to_dict() for item in items]
            database.close()

            print(f"🔍 DRY RUN: Found {len(results)} items for '{search_term}'")

            return {
                "success": True,
                "search_term": search_term,
                "results_count": len(results),
                "results": results,
            }
        except Exception as e:
            print(f"❌ DRY RUN: Search failed: {e}")
            return {"success": False, "error": str(e)}

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

            if db_info.get("tables"):
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

    async def dry_run_database_info(self) -> dict:
        """Show database information in dry mode"""
        print("🚀 DRY RUN: Getting database information...")

        try:
            # Import here to avoid Django setup
            from parsers.parser_demo.module.database.database import DemoDatabaseManager

            db_manager = DemoDatabaseManager()
            db_info = await db_manager.get_database_info()

            print("📁 DRY RUN: Database Information:")
            print(f"   Type: {db_info.get('database_type', 'Unknown')}")
            print(f"   Path: {db_info.get('database_path', 'Unknown')}")
            print(f"   Size: {db_info.get('database_size_mb', 0)} MB")

            # Check if file exists
            if self.db_path.exists():
                print(f"   File exists: ✅")
            else:
                print(f"   File exists: ❌")

            return {
                "success": True,
                "db_info": db_info,
                "file_exists": self.db_path.exists(),
            }
        except Exception as e:
            print(f"❌ DRY RUN: Failed to get database info: {e}")
            return {"success": False, "error": str(e)}


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Demo Parser Database CLI")
    parser.add_argument(
        "--dry", action="store_true", help="Run in dry mode without interactive menu"
    )
    parser.add_argument(
        "--mode",
        choices=["setup", "stats", "clear", "reset", "load", "search", "info"],
        default="setup",
        help="Mode to run in dry mode",
    )
    parser.add_argument(
        "--max-brands",
        type=int,
        default=2,
        help="Maximum number of brands for test data",
    )
    parser.add_argument(
        "--max-pages", type=int, default=1, help="Maximum pages per brand for test data"
    )
    parser.add_argument(
        "--max-urls", type=int, default=5, help="Maximum URLs for test data"
    )
    parser.add_argument(
        "--search-term", type=str, default="test", help="Search term for search mode"
    )

    args = parser.parse_args()

    try:
        cli = DemoDatabaseCLI()

        if args.dry:
            # Run in dry mode
            if args.mode == "setup":
                result = await cli.dry_run_setup()
            elif args.mode == "stats":
                result = await cli.dry_run_stats()
            elif args.mode == "clear":
                result = await cli.dry_run_clear()
            elif args.mode == "reset":
                result = await cli.dry_run_reset()
            elif args.mode == "load":
                result = await cli.dry_run_load_test_data(
                    max_brands=args.max_brands,
                    max_pages=args.max_pages,
                    max_urls=args.max_urls,
                )
            elif args.mode == "search":
                result = await cli.dry_run_search(search_term=args.search_term)
            elif args.mode == "info":
                result = await cli.dry_run_database_info()

            if not result.get("success", False):
                sys.exit(1)
        else:
            # Run interactive menu
            await cli.main_menu()

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
