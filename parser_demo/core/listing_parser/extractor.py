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
        
        car_models = ["Camry", "Corolla", "Civic", "Accord", "3 Series", "5 Series", "C-Class", "E-Class", "A4", "A6"]
        
        car_makes = ["Toyota", "Honda", "BMW", "Mercedes", "Audi", "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia"]
        
        for i in range(num_items):
            item = {
                "id": f"car_{i+1}",
                "title": f"{random.choice(car_makes)} {random.choice(car_models)}",
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
    
    def extract_listings(self, html_content: str, brand_name: str, page_num: int) -> List[Dict[str, Any]]:
        """Extract listings from HTML (demo implementation)"""
        # Generate fake listings for the brand
        listings = []
        num_listings = random.randint(8, 20)
        
        # Brand-specific models
        brand_models = {
            "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma"],
            "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
            "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series"],
            "Mercedes": ["C-Class", "E-Class", "S-Class", "GLC", "GLE"],
            "Audi": ["A4", "A6", "Q5", "Q7", "A3"],
            "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Focus"],
            "Chevrolet": ["Silverado", "Camaro", "Equinox", "Malibu", "Tahoe"],
            "Nissan": ["Altima", "Maxima", "Rogue", "Pathfinder", "Sentra"]
        }
        
        models = brand_models.get(brand_name, ["Model"])
        
        for i in range(num_listings):
            # Generate consistent ID format that matches detail extractor
            car_id = f"demo_car_{brand_name.lower()}_{i+1:03d}"
            dealer_id = f"demo_dealer_{brand_name.lower()}_{i+1:03d}"
            
            listing = {
                "id": car_id,  # Use the same ID format as detail extractor
                "title": f"{brand_name} {random.choice(models)}",
                "price": f"${random.randint(15000, 50000):,}",
                "mileage": f"{random.randint(10000, 100000):,} km",
                "year": random.randint(2015, 2024),
                "brand": brand_name,
                "url": f"https://demo-cars.com/dealer/{dealer_id}/{car_id}.html",
                "page_num": page_num
            }
            listings.append(listing)
        
        self.logger.info(f"Generated {len(listings)} fake listings for {brand_name} on page {page_num}")
        return listings
