"""
Demo Detail Saver - saves car details to database or fake storage
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from utils.logger import get_logger
from ...database.database import DemoDatabaseManager


class DemoDetailSaver:
    """Save fake car detail data to memory or database for demo purposes"""

    def __init__(self, use_database: bool = False, fake_db: bool = False):
        self.logger = get_logger("demo_detail_saver")
        self.use_database = use_database and not fake_db  # Disable DB if fake_db is True
        self.fake_db = fake_db
        
        # In-memory storage for demo detail data
        self.saved_details = []
        
        # Database manager for persistent storage
        if self.use_database and not self.fake_db:
            self.db_manager = DemoDatabaseManager()
            self.logger.info("DemoDetailSaver initialized with database support")
        else:
            self.db_manager = None
            if self.fake_db:
                self.logger.info("DemoDetailSaver initialized with fake database mode (memory-only)")
            else:
                self.logger.info("DemoDetailSaver initialized with memory-only storage")

    async def save_detail(self, detail_data: Dict[str, Any], page_html: str) -> bool:
        """Save single detail to memory or database"""
        try:
            # Add HTML to detail data
            detail_data["page_html"] = page_html
            detail_data["saved_at"] = datetime.now().isoformat()

            if self.use_database and self.db_manager:
                # Save to database
                success = await self.db_manager.save_detail_to_db(detail_data)
                if success:
                    self.logger.success(
                        f"Saved demo detail to database: {detail_data.get('title', 'Unknown')}"
                    )
                return success
            else:
                # Save to memory
                self.saved_details.append(detail_data)
                self.logger.success(
                    f"Saved demo detail to memory: {detail_data.get('title', 'Unknown')}"
                )
                return True

        except Exception as e:
            self.logger.error(f"Error saving demo detail: {e}")
            return False

    async def save_details(self, details: List[Tuple[Dict[str, Any], str]]) -> int:
        """Save multiple details to memory or database"""
        if not details:
            return 0

        try:
            saved_count = 0

            if self.use_database and self.db_manager:
                # Save batch to database
                details_data = []
                for detail_data, page_html in details:
                    detail_data["page_html"] = page_html
                    detail_data["saved_at"] = datetime.now().isoformat()
                    details_data.append(detail_data)
                
                saved_count = await self.db_manager.save_details_batch_to_db(details_data)
                self.logger.success(
                    f"Saved {saved_count}/{len(details)} demo details to database"
                )
            else:
                # Save to memory
                for detail_data, page_html in details:
                    success = await self.save_detail(detail_data, page_html)
                    if success:
                        saved_count += 1

                self.logger.success(
                    f"Saved {saved_count}/{len(details)} demo details to memory"
                )
            
            return saved_count

        except Exception as e:
            self.logger.error(f"Error saving demo details: {e}")
            return 0

    def get_saved_details(self) -> List[Dict[str, Any]]:
        """Get all saved details from memory or database"""
        if self.use_database and self.db_manager:
            # TODO: Implement get_details_from_db method
            self.logger.warning("Database detail retrieval not implemented yet")
            return []
        else:
            return self.saved_details.copy()

    def get_detail_by_car_id(self, car_id: str) -> Dict[str, Any]:
        """Get detail by car ID"""
        if self.use_database and self.db_manager:
            # TODO: Implement database lookup
            self.logger.warning("Database car_id lookup not implemented yet")
            return None
        else:
            for detail in self.saved_details:
                if detail.get("car_id") == car_id:
                    return detail
            return None

    def get_details_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Get details filtered by brand"""
        if self.use_database and self.db_manager:
            # TODO: Implement database filtering
            self.logger.warning("Database brand filtering not implemented yet")
            return []
        else:
            return [
                detail
                for detail in self.saved_details
                if detail.get("brand", "").lower() == brand.lower()
            ]

    def get_details_by_price_range(
        self, min_price: float, max_price: float
    ) -> List[Dict[str, Any]]:
        """Get details filtered by price range"""
        if self.use_database and self.db_manager:
            # TODO: Implement database filtering
            self.logger.warning("Database price filtering not implemented yet")
            return []
        else:
            return [
                detail
                for detail in self.saved_details
                if min_price <= detail.get("price_numeric", 0) <= max_price
            ]

    def get_details_by_year_range(
        self, min_year: int, max_year: int
    ) -> List[Dict[str, Any]]:
        """Get details filtered by year range"""
        if self.use_database and self.db_manager:
            # TODO: Implement database filtering
            self.logger.warning("Database year filtering not implemented yet")
            return []
        else:
            return [
                detail
                for detail in self.saved_details
                if min_year <= detail.get("year", 0) <= max_year
            ]

    def clear_details(self):
        """Clear all saved details from memory or database"""
        if self.use_database and self.db_manager:
            # TODO: Implement database clearing
            self.logger.warning("Database clearing not implemented yet")
        else:
            self.saved_details.clear()
            self.logger.info("Cleared all demo details from memory")

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about saved details"""
        if self.use_database and self.db_manager:
            # Get statistics from database
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're in an async context, we need to handle this differently
                    self.logger.warning("Cannot get database stats in async context")
                    return {"total_details": 0, "database_mode": True}
                else:
                    stats = loop.run_until_complete(self.db_manager.get_statistics_from_db())
                    return stats
            except Exception as e:
                self.logger.error(f"Error getting database statistics: {e}")
                return {"total_details": 0, "database_mode": True, "error": str(e)}
        else:
            # Get statistics from memory
            if not self.saved_details:
                return {
                    "total_details": 0,
                    "brands": [],
                    "price_range": {"min": 0, "max": 0, "avg": 0},
                }

            brands = list(
                set(detail.get("brand", "Unknown") for detail in self.saved_details)
            )
            prices = [detail.get("price_numeric", 0) for detail in self.saved_details]

            return {
                "total_details": len(self.saved_details),
                "brands": brands,
                "brands_count": len(brands),
                "price_range": {
                    "min": min(prices) if prices else 0,
                    "max": max(prices) if prices else 0,
                    "avg": sum(prices) / len(prices) if prices else 0,
                },
            }
