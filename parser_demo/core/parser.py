"""
Demo Parser - Main parser orchestrator with HTTP client integration
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..utils import get_logger
from ..config import DemoConfig
from .listing_parser import DemoListingParser
from .detail_parser import DemoDetailParser


class DemoParser:
    """Main demo parser orchestrator"""

    def __init__(self, service_id: str, config: DemoConfig, fake_mode: bool = False):
        self.config = config
        self.service_id = service_id
        self.fake_mode = fake_mode
        self.logger = get_logger("demo_parser")

        # Initialize specialized parsers with service_id and fake_mode
        self.listing_parser = DemoListingParser(
            service_id=self.service_id, config=self.config, fake_mode=self.fake_mode
        )
        self.detail_parser = DemoDetailParser(
            service_id=self.service_id, config=self.config, fake_mode=self.fake_mode
        )

        # Statistics
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        self.logger.info(f"DemoParser initialized with fake_mode={self.fake_mode}")

    async def initialize(self):
        """Initialize parser components"""
        self.logger.info(f"🚀 DEMO PARSER: initialize called")
        self.logger.info(f"   Service ID: {self.service_id}")
        self.logger.info(f"   Fake mode: {self.fake_mode}")

        self.logger.info("Initializing demo parser orchestrator...")
        self.start_time = datetime.now()

        # Initialize both parsers
        self.logger.info(f"🚀 DEMO PARSER: Initializing listing parser...")
        await self.listing_parser.initialize()
        self.logger.info(f"✅ DEMO PARSER: Listing parser initialized")

        self.logger.info(f"🚀 DEMO PARSER: Initializing detail parser...")
        await self.detail_parser.initialize()
        self.logger.info(f"✅ DEMO PARSER: Detail parser initialized")

        self.logger.success("Demo parser orchestrator initialized successfully")

    async def parse_listings(
        self,
        max_brands: Optional[int] = None,
        max_pages_per_brand: Optional[int] = None,
    ) -> int:
        """Parse fake car listings from brand pages"""
        return await self.listing_parser.parse_listings(max_brands, max_pages_per_brand)

    async def parse_details(self, max_urls: Optional[int] = None) -> int:
        """Parse fake detail pages for vehicles"""
        return await self.detail_parser.parse_details(max_urls)

    async def parse_html_pages(self, max_urls: Optional[int] = None) -> int:
        """Parse fake HTML pages for vehicles"""
        return await self.detail_parser.parse_html_pages(max_urls)

    async def run_full_parsing(
        self, max_brands: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run complete fake parsing pipeline"""
        self.logger.info("Starting full demo parsing pipeline...")

        try:
            # Initialize
            await self.initialize()

            # Parse listings
            listings_count = await self.parse_listings(max_brands)

            # Parse details (optional)
            details_count = await self.parse_details()

            # Parse HTML pages (optional)
            html_count = await self.parse_html_pages()

            # Finalize
            await self.finalize()

            return {
                "success": True,
                "listings_count": listings_count,
                "details_count": details_count,
                "html_count": html_count,
                "failed_brands": self.listing_parser.failed_brands,
                "failed_urls": self.detail_parser.failed_urls,
                "duration": self.get_duration(),
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
            }

        except Exception as e:
            self.logger.error(f"Error in full parsing: {e}")
            return {
                "success": False,
                "error": str(e),
                "listings_count": self.listing_parser.total_listings,
                "details_count": self.detail_parser.total_details,
                "html_count": self.detail_parser.total_html_pages,
                "failed_brands": self.listing_parser.failed_brands,
                "failed_urls": self.detail_parser.failed_urls,
            }

    async def finalize(self):
        """Finalize parsing and print summary"""
        self.end_time = datetime.now()

        # Finalize both parsers
        await self.listing_parser.finalize()
        await self.detail_parser.finalize()

        self.logger.success("=" * 60)
        self.logger.success("DEMO FULL PARSING PIPELINE COMPLETED")
        self.logger.success("=" * 60)
        self.logger.success(f"Total listings: {self.listing_parser.total_listings}")
        self.logger.success(f"Total details: {self.detail_parser.total_details}")
        self.logger.success(f"Total HTML pages: {self.detail_parser.total_html_pages}")
        self.logger.success(f"Failed brands: {len(self.listing_parser.failed_brands)}")
        self.logger.success(f"Failed URLs: {len(self.detail_parser.failed_urls)}")
        self.logger.success(f"Total duration: {self.get_duration()}")

        if self.listing_parser.failed_brands:
            self.logger.warning(
                f"Failed brands: {', '.join(self.listing_parser.failed_brands)}"
            )

        if self.detail_parser.failed_urls:
            self.logger.warning(f"Failed URLs: {len(self.detail_parser.failed_urls)}")

        self.logger.success("=" * 60)

    def get_duration(self) -> str:
        """Get parsing duration"""
        if not self.start_time or not self.end_time:
            return "Unknown"

        duration = self.end_time - self.start_time
        return str(duration)

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive parsing statistics"""
        return {
            "listings": self.listing_parser.get_statistics(),
            "details": self.detail_parser.get_statistics(),
            "total_duration": self.get_duration(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }

    # Convenience methods for accessing individual parser statistics
    @property
    def total_listings(self) -> int:
        return self.listing_parser.total_listings

    @property
    def total_details(self) -> int:
        return self.detail_parser.total_details

    @property
    def total_html_pages(self) -> int:
        return self.detail_parser.total_html_pages

    @property
    def failed_brands(self) -> List[str]:
        return self.listing_parser.failed_brands

    @property
    def failed_urls(self) -> List[str]:
        return self.detail_parser.failed_urls

    # Methods for accessing saved data
    def get_saved_listings(self) -> List[Dict[str, Any]]:
        """Get all saved listings from memory"""
        return self.listing_parser.saver.get_saved_listings()

    def get_saved_details(self) -> List[Dict[str, Any]]:
        """Get all saved details from memory"""
        return self.detail_parser.saver.get_saved_details()

    def get_listings_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Get listings filtered by brand"""
        return self.listing_parser.saver.get_listings_by_brand(brand)

    def get_details_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Get details filtered by brand"""
        return self.detail_parser.saver.get_details_by_brand(brand)

    def clear_all_data(self):
        """Clear all saved data from memory"""
        self.listing_parser.saver.clear_listings()
        self.detail_parser.saver.clear_details()
        self.logger.info("Cleared all demo data from memory")
