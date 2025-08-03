"""
Demo Listing Saver - saves car listings to database or fake storage
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from utils.logger import get_logger
from ...database.database import DemoDatabaseManager


class DemoListingSaver:
    """Save fake car listing data to memory or database for demo purposes"""

    def __init__(self, use_database: bool = False, fake_db: bool = False):
        self.logger = get_logger("demo_listing_saver")
        self.use_database = use_database and not fake_db  # Disable DB if fake_db is True
        self.fake_db = fake_db
        
        # In-memory storage for demo data
        self.saved_listings = []
        
        # Database manager for persistent storage
        if self.use_database and not self.fake_db:
            self.db_manager = DemoDatabaseManager()
            self.logger.info("DemoListingSaver initialized with database support")
        else:
            self.db_manager = None
            if self.fake_db:
                self.logger.info("DemoListingSaver initialized with fake database mode (memory-only)")
            else:
                self.logger.info("DemoListingSaver initialized with memory-only storage")

    async def save_listing(self, listing_data: Dict[str, Any], card_html: str) -> bool:
        """Save single listing to memory or database"""
        try:
            # Add HTML to listing data
            listing_data["card_html"] = card_html
            listing_data["html_content"] = card_html  # Add html_content for database
            listing_data["saved_at"] = datetime.now().isoformat()  # Convert to string for JSON serialization

            if self.use_database and self.db_manager:
                # Save to database
                success = await self.db_manager.save_listing_to_db(listing_data)
                if success:
                    self.logger.success(
                        f"Saved demo listing to database: {listing_data.get('title', 'Unknown')}"
                    )
                return success
            else:
                # Save to memory
                self.saved_listings.append(listing_data)
                self.logger.success(
                    f"Saved demo listing to memory: {listing_data.get('title', 'Unknown')}"
                )
                return True

        except Exception as e:
            self.logger.error(f"Error saving demo listing: {e}")
            return False

    async def save_listings(self, listings: List[Tuple[Dict[str, Any], str]]) -> int:
        """Save multiple listings to memory or database"""
        if not listings:
            return 0

        try:
            saved_count = 0

            if self.use_database and self.db_manager:
                # Save batch to database
                listings_data = []
                for listing_data, card_html in listings:
                    listing_data["card_html"] = card_html
                    listing_data["html_content"] = card_html  # Add html_content for database
                    listing_data["saved_at"] = datetime.now().isoformat()  # Convert to string for JSON serialization
                    listings_data.append(listing_data)
                
                saved_count = await self.db_manager.save_listings_batch_to_db(listings_data)
                self.logger.success(
                    f"Saved {saved_count}/{len(listings)} demo listings to database"
                )
            else:
                # Save to memory
                for listing_data, card_html in listings:
                    success = await self.save_listing(listing_data, card_html)
                    if success:
                        saved_count += 1

                self.logger.success(
                    f"Saved {saved_count}/{len(listings)} demo listings to memory"
                )
            
            return saved_count

        except Exception as e:
            self.logger.error(f"Error saving demo listings: {e}")
            return 0

    def get_saved_listings(self) -> List[Dict[str, Any]]:
        """Get all saved listings from memory or database"""
        if self.use_database and self.db_manager:
            # TODO: Implement get_listings_from_db method
            self.logger.warning("Database listing retrieval not implemented yet")
            return []
        else:
            return self.saved_listings.copy()

    def get_listings_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Get listings filtered by brand"""
        if self.use_database and self.db_manager:
            # TODO: Implement database filtering
            self.logger.warning("Database brand filtering not implemented yet")
            return []
        else:
            return [
                listing
                for listing in self.saved_listings
                if listing.get("brand", "").lower() == brand.lower()
            ]

    def get_listings_by_price_range(
        self, min_price: float, max_price: float
    ) -> List[Dict[str, Any]]:
        """Get listings filtered by price range"""
        if self.use_database and self.db_manager:
            # TODO: Implement database filtering
            self.logger.warning("Database price filtering not implemented yet")
            return []
        else:
            return [
                listing
                for listing in self.saved_listings
                if min_price <= listing.get("price_numeric", 0) <= max_price
            ]

    def clear_listings(self):
        """Clear all saved listings from memory or database"""
        if self.use_database and self.db_manager:
            # TODO: Implement database clearing
            self.logger.warning("Database clearing not implemented yet")
        else:
            self.saved_listings.clear()
            self.logger.info("Cleared all demo listings from memory")

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about saved listings"""
        if self.use_database and self.db_manager:
            # Get statistics from database
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're in an async context, we need to handle this differently
                    self.logger.warning("Cannot get database stats in async context")
                    return {"total_listings": 0, "database_mode": True}
                else:
                    stats = loop.run_until_complete(self.db_manager.get_statistics_from_db())
                    return stats
            except Exception as e:
                self.logger.error(f"Error getting database statistics: {e}")
                return {"total_listings": 0, "database_mode": True, "error": str(e)}
        else:
            # Get statistics from memory
            if not self.saved_listings:
                return {
                    "total_listings": 0,
                    "brands": [],
                    "price_range": {"min": 0, "max": 0, "avg": 0},
                }

            brands = list(
                set(listing.get("brand", "Unknown") for listing in self.saved_listings)
            )
            prices = [listing.get("price_numeric", 0) for listing in self.saved_listings]

            return {
                "total_listings": len(self.saved_listings),
                "brands": brands,
                "brands_count": len(brands),
                "price_range": {
                    "min": min(prices) if prices else 0,
                    "max": max(prices) if prices else 0,
                    "avg": sum(prices) / len(prices) if prices else 0,
                },
            }
