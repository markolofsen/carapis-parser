"""
Demo Listing Extractor - Generate fake car listing data
"""

from typing import List, Dict, Any, Tuple
import random
from datetime import datetime

from faker import Faker
from unreal_utils.logger import get_logger


class DemoListingExtractor:
    """Demo listing extractor that generates fake data"""

    def __init__(self):
        self.fake = Faker()
        self.logger = get_logger("demo_listing_extractor")

    def extract_brands_from_html(self, html_content: str) -> List[str]:
        """Extract brand names from HTML (demo implementation)"""
        # Generate fake brands
        brands = [
            "Toyota", "Honda", "BMW", "Mercedes", "Audi", 
            "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia"
        ]
        return random.sample(brands, random.randint(3, 6))

    def extract_listing_items_from_html(self, html_content: str) -> List[Dict[str, Any]]:
        """Extract listing items from HTML (demo implementation)"""
        items = []
        num_items = random.randint(5, 15)
        
        for i in range(num_items):
            item = {
                "id": f"car_{i+1}",
                "title": f"{self.fake.car_make()} {self.fake.car_model()}",
                "price": f"${random.randint(15000, 50000):,}",
                "mileage": f"{random.randint(10000, 100000):,} km",
                "year": random.randint(2015, 2024),
                "brand": random.choice(["Toyota", "Honda", "BMW", "Mercedes", "Audi"]),
                "url": f"https://demo-cars.com/dealer/dealer_{i+1}/car_{i+1}.html"
            }
            items.append(item)
        
        return items

    def extract_pagination_info(self, html_content: str) -> Dict[str, Any]:
        """Extract pagination information from HTML (demo implementation)"""
        return {
            "current_page": random.randint(1, 5),
            "total_pages": random.randint(3, 10),
            "has_next": random.choice([True, False]),
            "has_prev": random.choice([True, False])
        }
