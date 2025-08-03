"""
Demo Detail Parser - extracts fake detailed vehicle information
"""

import time
from typing import Optional, List, Dict, Any

from datetime import datetime
from unreal_utils.logger import get_logger
from ...config import DemoConfig
from .extractor import DemoDetailExtractor
from .saver import DemoDetailSaver


class DemoDetailParser:
    """
    Generates fake detailed vehicle information for testing purposes.
    """

    def __init__(
        self,
        service_id: str,
        config: DemoConfig,
        num_workers: int = 5,
        timeout: int = 60,
        fake_mode: bool = False,
    ):
        self.config = config
        self.num_workers = num_workers
        self.timeout = timeout
        self.service_id = service_id
        self.fake_mode = fake_mode
        self.logger = get_logger("demo_detail_parser", use_global=True)
        self.logger.info(
            f"Creating DemoDetailParser with service_id: {self.service_id}"
        )

        # Initialize components
        self.extractor = DemoDetailExtractor()
        # Use database saver when not in fake_db mode
        self.saver = DemoDetailSaver(use_database=not getattr(config, 'fake_db', False), fake_db=getattr(config, 'fake_db', False))

        self.unique_vehicle_urls = set()
        self.logger.info(f"Initialized demo detail parser with {num_workers} workers")

        # Statistics
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_details = 0
        self.total_html_pages = 0
        self.failed_urls: List[str] = []

    async def initialize(self):
        """Initialize parser components"""
        self.start_time = datetime.now()
        self.logger.success("Demo detail parser initialized successfully")

    async def _collect_unique_urls_from_listings(self, limit: Optional[int] = None):
        """Generate fake vehicle URLs for processing"""
        self.logger.info("Generating fake vehicle URLs for processing...")

        try:
            # Generate fake URLs based on demo brands
            demo_brands = [
                "toyota",
                "honda",
                "ford",
                "bmw",
                "mercedes",
                "audi",
                "lexus",
                "volkswagen",
            ]

            unique_urls = set()
            if limit:
                urls_per_brand = max(1, limit // len(demo_brands))
            else:
                urls_per_brand = 50  # Increased from 10 to 50 for better coverage

            for brand in demo_brands:
                for i in range(urls_per_brand):
                    dealer_id = f"demo_dealer_{brand}_{i+1:03d}"
                    car_id = f"demo_car_{brand}_{i+1:03d}"
                    url = f"https://demo-cars.com/dealer/{dealer_id}/{car_id}.html"
                    unique_urls.add(url)

            self.unique_vehicle_urls = unique_urls
            self.logger.info(
                f"Generated {len(self.unique_vehicle_urls)} fake vehicle URLs"
            )

        except Exception as e:
            self.logger.error(f"Error generating fake URLs: {e}")

    async def parse_details(self, max_urls: Optional[int] = None) -> int:
        """Parse fake detail pages for vehicles"""
        self.logger.info("Starting fake detail parsing...")
        await self.process_vehicles(max_urls)
        return self.total_details

    async def parse_html_pages(self, max_urls: Optional[int] = None) -> int:
        """Parse fake HTML pages for vehicles"""
        self.logger.info("Starting fake HTML page parsing...")
        await self.process_vehicles(max_urls)
        return self.total_html_pages

    async def process_vehicles(self, limit: Optional[int] = None):
        """Process vehicle URLs and generate fake data"""
        self.logger.info(
            f"🚀 Starting fake detail generation..."
        )

        try:
            # Generate fake URLs
            await self._collect_unique_urls_from_listings(limit)

            if not self.unique_vehicle_urls:
                self.logger.warning("No fake vehicle URLs generated. Exiting.")
                return

            # Convert set to list for processing
            urls_list = list(self.unique_vehicle_urls)

            self.logger.info(f"📋 Processing {len(urls_list)} fake vehicles")

            successful_vehicles = []
            failed_vehicles = []
            
            # Generate fake details for each URL
            for url in urls_list:
                try:
                    # Generate fake detail data
                    detail_data, page_html = self.extractor.extract_detail("", url)
                    
                    if detail_data:
                        successful_vehicles.append({
                            "url": url,
                            "success": True,
                            "detail_data": detail_data,
                            "page_html": page_html,
                        })
                    else:
                        failed_vehicles.append({
                            "url": url,
                            "success": False,
                            "error": "Failed to generate fake detail data",
                        })
                except Exception as e:
                    failed_vehicles.append({
                        "url": url,
                        "success": False,
                        "error": str(e),
                    })
            
            # Save successful vehicles
            if successful_vehicles:
                self.logger.info(
                    f"💾 Saving {len(successful_vehicles)} fake vehicle details..."
                )

                # Save details to database/memory
                details_to_save = []
                for vehicle_data in successful_vehicles:
                    detail_data = vehicle_data.get("detail_data", {})
                    page_html = vehicle_data.get("page_html", "")
                    if detail_data and page_html:
                        details_to_save.append((detail_data, page_html))

                if details_to_save:
                    saved_count = await self.saver.save_details(details_to_save)
                else:
                    saved_count = 0
            else:
                saved_count = 0

            # Update statistics
            self.total_details = len(successful_vehicles)
            self.total_html_pages = saved_count
            self.failed_urls = [r.get("url") for r in failed_vehicles if r]

            # Show detailed final statistics
            total_processed = len(urls_list)
            total_successful = len(successful_vehicles)
            total_failed = len(failed_vehicles)
            overall_success_rate = (
                (total_successful / total_processed * 100)
                if total_processed > 0
                else 0
            )

            self.logger.success("🎯 Fake detail processing completed!")
            self.logger.info(f"📊 Processing results:")
            self.logger.info(f"   • Total vehicles: {total_processed}")
            self.logger.info(
                f"   • Successfully processed: {total_successful} ({overall_success_rate:.1f}%)"
            )
            self.logger.info(f"   • Failed to process: {total_failed}")
            self.logger.info(f"   • Saved to database: {saved_count}")

            if total_failed > 0:
                self.logger.warning(f"⚠️ {total_failed} vehicles failed processing")

        except Exception as e:
            import traceback

            self.logger.error(f"Error in process_vehicles: {e}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    async def cleanup(self):
        """Cleanup resources"""
        pass

    async def finalize(self):
        """Finalize parsing and print summary"""
        self.end_time = datetime.now()
        self.logger.success(
            f"Fake detail parsing completed. Details: {self.total_details}, HTML: {self.total_html_pages}"
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
            "total_details": self.total_details,
            "total_html_pages": self.total_html_pages,
            "failed_urls": self.failed_urls,
            "duration": self.get_duration(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "saved_details_stats": self.saver.get_statistics(),
        }

    async def run(self, limit: Optional[int] = None):
        """Main execution method for generating fake detail data."""
        self.logger.info("Starting demo detail parser")

        # Process vehicles
        await self.process_vehicles(limit)
