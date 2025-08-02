"""
Demo Detail Parser - extracts fake detailed vehicle information
Uses universal HTTP client module for HTTP requests but generates fake data
"""

import time
from typing import Optional, List, Dict, Any

from datetime import datetime
from unreal_utils.logger import get_logger
from unreal_http import HttpWorkerManager
from ...config import DemoConfig
from .extractor import DemoDetailExtractor
from .saver import DemoDetailSaver


# Configure logging for standalone functions
demo_processor_logger = get_logger("demo_detail_processor")


async def demo_url_processor(url: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process demo URL with HTTP manager but generate fake data

    Args:
        url: Demo URL to process
        context: Context with HTTP manager and other data

    Returns:
        Processing result with fake data
    """
    http_manager = context["http_manager"]
    worker_id = context["worker_id"]
    ids = context.get("ids", {})

    try:
        # Make a real HTTP request to the demo URL (but we'll ignore the response)
        result = await http_manager.get_html(url)

        # Extract IDs from URL
        car_id = ids.get("car_id")
        dealer_id = ids.get("dealer_id")

        # Generate fake detail data regardless of HTTP response
        extractor = DemoDetailExtractor()
        detail_data, page_html = extractor.extract_detail(
            result.get("content", ""), url
        )

        if detail_data:
            demo_processor_logger.success(
                f"Successfully generated fake detail data: {car_id}/{dealer_id}"
            )
            return {
                "url": url,
                "success": True,
                "detail_data": detail_data,
                "page_html": page_html,
                "dealer_id": dealer_id,
                "car_id": car_id,
                "worker_id": worker_id,
            }
        else:
            demo_processor_logger.warning(
                f"Failed to generate fake detail data for: {car_id}/{dealer_id}"
            )
            return {
                "url": url,
                "success": False,
                "error": "Failed to generate fake detail data",
                "dealer_id": dealer_id,
                "car_id": car_id,
            }

    except Exception as e:
        demo_processor_logger.error(f"Error processing {url}: {e}")
        return {
            "url": url,
            "success": False,
            "error": str(e),
            "dealer_id": ids.get("dealer_id"),
            "car_id": ids.get("car_id"),
        }


def demo_extract_ids(url: str) -> Dict[str, str]:
    """Extract demo IDs from URL"""
    try:
        # Extract dealer_id and car_id from URL like: https://demo-cars.com/dealer/dealer_id/car_id.html
        if "/dealer/" in url:
            parts = url.split("/dealer/")[1].split(".html")[0].split("/")
            if len(parts) == 2:
                dealer_id = parts[0]
                car_id = parts[1]
                return {"dealer_id": dealer_id, "car_id": car_id}
    except Exception:
        pass

    return {"dealer_id": None, "car_id": None}


def demo_save_result(result: Dict[str, Any]) -> bool:
    """Save demo result to memory"""
    demo_saver_logger = get_logger("demo_saver", use_global=True)

    if result.get("success"):
        # Save detail data to memory
        detail_data = result.get("detail_data", {})
        page_html = result.get("page_html", "")
        car_id = result.get("car_id")
        dealer_id = result.get("dealer_id")

        demo_saver_logger.info(
            f"Attempting to save fake detail data for {dealer_id}/{car_id}"
        )

        if detail_data and page_html:
            # In a real implementation, this would save to database
            # For demo, we just log success
            demo_saver_logger.success(
                f"✅ Generated fake detail data for {dealer_id}/{car_id}"
            )
            return True
        else:
            demo_saver_logger.warning(
                f"⚠️ Invalid fake detail data for: {dealer_id}/{car_id}"
            )
            return False
    else:
        demo_saver_logger.error(
            f"❌ Failed to generate fake detail data: {result.get('error')}"
        )
        return False


class DemoDetailParser:
    """
    Generates fake detailed vehicle information using HTTP client for requests
    but always returns fake data for testing purposes.
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

        # Initialize HTTP Worker Manager for demo
        self.worker_manager = HttpWorkerManager.create_for_service(
            service_name=self.service_id,
            num_workers=num_workers,
            timeout=timeout,
            max_retries=2,
            retry_delay=1.0,
        )
        self.logger.info(
            f"Created HttpWorkerManager with service_name: {self.service_id}"
        )

        # Initialize components
        self.extractor = DemoDetailExtractor()
        # Use database saver when not in fake_mode and not in fake_db
        self.saver = DemoDetailSaver(use_database=not fake_mode, fake_db=getattr(config, 'fake_db', False))

        self.unique_vehicle_urls = set()
        self.logger.info(f"Initialized demo detail parser with {num_workers} workers")

        # Statistics
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_details = 0
        self.total_html_pages = 0
        self.failed_urls: List[str] = []

    async def initialize(self):
        """Initialize worker manager and parser components"""
        # HttpWorkerManager doesn't have initialize method, it uses context manager
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
                urls_per_brand = 10

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
        await self.process_vehicles_multithreaded(max_urls)
        return self.total_details

    async def parse_html_pages(self, max_urls: Optional[int] = None) -> int:
        """Parse fake HTML pages for vehicles"""
        self.logger.info("Starting fake HTML page parsing...")
        await self.process_vehicles_multithreaded(max_urls)
        return self.total_html_pages

    async def process_vehicles_multithreaded(self, limit: Optional[int] = None):
        """Process vehicle URLs using universal HTTP client module"""
        self.logger.info(
            f"🚀 Starting multithreaded fake detail generation with {self.num_workers} workers..."
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

            # Process URLs using universal HTTP client module
            try:
                results = await self.worker_manager.process_urls_with_retry(
                    urls=urls_list,
                    url_processor=demo_url_processor,
                    extract_ids_func=demo_extract_ids,
                    save_func=demo_save_result,
                    max_retries=2,
                    retry_delay=1.0,
                )

                # Process results
                successful_vehicles = []
                failed_vehicles = []

                for result in results:
                    if result and result.get("success"):
                        successful_vehicles.append(result)
                    else:
                        failed_vehicles.append(result)

                # Save successful vehicles to memory
                if successful_vehicles:
                    self.logger.info(
                        f"💾 Saving {len(successful_vehicles)} fake vehicle details to memory..."
                    )

                    # Save details to memory
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
                self.logger.info(f"   • Saved to memory: {saved_count}")

                if total_failed > 0:
                    self.logger.warning(f"⚠️ {total_failed} vehicles failed processing")

            except Exception as e:
                self.logger.error(f"Error processing vehicles: {e}")

        except Exception as e:
            import traceback

            self.logger.error(f"Error in process_vehicles_multithreaded: {e}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")

    async def cleanup(self):
        """Cleanup resources"""
        # HttpWorkerManager uses context manager, no explicit cleanup needed
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
        await self.process_vehicles_multithreaded(limit)
