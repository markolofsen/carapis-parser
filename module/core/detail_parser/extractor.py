"""
Demo Detail Extractor - Generate fake car detail data
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from bs4 import BeautifulSoup

from faker import Faker
from unreal_utils.logger import get_logger


class DemoDetailExtractor:
    """Generate fake car detail data for demo purposes"""

    def __init__(self):
        self.logger = get_logger("demo_detail_extractor")
        self.fake = Faker()
        Faker.seed(42)  # For reproducible results

    def extract_detail(self, html_content: str, url: str) -> Tuple[Dict[str, Any], str]:
        """Generate fake detail data and page HTML"""
        try:
            # Extract structured data
            detail_data = self._generate_detail_data(url)

            # Generate fake page HTML
            page_html = self._generate_page_html(detail_data)

            # Return both data and HTML
            return detail_data, page_html

        except Exception as e:
            self.logger.error(f"Error generating detail: {e}")
            return {
                "url": url,
                "source": "demo",
            }, "<html><body>Error generating detail</body></html>"

    def _generate_detail_data(self, url: str) -> Dict[str, Any]:
        """Generate structured detail data from URL"""
        detail_data = {
            "url": url,
            "source": "demo",
            "extracted_at": datetime.now().isoformat(),
        }

        try:
            # Extract car_id and dealer_id from URL
            car_id, dealer_id = self._extract_ids_from_url(url)

            if not car_id or not dealer_id:
                # Generate random IDs if URL parsing fails
                car_id = f"demo_car_{random.randint(10000, 99999)}"
                dealer_id = f"demo_dealer_{random.randint(1000, 9999)}"

            # Generate comprehensive car details
            detail_data.update(self._generate_car_specifications(car_id, dealer_id))
            detail_data.update(self._generate_dealer_info(dealer_id))
            detail_data.update(self._generate_images(car_id))
            detail_data.update(self._generate_reviews())

            self.logger.info(f"Generated detail data for {car_id}")
            return detail_data

        except Exception as e:
            self.logger.error(f"Error generating detail data: {e}")
            return detail_data

    def _extract_ids_from_url(self, url: str) -> Tuple[str, str]:
        """Extract car_id and dealer_id from URL"""
        try:
            # Format: https://demo-cars.com/dealer/dealer_id/car_id.html
            if "/dealer/" in url:
                parts = url.split("/dealer/")[1].split(".html")[0].split("/")
                if len(parts) == 2:
                    dealer_id = parts[0]
                    car_id = parts[1]
                    return car_id, dealer_id
        except Exception:
            pass

        return None, None

    def _generate_car_specifications(
        self, car_id: str, dealer_id: str
    ) -> Dict[str, Any]:
        """Generate comprehensive car specifications"""
        # Car brands and models
        car_brands = {
            "toyota": [
                "Camry",
                "Corolla",
                "RAV4",
                "Highlander",
                "Tacoma",
                "Tundra",
                "Prius",
                "Avalon",
            ],
            "honda": [
                "Civic",
                "Accord",
                "CR-V",
                "Pilot",
                "Odyssey",
                "Ridgeline",
                "Insight",
                "Passport",
            ],
            "ford": [
                "F-150",
                "Mustang",
                "Explorer",
                "Escape",
                "Edge",
                "Ranger",
                "Bronco",
                "Mach-E",
            ],
            "bmw": ["3 Series", "5 Series", "X3", "X5", "X1", "X7", "M3", "M5"],
            "mercedes": [
                "C-Class",
                "E-Class",
                "S-Class",
                "GLC",
                "GLE",
                "GLA",
                "AMG GT",
                "CLA",
            ],
            "audi": ["A4", "A6", "Q5", "Q7", "Q3", "A3", "RS6", "e-tron"],
            "lexus": ["ES", "RX", "NX", "LS", "GS", "IS", "LC", "LX"],
            "volkswagen": [
                "Golf",
                "Passat",
                "Tiguan",
                "Atlas",
                "Jetta",
                "ID.4",
                "Arteon",
                "Taos",
            ],
        }

        # Select random brand and model
        brand_key = random.choice(list(car_brands.keys()))
        brand_name = brand_key.title()
        model = random.choice(car_brands[brand_key])

        # Generate specifications
        year = random.randint(2015, 2024)
        mileage = random.randint(1000, 150000)
        price = random.randint(15000, 80000)

        # Engine specs
        engines = [
            "2.0L I4",
            "2.5L I4",
            "3.0L V6",
            "3.5L V6",
            "4.0L V8",
            "2.0L Turbo",
            "3.0L Turbo",
        ]
        engine = random.choice(engines)

        # Transmission
        transmissions = [
            "Automatic",
            "Manual",
            "CVT",
            "8-Speed Automatic",
            "6-Speed Manual",
        ]
        transmission = random.choice(transmissions)

        # Fuel type
        fuel_types = ["Gasoline", "Hybrid", "Electric", "Diesel", "Plug-in Hybrid"]
        fuel_type = random.choice(fuel_types)

        # Colors
        colors = [
            "White",
            "Black",
            "Silver",
            "Gray",
            "Blue",
            "Red",
            "Green",
            "Orange",
            "Yellow",
        ]
        exterior_color = random.choice(colors)
        interior_color = random.choice(["Black", "Gray", "Beige", "Brown", "White"])

        # Features
        features = [
            "Bluetooth",
            "Navigation",
            "Backup Camera",
            "Heated Seats",
            "Sunroof",
            "Leather Seats",
            "Apple CarPlay",
            "Android Auto",
            "Blind Spot Monitor",
            "Lane Departure Warning",
            "Adaptive Cruise Control",
            "Wireless Charging",
        ]
        selected_features = random.sample(features, random.randint(5, 10))

        return {
            "car_id": car_id,
            "dealer_id": dealer_id,
            "title": f"{year} {brand_name} {model}",
            "brand": brand_name,
            "model": model,
            "year": year,
            "price": f"${price:,}",
            "price_numeric": price,
            "mileage": f"{mileage:,} miles",
            "mileage_numeric": mileage,
            "engine": engine,
            "transmission": transmission,
            "fuel_type": fuel_type,
            "exterior_color": exterior_color,
            "interior_color": interior_color,
            "features": selected_features,
            "description": self.fake.text(max_nb_chars=500),
            "vin": self._generate_vin(),
            "condition": random.choice(["Excellent", "Good", "Fair", "Like New"]),
            "title_status": random.choice(["Clean", "Salvage", "Rebuilt"]),
            "accident_history": random.choice(["None", "Minor", "Moderate", "Major"]),
            "owner_count": random.randint(1, 4),
            "fuel_economy": {
                "city": random.randint(15, 35),
                "highway": random.randint(25, 45),
                "combined": random.randint(20, 40),
            },
        }

    def _generate_dealer_info(self, dealer_id: str) -> Dict[str, Any]:
        """Generate dealer information"""
        return {
            "dealer": {
                "name": f"{self.fake.company()} Auto",
                "phone": self.fake.phone_number(),
                "email": self.fake.email(),
                "address": self.fake.address(),
                "city": self.fake.city(),
                "state": self.fake.state_abbr(),
                "zip_code": self.fake.zipcode(),
                "website": f"https://{self.fake.domain_name()}",
                "hours": {
                    "monday": "9:00 AM - 6:00 PM",
                    "tuesday": "9:00 AM - 6:00 PM",
                    "wednesday": "9:00 AM - 6:00 PM",
                    "thursday": "9:00 AM - 6:00 PM",
                    "friday": "9:00 AM - 6:00 PM",
                    "saturday": "9:00 AM - 5:00 PM",
                    "sunday": "Closed",
                },
            }
        }

    def _generate_images(self, car_id: str) -> Dict[str, Any]:
        """Generate image URLs"""
        num_images = random.randint(8, 15)
        images = []

        for i in range(num_images):
            images.append(f"https://demo-cars.com/images/{car_id}_{i+1}.jpg")

        return {
            "images": images,
            "main_image": images[0] if images else None,
            "image_count": len(images),
        }

    def _generate_reviews(self) -> Dict[str, Any]:
        """Generate fake reviews"""
        num_reviews = random.randint(3, 8)
        reviews = []

        for i in range(num_reviews):
            reviews.append(
                {
                    "rating": random.randint(3, 5),
                    "comment": self.fake.text(max_nb_chars=200),
                    "author": self.fake.name(),
                    "date": self.fake.date_this_year().isoformat(),
                    "helpful_votes": random.randint(0, 50),
                }
            )

        return {
            "reviews": reviews,
            "average_rating": round(
                sum(r["rating"] for r in reviews) / len(reviews), 1
            ),
            "total_reviews": len(reviews),
        }

    def _generate_vin(self) -> str:
        """Generate fake VIN"""
        # VIN format: 17 characters
        chars = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
        vin = "".join(random.choice(chars) for _ in range(17))
        return vin

    def _generate_page_html(self, detail_data: Dict[str, Any]) -> str:
        """Generate fake HTML page for the car detail"""
        try:
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{detail_data.get('title', 'Car Details')}</title>
            </head>
            <body>
                <div class="car-detail-page">
                    <header>
                        <h1>{detail_data.get('title', 'Car Details')}</h1>
                        <div class="price">Price: {detail_data.get('price', 'N/A')}</div>
                    </header>
                    
                    <div class="car-images">
                        <img src="{detail_data.get('images', [])[0] if detail_data.get('images') else ''}" alt="Main Image" />
                    </div>
                    
                    <div class="car-specifications">
                        <h2>Specifications</h2>
                        <ul>
                            <li>Year: {detail_data.get('year', 'N/A')}</li>
                            <li>Mileage: {detail_data.get('mileage', 'N/A')}</li>
                            <li>Engine: {detail_data.get('engine', 'N/A')}</li>
                            <li>Transmission: {detail_data.get('transmission', 'N/A')}</li>
                            <li>Fuel Type: {detail_data.get('fuel_type', 'N/A')}</li>
                            <li>Color: {detail_data.get('exterior_color', 'N/A')}</li>
                        </ul>
                    </div>
                    
                    <div class="dealer-info">
                        <h2>Dealer Information</h2>
                        <p>Name: {detail_data.get('dealer', {}).get('name', 'N/A')}</p>
                        <p>Phone: {detail_data.get('dealer', {}).get('phone', 'N/A')}</p>
                        <p>Address: {detail_data.get('dealer', {}).get('address', 'N/A')}</p>
                    </div>
                    
                    <div class="description">
                        <h2>Description</h2>
                        <p>{detail_data.get('description', 'No description available.')}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return html.strip()

        except Exception as e:
            self.logger.error(f"Error generating page HTML: {e}")
            return "<html><body>Error generating page</body></html>"
