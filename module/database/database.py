"""
Demo Parser Database Manager
Centralized database operations with Peewee ORM and SQLite3
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from asgiref.sync import sync_to_async
from ..utils.logger import get_logger
from .models import DemoItem, DemoStatistics, database, get_database_stats


class DemoDatabaseManager:
    """Database manager for demo parser operations with Peewee ORM"""

    def __init__(self):
        self.logger = get_logger('demo_db_manager')

    @sync_to_async
    def save_listing_to_db(self, listing_data: Dict[str, Any]) -> bool:
        """Save single listing to database"""
        try:
            self.logger.info(f"Demo: Saving listing {listing_data.get('id', 'unknown')}")
            
            # Extract price from listing_data
            price_numeric = listing_data.get('price_numeric')
            if price_numeric:
                price_decimal = float(price_numeric)
            else:
                price_decimal = None
            
            # Create or update demo item
            item, created = DemoItem.get_or_create(
                item_id=listing_data.get('id', 'unknown'),
                defaults={
                    'title': listing_data.get('title'),
                    'url': listing_data.get('url'),
                    'brand': listing_data.get('brand'),
                    'category': listing_data.get('category'),
                    'listing_html': listing_data.get('html_content'),
                    'listing_data': json.dumps(listing_data, ensure_ascii=False),
                    'price': price_decimal,
                    'status': 'processed'
                }
            )
            
            if not created:
                # Update existing item
                item.title = listing_data.get('title')
                item.url = listing_data.get('url')
                item.brand = listing_data.get('brand')
                item.category = listing_data.get('category')
                item.listing_html = listing_data.get('html_content')
                item.listing_data = json.dumps(listing_data, ensure_ascii=False)
                item.price = price_decimal
                item.status = 'processed'
                item.save()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to save listing: {e}")
            return False

    @sync_to_async
    def save_listings_batch_to_db(self, listings_data: List[Dict[str, Any]]) -> int:
        """Save batch of listings to database"""
        try:
            self.logger.info(f"Demo: Saving {len(listings_data)} listings batch")
            
            saved_count = 0
            for listing_data in listings_data:
                try:
                    # Extract price from listing_data
                    price_numeric = listing_data.get('price_numeric')
                    if price_numeric:
                        price_decimal = float(price_numeric)
                    else:
                        price_decimal = None
                    
                    # Create or update demo item
                    item, created = DemoItem.get_or_create(
                        item_id=listing_data.get('id', f'batch_{saved_count}'),
                        defaults={
                            'title': listing_data.get('title'),
                            'url': listing_data.get('url'),
                            'brand': listing_data.get('brand'),
                            'category': listing_data.get('category'),
                            'listing_html': listing_data.get('html_content'),
                            'listing_data': json.dumps(listing_data, ensure_ascii=False),
                            'price': price_decimal,
                            'status': 'processed'
                        }
                    )
                    
                    if not created:
                        # Update existing item
                        item.title = listing_data.get('title')
                        item.url = listing_data.get('url')
                        item.brand = listing_data.get('brand')
                        item.category = listing_data.get('category')
                        item.listing_html = listing_data.get('html_content')
                        item.listing_data = json.dumps(listing_data, ensure_ascii=False)
                        item.price = price_decimal
                        item.status = 'processed'
                        item.save()
                    
                    saved_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to save listing in batch: {e}")
                    continue
            
            return saved_count
        except Exception as e:
            self.logger.error(f"Failed to save listings batch: {e}")
            return 0

    @sync_to_async
    def save_detail_to_db(self, detail_data: Dict[str, Any]) -> bool:
        """Save single detail to database"""
        try:
            self.logger.info(f"Demo: Saving detail {detail_data.get('id', 'unknown')}")
            
            # Find existing item or create new one
            try:
                item = DemoItem.get(DemoItem.item_id == detail_data.get('id'))
            except DemoItem.DoesNotExist:
                item = DemoItem.create(
                    item_id=detail_data.get('id', 'unknown'),
                    title=detail_data.get('title'),
                    url=detail_data.get('url')
                )
            
            # Update with detail data
            item.detail_html = detail_data.get('html_content')
            item.detail_data = json.dumps(detail_data, ensure_ascii=False)
            item.status = 'processed'
            item.save()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to save detail: {e}")
            return False

    @sync_to_async
    def save_details_batch_to_db(self, details_data: List[Dict[str, Any]]) -> int:
        """Save batch of details to database"""
        try:
            self.logger.info(f"Demo: Saving {len(details_data)} details batch")
            
            saved_count = 0
            for detail_data in details_data:
                try:
                    # Find existing item or create new one
                    try:
                        item = DemoItem.get(DemoItem.item_id == detail_data.get('id'))
                    except DemoItem.DoesNotExist:
                        item = DemoItem.create(
                            item_id=detail_data.get('id', f'detail_{saved_count}'),
                            title=detail_data.get('title'),
                            url=detail_data.get('url')
                        )
                    
                    # Update with detail data
                    item.detail_html = detail_data.get('html_content')
                    item.detail_data = json.dumps(detail_data, ensure_ascii=False)
                    item.status = 'processed'
                    item.save()
                    
                    saved_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to save detail in batch: {e}")
                    continue
            
            return saved_count
        except Exception as e:
            self.logger.error(f"Failed to save details batch: {e}")
            return 0

    @sync_to_async
    def save_html_content_to_db(self, item_id: str, html_content: str, url: str) -> bool:
        """Save HTML content to database"""
        try:
            self.logger.info(f"Demo: Saving HTML content for {item_id}")
            
            # Find existing item or create new one
            try:
                item = DemoItem.get(DemoItem.item_id == item_id)
            except DemoItem.DoesNotExist:
                item = DemoItem.create(
                    item_id=item_id,
                    url=url
                )
            
            # Update with HTML content
            item.html_content = html_content
            item.status = 'processed'
            item.save()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to save HTML content: {e}")
            return False

    @sync_to_async
    def get_statistics_from_db(self) -> Dict[str, Any]:
        """Get statistics from database"""
        try:
            stats = get_database_stats()
            stats['database_type'] = 'sqlite3_peewee'
            return stats
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {
                'total_items': 0,
                'new_items': 0,
                'processed_items': 0,
                'failed_items': 0,
                'success_rate': 0,
                'top_brands': [],
                'database_type': 'sqlite3_peewee',
                'error': str(e)
            }

    @sync_to_async
    def get_items_for_details(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get items that need detail parsing"""
        try:
            # Get items that have listing data but no detail data
            items = (DemoItem
                    .select()
                    .where(
                        (DemoItem.listing_data.is_null(False)) & 
                        (DemoItem.detail_data.is_null(True))
                    )
                    .limit(limit))
            
            return [item.to_dict() for item in items]
        except Exception as e:
            self.logger.error(f"Failed to get items for details: {e}")
            return []

    @sync_to_async
    def get_items_for_html(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get items that need HTML content"""
        try:
            # Get items that don't have HTML content
            items = (DemoItem
                    .select()
                    .where(DemoItem.html_content.is_null(True))
                    .limit(limit))
            
            return [item.to_dict() for item in items]
        except Exception as e:
            self.logger.error(f"Failed to get items for HTML: {e}")
            return []

    @sync_to_async
    def clear_all_data(self) -> int:
        """Clear all data from database"""
        try:
            self.logger.info("Demo: Clearing all data")
            
            # Count items before deletion
            total_items = DemoItem.select().count()
            
            # Delete all items
            DemoItem.delete().execute()
            
            # Clear statistics
            DemoStatistics.delete().execute()
            
            return total_items
        except Exception as e:
            self.logger.error(f"Failed to clear data: {e}")
            return 0

    @sync_to_async
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        try:
            from .models import DB_PATH
            import os
            
            db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
            
            return {
                'database_path': DB_PATH,
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'database_type': 'sqlite3_peewee',
                'tables': ['demo_items', 'demo_statistics']
            }
        except Exception as e:
            self.logger.error(f"Failed to get database info: {e}")
            return {
                'database_type': 'sqlite3_peewee',
                'error': str(e)
            }
