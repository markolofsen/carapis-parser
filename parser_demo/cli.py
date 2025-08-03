#!/usr/bin/env python3
"""
Demo Parser CLI - Simple interactive demo parser
"""

import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__)
sys.path.insert(0, str(project_root))

import asyncio
import questionary
from .config import DemoConfig
from .core.parser import DemoParser
from .core.listing_parser import DemoListingParser
from .core.detail_parser import DemoDetailParser
from unreal_utils.logger import get_logger


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
                    {"name": "📊 Parse Listings", "value": "listings"},
                    {"name": "🔄 Full Pipeline", "value": "pipeline"},
                    {"name": "📄 Parse Details", "value": "details"},
                    {"name": "🌐 Parse HTML", "value": "html"},
                    {"name": "🗄️ Database", "value": "database"},
                    {"name": "🧪 Run Tests", "value": "tests"},
                    {"name": "❌ Exit", "value": "exit"},
                ],
            ).ask_async()

            if choice == "listings":
                await self.parse_listings()
            elif choice == "pipeline":
                await self.full_pipeline()
            elif choice == "details":
                await self.parse_details()
            elif choice == "html":
                await self.parse_html()
            elif choice == "database":
                await self.database()
            elif choice == "tests":
                await self.run_tests()
            elif choice == "exit":
                break

    async def parse_listings(self):
        """Parse listings with simple config"""
        max_brands = await questionary.text("Max brands:", default="3").ask_async()
        max_pages = await questionary.text(
            "Max pages per brand:", default="2"
        ).ask_async()

        if await questionary.confirm("Start listing parsing?").ask_async():
            config = DemoConfig(
                max_brands=int(max_brands),
                max_pages_per_brand=int(max_pages)
            )

            parser = DemoListingParser(
                service_id="demo_cli_listing", config=config, fake_mode=True
            )
            await parser.initialize()

            try:
                result = await parser.parse_listings()
                print(f"✅ Parsed {result} listings")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def dry_run(self, max_brands: int = 3, max_pages: int = 2) -> dict:
        """Run parsing in dry mode without interactive prompts"""
        print(f"🚀 DRY RUN: Parsing {max_brands} brands, {max_pages} pages each")

        config = DemoConfig(
            max_brands=max_brands,
            max_pages_per_brand=max_pages
        )

        parser = DemoListingParser(
            service_id="demo_cli_listing", config=config, fake_mode=True
        )
        await parser.initialize()

        try:
            result = await parser.parse_listings()
            print(f"✅ DRY RUN completed: {result} listings")
            return {"success": True, "listings_count": result}
        except Exception as e:
            print(f"❌ DRY RUN error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await parser.finalize()

    async def full_pipeline(self):
        """Run full parsing pipeline"""
        max_brands = await questionary.text("Max brands:", default="2").ask_async()

        if await questionary.confirm("Start full pipeline?").ask_async():
            config = DemoConfig()
            config.max_brands = int(max_brands)

            parser = DemoParser(
                service_id="demo_cli_service", config=config, fake_mode=True
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

    async def dry_run_pipeline(self, max_brands: int = 2) -> dict:
        """Run full pipeline in dry mode"""
        print(f"🚀 DRY RUN PIPELINE: Parsing {max_brands} brands")

        config = DemoConfig(max_brands=max_brands)

        parser = DemoParser(
            service_id="demo_cli_service", config=config, fake_mode=True
        )

        try:
            result = await parser.run_full_parsing()
            if result["success"]:
                print(
                    f"✅ DRY RUN PIPELINE completed: {result['listings_count']} listings, {result['details_count']} details"
                )
                return result
            else:
                print(f"❌ DRY RUN PIPELINE failed: {result.get('error')}")
                return result
        except Exception as e:
            print(f"❌ DRY RUN PIPELINE error: {e}")
            return {"success": False, "error": str(e)}

    async def parse_details(self):
        """Parse details"""
        max_urls = await questionary.text("Max URLs:", default="20").ask_async()

        if await questionary.confirm("Start details parsing?").ask_async():
            config = DemoConfig(max_urls=int(max_urls))

            parser = DemoDetailParser(
                service_id="demo_cli_detail", config=config, fake_mode=True
            )
            await parser.initialize()

            try:
                result = await parser.parse_details()
                print(f"✅ Parsed {result} details")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def dry_run_details(self, max_urls: int = 10) -> dict:
        """Run details parsing in dry mode"""
        print(f"🚀 DRY RUN DETAILS: Parsing {max_urls} URLs")

        config = DemoConfig(max_urls=max_urls)

        parser = DemoDetailParser(
            service_id="demo_cli_detail", config=config, fake_mode=True
        )
        await parser.initialize()

        try:
            result = await parser.parse_details()
            print(f"✅ DRY RUN DETAILS completed: {result} details")
            return {"success": True, "details_count": result}
        except Exception as e:
            print(f"❌ DRY RUN DETAILS error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await parser.finalize()

    async def parse_html(self):
        """Parse HTML pages"""
        max_urls = await questionary.text("Max URLs:", default="10").ask_async()

        if await questionary.confirm("Start HTML parsing?").ask_async():
            config = DemoConfig(max_urls=int(max_urls))

            parser = DemoDetailParser(
                service_id="demo_cli_html", config=config, fake_mode=True
            )
            await parser.initialize()

            try:
                result = await parser.parse_html_pages()
                print(f"✅ Parsed {result} HTML pages")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await parser.finalize()

    async def dry_run_html(self, max_urls: int = 5) -> dict:
        """Run HTML parsing in dry mode"""
        print(f"🚀 DRY RUN HTML: Parsing {max_urls} URLs")

        config = DemoConfig(max_urls=max_urls)

        parser = DemoDetailParser(
            service_id="demo_cli_html", config=config, fake_mode=True
        )
        await parser.initialize()

        try:
            result = await parser.parse_html_pages()
            print(f"✅ DRY RUN HTML completed: {result} HTML pages")
            return {"success": True, "html_count": result}
        except Exception as e:
            print(f"❌ DRY RUN HTML error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await parser.finalize()

    async def database(self):
        """Database management"""
        from .cli_db import DemoDatabaseCLI

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


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Demo Parser CLI")
    parser.add_argument(
        "--dry", action="store_true", help="Run in dry mode without interactive menu"
    )
    parser.add_argument(
        "--mode",
        choices=["listings", "pipeline", "details", "html"],
        default="listings",
        help="Mode to run in dry mode",
    )
    parser.add_argument(
        "--max-brands", type=int, default=3, help="Maximum number of brands to parse"
    )
    parser.add_argument(
        "--max-pages", type=int, default=2, help="Maximum pages per brand"
    )
    parser.add_argument(
        "--max-urls", type=int, default=10, help="Maximum URLs to parse"
    )

    args = parser.parse_args()

    try:
        cli = DemoCLI()

        if args.dry:
            # Run in dry mode
            if args.mode == "listings":
                result = await cli.dry_run(
                    max_brands=args.max_brands, max_pages=args.max_pages
                )
            elif args.mode == "pipeline":
                result = await cli.dry_run_pipeline(max_brands=args.max_brands)
            elif args.mode == "details":
                result = await cli.dry_run_details(max_urls=args.max_urls)
            elif args.mode == "html":
                result = await cli.dry_run_html(max_urls=args.max_urls)

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
