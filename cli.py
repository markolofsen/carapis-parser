#!/usr/bin/env python3
"""
Demo Parser CLI - Simple interactive demo parser
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


import asyncio
import questionary
from parsers.parser_demo.module import DemoParser, DemoConfig, get_logger
from parsers.parser_demo.module.core.listing_parser import DemoListingParser
from parsers.parser_demo.module.core.detail_parser import DemoDetailParser

class DemoCLI:
    """Simple interactive CLI for demo parser"""

    def __init__(self):
        self.logger = get_logger("demo_cli")

    async def main_menu(self):
        """Main menu"""
        while True:
            choice = await questionary.select(
                "🎯 Demo Parser",
                choices=[
                    "📊 Parse Listings",
                    "🔄 Full Pipeline",
                    "📄 Parse Details",
                    "🌐 Parse HTML",
                    "🗄️ Database",
                    "🧪 Run Tests",
                    "📖 Show Pipeline",
                    "❌ Exit",
                ],
            ).ask_async()

            if choice == "📊 Parse Listings":
                await self.parse_listings()
            elif choice == "🔄 Full Pipeline":
                await self.full_pipeline()
            elif choice == "📄 Parse Details":
                await self.parse_details()
            elif choice == "🌐 Parse HTML":
                await self.parse_html()
            elif choice == "🗄️ Database":
                await self.database()
            elif choice == "🧪 Run Tests":
                await self.run_tests()
            elif choice == "📖 Show Pipeline":
                await self.show_pipeline()
            elif choice == "❌ Exit":
                break

    async def parse_listings(self):
        """Parse listings with simple config"""
        max_brands = await questionary.text("Max brands:", default="3").ask_async()
        max_pages = await questionary.text(
            "Max pages per brand:", default="2"
        ).ask_async()

        if await questionary.confirm("Start listing parsing?").ask_async():
            config = DemoConfig()
            config.max_brands = int(max_brands)
            config.max_pages_per_brand = int(max_pages)

            parser = DemoListingParser(
                service_id="demo_cli_listing", config=config, fake_mode=False
            )
            await parser.initialize()

            try:
                result = await parser.parse_listings()
                print(f"✅ Parsed {result} listings")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def full_pipeline(self):
        """Run full parsing pipeline"""
        max_brands = await questionary.text("Max brands:", default="2").ask_async()

        if await questionary.confirm("Start full pipeline?").ask_async():
            config = DemoConfig()
            config.max_brands = int(max_brands)

            parser = DemoParser(
                service_id="demo_cli_service", config=config, fake_mode=False
            )

            try:
                result = await parser.run_full_parsing()
                if result["success"]:
                    print(
                        f"✅ Pipeline completed: {result['listings_count']} listings, {result['details_count']} details"
                    )
                else:
                    print(f"❌ Pipeline failed: {result.get('error')}")
            except Exception as e:
                print(f"❌ Error: {e}")

    async def parse_details(self):
        """Parse details"""
        max_urls = await questionary.text("Max URLs:", default="20").ask_async()

        if await questionary.confirm("Start details parsing?").ask_async():
            config = DemoConfig()
            config.max_urls = int(max_urls)

            parser = DemoDetailParser(
                service_id="demo_cli_detail", config=config, fake_mode=False
            )
            await parser.initialize()

            try:
                result = await parser.parse_details()
                print(f"✅ Parsed {result} details")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def parse_html(self):
        """Parse HTML pages"""
        max_urls = await questionary.text("Max URLs:", default="10").ask_async()

        if await questionary.confirm("Start HTML parsing?").ask_async():
            config = DemoConfig()
            config.max_urls = int(max_urls)

            parser = DemoDetailParser(
                service_id="demo_cli_html", config=config, fake_mode=False
            )
            await parser.initialize()

            try:
                result = await parser.parse_html_pages()
                print(f"✅ Parsed {result} HTML pages")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def database(self):
        """Database management"""
        from parsers.parser_demo.cli_db import DemoDatabaseCLI

        db_cli = DemoDatabaseCLI()
        await db_cli.main_menu()

    async def run_tests(self):
        """Run tests"""
        if await questionary.confirm("Run all tests?").ask_async():
            import subprocess
            import sys
            from pathlib import Path

            try:
                tests_dir = Path(__file__).parent / "tests"
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", str(tests_dir), "-v"],
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent.parent.parent,
                )

                if result.returncode == 0:
                    print("✅ All tests passed")
                else:
                    print("❌ Some tests failed")
                    print(result.stdout)
            except Exception as e:
                print(f"❌ Error running tests: {e}")

    async def show_pipeline(self):
        """Show pipeline information"""
        print("📖 Demo Parser Pipeline:")
        print("")
        print("1. 📊 Parse Listings")
        print("   - Extract brand list")
        print("   - Parse listing pages")
        print("   - Save listings to DB")
        print("")
        print("2. 📄 Parse Details")
        print("   - Get items without details")
        print("   - Parse detail pages")
        print("   - Save details to DB")
        print("")
        print("3. 🌐 Parse HTML")
        print("   - Get items for HTML parsing")
        print("   - Download HTML pages")
        print("   - Save HTML content")
        print("")
        print("4. 🔄 Full Pipeline")
        print("   - Run all steps in sequence")
        print("   - Handle errors gracefully")
        print("   - Generate statistics")
        print("")
        print("📁 File Structure:")
        print("   module/")
        print("   ├── config.py          # Configuration")
        print("   ├── database.py        # Database operations")
        print("   ├── adapter.py         # Data server integration")
        print("   └── core/")
        print("       ├── listing_parser/")
        print("       ├── detail_parser/")
        print("       └── parser.py")
        print("")
        print("🎯 This is a demo parser showing the standard pipeline structure!")


async def main():
    """Main entry point"""
    try:
        cli = DemoCLI()
        await cli.main_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
