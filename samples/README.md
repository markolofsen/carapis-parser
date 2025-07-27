# 📁 Sample Files

This directory contains sample HTML files for testing and learning the Demo Parser.

## 📄 HTML Samples

### `html/listing_page.html`
**Purpose**: Sample listing page with car items and pagination

**Features**:
- Multiple car items with realistic data
- Brand navigation menu
- Pagination controls
- Car specifications (price, mileage, year, fuel type)
- Location information
- Image placeholders

**Use case**: Test listing extraction logic

### `html/detail_page.html`
**Purpose**: Sample car detail page with comprehensive information

**Features**:
- Detailed car specifications
- Image gallery (main + thumbnails)
- Price and negotiation status
- Complete description with features list
- Seller information and contact details
- Detailed specifications (engine, dimensions, fuel economy)

**Use case**: Test detail extraction logic

### `html/brands_page.html`
**Purpose**: Sample brands listing page

**Features**:
- Multiple car brands with logos
- Brand statistics (car count, price range)
- Brand descriptions
- Navigation links to brand-specific pages
- Summary statistics

**Use case**: Test brand extraction logic

## 🧪 How to Use

### 1. For Testing
```python
from pathlib import Path

# Load sample HTML
samples_dir = Path("parsers/parser_demo/samples/html")
with open(samples_dir / "listing_page.html", "r") as f:
    html_content = f.read()

# Test your extractor
extractor = DemoListingExtractor()
cars = extractor.extract_cars_from_html(html_content)
print(f"Found {len(cars)} cars")
```

### 2. For Learning
- Study the HTML structure
- Understand the data patterns
- See how selectors should work
- Learn about pagination and navigation

### 3. For Development
- Use as templates for your own parsers
- Modify to match your target website structure
- Test different HTML variations

## 🎯 Sample Data Structure

### Listing Page Data
```json
{
  "id": "toyota_camry_001",
  "title": "Toyota Camry 2020",
  "url": "/car/toyota_camry_001",
  "price": "$25,000",
  "mileage": "45,000 km",
  "year": "2020",
  "fuel": "Gasoline",
  "location": "New York, NY"
}
```

### Detail Page Data
```json
{
  "id": "toyota_camry_001",
  "title": "Toyota Camry 2020",
  "price": "$25,000",
  "description": "Excellent condition Toyota Camry 2020...",
  "specifications": {
    "engine": "2.5L 4-Cylinder",
    "transmission": "Automatic",
    "mileage": "45,000 km",
    "year": "2020",
    "color": "Pearl White"
  },
  "seller": {
    "name": "Premium Auto Sales",
    "location": "New York, NY",
    "phone": "(555) 123-4567",
    "email": "sales@premiumauto.com"
  }
}
```

## 🔧 Customization

You can modify these samples to:
- Match your target website structure
- Add more realistic data
- Test edge cases
- Create different scenarios

## 📝 Notes

- All sample files are for testing purposes only
- Data is fictional and for demonstration
- HTML structure follows common car listing patterns
- Files are optimized for parser testing 