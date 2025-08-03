"""
Demo Listing Parser - Main orchestrator for fake car listing parsing
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from unreal_utils.logger import get_logger
from ...config import DemoConfig
from .extractor import DemoListingExtractor
from .saver import DemoListingSaver


class DemoListingParser:
    """Demo listing parser that generates fake data"""

    def __init__(self, service_id: str, config: DemoConfig, fake_mode: bool = False):
        self.config = config
        self.service_id = service_id
        self.fake_mode = fake_mode
        self.logger = get_logger("demo_listing_parser")

        # Initialize components
        self.extractor = DemoListingExtractor()
        # Use database saver when not in fake_db mode
        self.saver = DemoListingSaver(use_database=not getattr(config, 'fake_db', False), fake_db=getattr(config, 'fake_db', False))

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

        # Generate fake listings for each brand
        for brand in brands:
            brand_name = brand["name"]
            self.logger.info(f"🎯 Generating fake listings for {brand_name}")
            
            # Generate fake listings
            fake_listings = []
            max_pages = max_pages_per_brand or 3  # Default to 3 pages
            
            for page_num in range(1, max_pages + 1):
                page_listings = self.extractor.extract_listings(
                    html_content="",  # Empty content in fake mode
                    brand_name=brand_name,
                    page_num=page_num
                )
                fake_listings.extend(page_listings)
            
            # Save fake listings
            if fake_listings:
                try:
                    # Convert listings to format expected by saver: (listing_data, card_html)
                    listings_with_html = []
                    for listing in fake_listings:
                        # Generate fake HTML for each listing
                        card_html = f"""
                        <div class="car-listing">
                            <h3>{listing['title']}</h3>
                            <p>Price: {listing['price']}</p>
                            <p>Mileage: {listing['mileage']}</p>
                            <p>Year: {listing['year']}</p>
                            <p>Brand: {listing['brand']}</p>
                        </div>
                        """
                        listings_with_html.append((listing, card_html))
                    
                    saved_count = await self.saver.save_listings(listings_with_html)
                    self.total_listings += saved_count
                    self.logger.success(
                        f"✅ Generated {saved_count} fake listings for {brand_name}"
                    )
                except Exception as e:
                    self.logger.error(f"Error saving fake listings for {brand_name}: {e}")
                    self.failed_brands.append(brand_name)
            else:
                self.logger.warning(f"No fake listings generated for {brand_name}")
        
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
