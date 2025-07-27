"""
Demo Listing Extractor - Generate fake car listing data
"""

from typing import List, Dict, Any, Tuple
import random
from datetime import datetime

from faker import Faker
from parsers.tools.module.logger import get_logger


class DemoListingExtractor:
    """Generate fake car listing data for demo purposes"""

    def __init__(self):
        self.logger = get_logger("demo_listing_extractor")
        self.fake = Faker()
        Faker.seed(42)  # For reproducible results

        # Car brands and models for realistic data
        self.car_brands = {
            "toyota": {
                "name": "Toyota",
                "models": [
                    "Camry",
                    "Corolla",
                    "RAV4",
                    "Highlander",
                    "Tacoma",
                    "Tundra",
                    "Prius",
                    "Avalon",
                ],
            },
            "honda": {
                "name": "Honda",
                "models": [
                    "Civic",
                    "Accord",
                    "CR-V",
                    "Pilot",
                    "Odyssey",
                    "Ridgeline",
                    "Insight",
                    "Passport",
                ],
            },
            "ford": {
                "name": "Ford",
                "models": [
                    "F-150",
                    "Mustang",
                    "Explorer",
                    "Escape",
                    "Edge",
                    "Ranger",
                    "Bronco",
                    "Mach-E",
                ],
            },
            "bmw": {
                "name": "BMW",
                "models": ["3 Series", "5 Series", "X3", "X5", "X1", "X7", "M3", "M5"],
            },
            "mercedes": {
                "name": "Mercedes-Benz",
                "models": [
                    "C-Class",
                    "E-Class",
                    "S-Class",
                    "GLC",
                    "GLE",
                    "GLA",
                    "AMG GT",
                    "CLA",
                ],
            },
            "audi": {
                "name": "Audi",
                "models": ["A4", "A6", "Q5", "Q7", "Q3", "A3", "RS6", "e-tron"],
            },
            "lexus": {
                "name": "Lexus",
                "models": ["ES", "RX", "NX", "LS", "GS", "IS", "LC", "LX"],
            },
            "volkswagen": {
                "name": "Volkswagen",
                "models": [
                    "Golf",
                    "Passat",
                    "Tiguan",
                    "Atlas",
                    "Jetta",
                    "ID.4",
                    "Arteon",
                    "Taos",
                ],
            },
        }

    def extract_listings_from_page(
        self, html_content: str, brand_name: str = "", page_num: int = 1
    ) -> List[Dict[str, Any]]:
        """Extract listings from page HTML - wrapper for extract_listings"""
        listings_with_html = self.extract_listings(html_content, brand_name, page_num)
        # Return only the listing data, not the HTML
        return [listing_data for listing_data, _ in listings_with_html]

    def extract_listings(
        self, html_content: str, brand_name: str = "", page_num: int = 1
    ) -> List[Tuple[Dict[str, Any], str]]:
        """Generate fake car listings with card HTML"""
        listings = []

        # Generate 10-15 listings per page
        num_listings = random.randint(10, 15)

        self.logger.info(
            f"Generating {num_listings} fake car listings for page {page_num}"
        )

        for i in range(num_listings):
            listing_data = self._generate_car_listing(brand_name, page_num, i + 1)
            if listing_data:
                # Generate fake HTML card
                card_html = self._generate_card_html(listing_data)
                listings.append((listing_data, card_html))

        self.logger.success(f"Generated {len(listings)} fake car listings")
        return listings

    def _generate_car_listing(
        self, brand_name: str, page_num: int, item_index: int
    ) -> Dict[str, Any]:
        """Generate fake car listing data"""
        try:
            # Select random brand if not specified
            if not brand_name or brand_name.lower() not in self.car_brands:
                brand_key = random.choice(list(self.car_brands.keys()))
                brand_name = self.car_brands[brand_key]["name"]
            else:
                brand_key = brand_name.lower()

            brand_info = self.car_brands[brand_key]
            model = random.choice(brand_info["models"])

            # Generate realistic car data
            year = random.randint(2015, 2024)
            mileage = random.randint(1000, 150000)
            price = random.randint(15000, 80000)

            # Generate IDs
            dealer_id = f"demo_dealer_{random.randint(1000, 9999)}"
            car_id = f"demo_car_{random.randint(10000, 99999)}"

            # Generate URL
            url = f"https://demo-cars.com/dealer/{dealer_id}/{car_id}.html"

            # Generate title
            title = f"{year} {brand_name} {model}"

            # Generate additional specs
            engine = random.choice(
                ["2.0L I4", "2.5L I4", "3.0L V6", "3.5L V6", "4.0L V8", "2.0L Turbo"]
            )
            transmission = random.choice(["Automatic", "Manual", "CVT"])
            fuel_type = random.choice(["Gasoline", "Hybrid", "Electric", "Diesel"])
            color = random.choice(
                ["White", "Black", "Silver", "Gray", "Blue", "Red", "Green"]
            )

            # Generate dealer info
            dealer_name = f"{self.fake.company()} Auto"
            dealer_location = f"{self.fake.city()}, {self.fake.state_abbr()}"

            # Generate car image URL
            car_image = f"https://demo-cars.com/images/{car_id}.jpg"

            # Generate category based on model type
            category = self._get_category_by_model(model)

            listing_data = {
                "url": url,
                "title": title,
                "car_id": car_id,
                "dealer_id": dealer_id,
                "price": f"${price:,}",
                "price_numeric": price,
                "mileage": f"{mileage:,} miles",
                "mileage_numeric": mileage,
                "year": year,
                "brand": brand_name,
                "model": model,
                "engine": engine,
                "transmission": transmission,
                "fuel_type": fuel_type,
                "color": color,
                "dealer_name": dealer_name,
                "dealer_location": dealer_location,
                "car_image": car_image,
                "brand_name": brand_name,
                "category": category,
                "page_number": page_num,
                "source": "demo",
                "created_at": datetime.now().isoformat(),
            }

            return listing_data

        except Exception as e:
            self.logger.error(f"Error generating car listing: {e}")
            return None

    def _get_category_by_model(self, model: str) -> str:
        """Determine category based on model name"""
        model_lower = model.lower()
        
        # SUV/Crossover models
        suv_models = ["rav4", "cr-v", "pilot", "explorer", "escape", "edge", "x3", "x5", "x1", "x7", 
                     "glc", "gle", "gla", "q5", "q7", "q3", "rx", "nx", "lx", "tiguan", "atlas", "id.4", "taos"]
        
        # Truck models
        truck_models = ["tacoma", "tundra", "f-150", "ranger", "bronco", "ridgeline"]
        
        # Sedan models
        sedan_models = ["camry", "corolla", "civic", "accord", "mustang", "3 series", "5 series", 
                       "c-class", "e-class", "s-class", "a4", "a6", "a3", "es", "ls", "gs", "is", 
                       "lc", "golf", "passat", "jetta", "arteon", "avalon"]
        
        # Luxury/Sports models
        luxury_models = ["m3", "m5", "amg gt", "cla", "rs6", "e-tron"]
        
        # Van/Minivan models
        van_models = ["odyssey", "passport"]
        
        # Electric/Hybrid models
        electric_models = ["prius", "insight", "mach-e", "id.4", "e-tron"]
        
        if model_lower in suv_models:
            return "SUV/Crossover"
        elif model_lower in truck_models:
            return "Truck"
        elif model_lower in luxury_models:
            return "Luxury/Sports"
        elif model_lower in van_models:
            return "Van/Minivan"
        elif model_lower in electric_models:
            return "Electric/Hybrid"
        elif model_lower in sedan_models:
            return "Sedan"
        else:
            return "Other"

    def _generate_card_html(self, listing_data: Dict[str, Any]) -> str:
        """Generate fake HTML card for the listing"""
        try:
            html = f"""
            <div class="car-card" data-car-id="{listing_data['car_id']}" data-dealer-id="{listing_data['dealer_id']}">
                <div class="car-image">
                    <img src="{listing_data['car_image']}" alt="{listing_data['title']}" />
                </div>
                <div class="car-info">
                    <h3 class="car-title">{listing_data['title']}</h3>
                    <div class="car-specs">
                        <span class="year">{listing_data['year']}</span>
                        <span class="mileage">{listing_data['mileage']}</span>
                        <span class="engine">{listing_data['engine']}</span>
                    </div>
                    <div class="car-price">
                        <span class="price">{listing_data['price']}</span>
                    </div>
                    <div class="dealer-info">
                        <span class="dealer-name">{listing_data['dealer_name']}</span>
                        <span class="dealer-location">{listing_data['dealer_location']}</span>
                    </div>
                </div>
            </div>
            """
            return html.strip()

        except Exception as e:
            self.logger.error(f"Error generating card HTML: {e}")
            return "<div>Error generating card</div>"
