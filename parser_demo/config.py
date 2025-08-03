"""
Demo Parser Configuration
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class DemoConfig(BaseModel):
    """Configuration for demo parser"""

    # Parser settings
    max_brands: int = Field(default=4, description="Maximum number of brands to parse")
    max_pages_per_brand: int = Field(default=3, description="Maximum pages per brand")
    max_urls: int = Field(default=100, description="Maximum URLs to process")
    max_items_per_category: int = Field(
        default=10, description="Maximum items per category"
    )
    max_items_for_details: int = Field(
        default=20, description="Maximum items for detail parsing"
    )

    # HTTP client settings
    max_workers: int = Field(default=5, description="Number of HTTP workers")
    timeout: int = Field(default=60, description="HTTP request timeout in seconds")
    max_retries: int = Field(default=2, description="Maximum retry attempts")
    retry_delay: float = Field(
        default=1.0, description="Delay between retries in seconds"
    )

    # Timing settings
    listing_delay: float = Field(
        default=0.1, description="Delay between listing items (seconds)"
    )
    detail_delay: float = Field(
        default=0.2, description="Delay between detail items (seconds)"
    )

    # Demo data settings
    enable_random_errors: bool = Field(
        default=False, description="Enable random errors for testing"
    )
    error_rate: float = Field(default=0.1, description="Error rate (0.0 to 1.0)")

    # Logging settings
    verbose_logging: bool = Field(default=True, description="Enable verbose logging")

    # Testing settings
    fake_mode: bool = Field(
        default=True,
        description="Enable fake mode for testing without real HTTP requests",
    )
    fake_db: bool = Field(
        default=False,
        description="Enable fake database mode for testing without database operations",
    )

    # HTTP client settings
    use_smart_manager: bool = Field(
        default=True,
        description="Use smart proxy manager for HTTP requests",
    )

    # Car-specific settings
    cars_per_page: int = Field(default=20, description="Number of cars per page")
    consecutive_empty_pages_limit: int = Field(
        default=3, description="Stop after N consecutive empty pages"
    )

    model_config = dict(validate_assignment=True, frozen=False)  # Pydantic v2 ConfigDict

    @field_validator('max_brands', 'max_pages_per_brand', 'max_urls', 'max_items_per_category', 'max_items_for_details', 'max_workers', 'timeout', 'max_retries', 'cars_per_page', 'consecutive_empty_pages_limit')
    @classmethod
    def validate_positive_integers(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v

    @field_validator('retry_delay', 'listing_delay', 'detail_delay')
    @classmethod
    def validate_positive_floats(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

    @field_validator('error_rate')
    @classmethod
    def validate_error_rate(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Error rate must be between 0.0 and 1.0')
        return v

    def to_http_config(self) -> Dict[str, Any]:
        """Convert to HTTP client configuration"""
        return {
            "service_name": "demo_parser",
            "num_workers": self.max_workers,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "use_smart_manager": self.use_smart_manager,
            "show_progress": False,
            "fake_mode": self.fake_mode,
        }
