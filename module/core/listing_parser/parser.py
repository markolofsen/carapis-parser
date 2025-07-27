"""
Demo Listing Parser - Main orchestrator for fake car listing parsing
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from parsers.tools.module.logger import get_logger
from parsers.http_client.module.worker_manager import HttpWorkerManager
from ...config import DemoConfig
from .extractor import DemoListingExtractor
from .saver import DemoListingSaver


class DemoListingParser:
    """Demo listing parser with HTTP client integration"""

    def __init__(self, service_id: str, config: DemoConfig, fake_mode: bool = False):
        self.config = config
        self.service_id = service_id
        self.fake_mode = fake_mode
        self.logger = get_logger("demo_listing_parser")

        # Initialize components
        self.extractor = DemoListingExtractor()
        # Use database saver when not in fake_mode and not in fake_db
        self.saver = DemoListingSaver(use_database=not fake_mode, fake_db=getattr(config, 'fake_db', False))

        # Statistics
        self.total_listings = 0
        self.failed_brands: List[str] = []

    async def initialize(self):
        """Initialize parser components"""
        self.logger.info("Initializing demo listing parser...")
        self.start_time = datetime.now()
        self.logger.success("Demo listing parser initialized successfully")

    async def parse_listings(
        self,
        max_brands: Optional[int] = None,
        max_pages_per_brand: Optional[int] = None,
    ) -> int:
        """Parse fake car listings from brand pages"""
        self.logger.info(f"🚀 LISTING PARSER: parse_listings called")
        self.logger.info(f"   Max brands: {max_brands}")
        self.logger.info(f"   Max pages per brand: {max_pages_per_brand}")
        self.logger.info(f"   Fake mode: {self.fake_mode}")

        self.logger.info("Starting demo listings parsing...")

        # Get demo brands
        brands = self._get_demo_brands()
        self.logger.info(f"🚀 LISTING PARSER: Got {len(brands)} demo brands")

        if max_brands:
            brands = brands[:max_brands]
            self.logger.info(f"🚀 LISTING PARSER: Limited to {len(brands)} brands")

        if not brands:
            self.logger.warning("No brands to process")
            self.logger.info(f"❌ LISTING PARSER: No brands to process")
            return 0

        self.logger.info(f"Processing {len(brands)} demo brands for listings...")

        # Create HTTP worker manager for demo requests
        self.logger.info(
            f"🚀 LISTING PARSER: Creating HttpWorkerManager for service {self.service_id}"
        )
        http_config = self.config.to_http_config()
        http_config["service_name"] = self.service_id  # Override with actual service_id
        self.logger.info(f"🚀 LISTING PARSER: HTTP config: {http_config}")

        worker_manager = HttpWorkerManager.create_for_service(**http_config)
        self.logger.info(f"✅ LISTING PARSER: HttpWorkerManager created")

        async def process_brand_listings(
            url: str, context: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Process listings for a single brand"""
            http_manager = context["http_manager"]

            # Find brand info by URL
            brand_info = next((brand for brand in brands if brand["url"] == url), None)
            if not brand_info:
                return {"success": False, "error": f"Brand not found for URL: {url}"}

            brand_name = brand_info.get("name", "Unknown")
            brand_url = brand_info.get("url", "")

            if not brand_url:
                return {"success": False, "error": f"No URL for brand {brand_name}"}

            self.logger.info(f"Processing demo brand: {brand_name}")

            all_listings = []
            max_pages = max_pages_per_brand or self.config.max_pages_per_brand

            for page_num in range(1, max_pages + 1):
                try:
                    # Make a real HTTP request to the demo URL (but we'll ignore the response)
                    result = await http_manager.get_html(brand_url)

                    # Simulate processing delay
                    await asyncio.sleep(self.config.listing_delay)

                    # Generate fake listings regardless of HTTP response
                    page_listings_with_html = self.extractor.extract_listings(
                        result.get("content", ""), brand_name, page_num
                    )

                    if page_listings_with_html:
                        all_listings.extend(page_listings_with_html)
                        self.logger.info(
                            f"Generated {len(page_listings_with_html)} fake listings on page {page_num} for {brand_name}"
                        )
                    else:
                        self.logger.info(
                            f"No fake listings generated on page {page_num} for {brand_name}"
                        )

                except Exception as e:
                    self.logger.error(
                        f"Error processing page {page_num} for {brand_name}: {e}"
                    )
                    # Continue with next page even if there's an error

            # Save listings for this brand
            if all_listings:
                try:
                    saved_count = await self.saver.save_listings(all_listings)
                    self.total_listings += saved_count
                    self.logger.success(
                        f"✅ Completed demo brand {brand_name}: {saved_count} listings"
                    )
                    return {
                        "success": True,
                        "brand": brand_name,
                        "listings_count": saved_count,
                        "total_pages": max_pages,
                    }
                except Exception as e:
                    self.logger.error(f"Error saving listings for {brand_name}: {e}")
                    self.failed_brands.append(brand_name)
                    return {"success": False, "brand": brand_name, "error": str(e)}
            else:
                self.logger.warning(f"No fake listings generated for {brand_name}")
                return {
                    "success": True,
                    "brand": brand_name,
                    "listings_count": 0,
                    "total_pages": 0,
                }

        # Process all brands
        async with worker_manager:
            brand_urls = [brand["url"] for brand in brands]
            results = await worker_manager.process_urls_batch(
                urls=brand_urls, url_processor=process_brand_listings
            )

        # Process results
        successful_brands = 0
        for result in results:
            # Handle both coroutines and regular results
            if hasattr(result, "__await__"):
                result = await result

            # Handle ExecutionResult objects
            if hasattr(result, "data"):
                result = result.data

            if result.get("success"):
                successful_brands += 1
            else:
                self.failed_brands.append(result.get("brand", "Unknown"))

        self.logger.success(
            f"✅ Demo listing parsing completed. Total: {self.total_listings}"
        )
        return self.total_listings

    def _get_demo_brands(self) -> List[Dict[str, str]]:
        """Get demo car brands"""
        return [
            {"name": "Toyota", "url": "https://demo-cars.com/brand/toyota"},
            {"name": "Honda", "url": "https://demo-cars.com/brand/honda"},
            {"name": "Ford", "url": "https://demo-cars.com/brand/ford"},
            {"name": "BMW", "url": "https://demo-cars.com/brand/bmw"},
            {"name": "Mercedes-Benz", "url": "https://demo-cars.com/brand/mercedes"},
            {"name": "Audi", "url": "https://demo-cars.com/brand/audi"},
            {"name": "Lexus", "url": "https://demo-cars.com/brand/lexus"},
            {"name": "Volkswagen", "url": "https://demo-cars.com/brand/volkswagen"},
        ]

    async def finalize(self):
        """Finalize parsing and print summary"""
        self.end_time = datetime.now()
        self.logger.success(
            f"Demo listing parsing completed. Total: {self.total_listings}"
        )

    def get_duration(self) -> str:
        """Get parsing duration"""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return str(duration)
        return "N/A"

    def get_statistics(self) -> Dict[str, Any]:
        """Get parsing statistics"""
        return {
            "total_listings": self.total_listings,
            "failed_brands": self.failed_brands,
            "duration": self.get_duration(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "saved_listings_stats": self.saver.get_statistics(),
        }
