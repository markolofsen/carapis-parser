"""
Demo Parser Models - Peewee ORM with SQLite3
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from peewee import *
from ..utils.logger import get_logger

# Database setup
# Path to database: from module/database/ -> ../../data/demo_parser.db
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'demo_parser.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

database = SqliteDatabase(DB_PATH, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})

logger = get_logger('demo_models')


class BaseModel(Model):
    """Base model with common fields"""
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class DemoItem(BaseModel):
    """Demo item model for storing parsed data"""
    
    # Basic fields
    item_id = CharField(max_length=100, unique=True, index=True)
    title = CharField(max_length=500, null=True)
    url = CharField(max_length=1000, null=True)
    status = CharField(max_length=50, default='new')
    
    # HTML content
    listing_html = TextField(null=True)
    detail_html = TextField(null=True)
    html_content = TextField(null=True)
    
    # Parsed data (JSON)
    listing_data = TextField(null=True)  # JSON string
    detail_data = TextField(null=True)   # JSON string
    
    # Metadata
    brand = CharField(max_length=100, null=True)
    category = CharField(max_length=100, null=True)
    price = DecimalField(max_digits=15, decimal_places=2, null=True)
    
    # Processing info
    processed_at = DateTimeField(null=True)
    error_message = TextField(null=True)
    
    class Meta:
        table_name = 'demo_items'
        indexes = (
            (('status',), False),
            (('brand',), False),
            (('category',), False),
        )

    def __str__(self):
        return f"DemoItem(id={self.item_id}, title={self.title}, status={self.status})"

    @classmethod
    def create_demo_item(cls, **kwargs) -> 'DemoItem':
        """Create a demo item with validation"""
        try:
            item = cls.create(**kwargs)
            logger.info(f"Created demo item: {item.item_id}")
            return item
        except Exception as e:
            logger.error(f"Failed to create demo item: {e}")
            raise

    def update_status(self, status: str, error_message: Optional[str] = None):
        """Update item status"""
        self.status = status
        if error_message:
            self.error_message = error_message
        self.processed_at = datetime.now()
        self.save()
        logger.info(f"Updated item {self.item_id} status to {status}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'title': self.title,
            'url': self.url,
            'status': self.status,
            'brand': self.brand,
            'category': self.category,
            'price': float(self.price) if self.price else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'error_message': self.error_message,
            'has_listing_html': bool(self.listing_html),
            'has_detail_html': bool(self.detail_html),
            'has_html_content': bool(self.html_content),
            'has_listing_data': bool(self.listing_data),
            'has_detail_data': bool(self.detail_data),
        }


class DemoStatistics(BaseModel):
    """Statistics model for tracking parser performance"""
    
    parser_type = CharField(max_length=50)  # 'listing', 'detail', 'html'
    total_items = IntegerField(default=0)
    processed_items = IntegerField(default=0)
    failed_items = IntegerField(default=0)
    start_time = DateTimeField()
    end_time = DateTimeField(null=True)
    duration_seconds = FloatField(null=True)
    
    class Meta:
        table_name = 'demo_statistics'

    def __str__(self):
        return f"DemoStatistics(type={self.parser_type}, processed={self.processed_items}/{self.total_items})"

    @classmethod
    def create_session(cls, parser_type: str, total_items: int = 0) -> 'DemoStatistics':
        """Create a new statistics session"""
        return cls.create(
            parser_type=parser_type,
            total_items=total_items,
            start_time=datetime.now()
        )

    def complete_session(self, processed_items: int, failed_items: int = 0):
        """Complete the statistics session"""
        self.processed_items = processed_items
        self.failed_items = failed_items
        self.end_time = datetime.now()
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.save()
        logger.info(f"Completed {self.parser_type} session: {processed_items} processed, {failed_items} failed")


def initialize_database():
    """Initialize database and create tables"""
    try:
        database.connect()
        database.create_tables([DemoItem, DemoStatistics], safe=True)
        logger.info(f"Database initialized: {DB_PATH}")
        
        # Create indexes
        database.execute_sql('CREATE INDEX IF NOT EXISTS idx_demo_items_status ON demo_items(status)')
        database.execute_sql('CREATE INDEX IF NOT EXISTS idx_demo_items_brand ON demo_items(brand)')
        database.execute_sql('CREATE INDEX IF NOT EXISTS idx_demo_items_category ON demo_items(category)')
        
        logger.info("Database indexes created")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        if not database.is_closed():
            database.close()


def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    try:
        database.connect()
        
        total_items = DemoItem.select().count()
        new_items = DemoItem.select().where(DemoItem.status == 'new').count()
        processed_items = DemoItem.select().where(DemoItem.status == 'processed').count()
        failed_items = DemoItem.select().where(DemoItem.status == 'failed').count()
        
        # Get brand statistics
        brands = (DemoItem
                 .select(DemoItem.brand, fn.COUNT(DemoItem.id).alias('count'))
                 .where(DemoItem.brand.is_null(False))
                 .group_by(DemoItem.brand)
                 .order_by(fn.COUNT(DemoItem.id).desc())
                 .limit(10))
        
        brand_stats = [(brand.brand, brand.count) for brand in brands]
        
        return {
            'total_items': total_items,
            'new_items': new_items,
            'processed_items': processed_items,
            'failed_items': failed_items,
            'success_rate': (processed_items / total_items * 100) if total_items > 0 else 0,
            'top_brands': brand_stats,
            'database_path': DB_PATH
        }
        
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {
            'total_items': 0,
            'new_items': 0,
            'processed_items': 0,
            'failed_items': 0,
            'success_rate': 0,
            'top_brands': [],
            'database_path': DB_PATH,
            'error': str(e)
        }
    finally:
        if not database.is_closed():
            database.close()


# Database initialization is now manual - call initialize_database() when needed
# Auto-migration removed to prevent automatic database creation 