# 🚀 Quick Start

## Getting Started (Step-by-Step)

### 1. Explore the Structure
```bash
cd backend/django/parsers/parser_demo
ls -la
# You'll see: module/, tests/, cli.py, cli_db.py, @docs/, samples/, tutorial.py
```

### 2. Run the Interactive Tutorial 🎓
```bash
# Start the interactive tutorial
python tutorial.py

# The tutorial will guide you through:
# • Parser architecture overview
# • Configuration management
# • Database setup
# • Listing and detail parsing
# • Adapter integration
# • Sample HTML files
# • Testing procedures
# • Interactive demos
```

### 3. Run the Demo
```bash
# Start interactive CLI
python cli.py

# Try different options:
# 1. Parse listings (fake mode)
# 2. Parse details  
# 3. Run full pipeline
# 4. Show pipeline info
```

### 4. Check the Database
```bash
# Database CLI
python cli_db.py

# Options:
# 1. Show statistics
# 2. Clear all data
# 3. Show database info
```

### 5. Run Tests
```bash
cd backend/django
pytest parsers/parser_demo/tests/ -v
```

### 6. Study the Code
- Start with `module/config.py` (configuration)
- Then `module/database/` (data persistence)
- Then `module/core/` (parsing logic)
- Finally `module/adapter.py` (Data Server integration)

### 7. Explore Sample HTML Files 📄
```bash
# Check sample HTML files
ls samples/html/
# • listing_page.html - Car listings with pagination
# • detail_page.html - Detailed car information
# • brands_page.html - Brand navigation page

# Use samples for testing your extractors
python -c "
from pathlib import Path
with open('samples/html/listing_page.html', 'r') as f:
    html = f.read()
print('Sample HTML loaded successfully!')
"
```

## Basic Usage

```python
from parsers.parser_demo.module import DemoParser, DemoConfig

# Create configuration
config = DemoConfig(
    max_brands=5,
    fake_mode=True,
    timeout=60
)

# Run full pipeline
parser = DemoParser(config)
result = await parser.run_full_parsing()
print(f"Parsed {result['listings_count']} listings")
```

## CLI Usage

```bash
# Run interactive CLI
cd backend/django
python parsers/parser_demo/cli.py

# Run database CLI
python parsers/parser_demo/cli_db.py

# Run interactive tutorial
python parsers/parser_demo/tutorial.py

# Database will be automatically created at:
# parsers/parser_demo/data/demo_parser.db
```

## HTTP Client with Auto-Proxy

```python
from parsers.http_client.module import HttpWorkerManager
from parsers.parser_demo.module.config import DemoConfig

# Create HTTP worker manager with auto-proxy rotation
worker_manager = await HttpWorkerManager.create_for_service(
    service_name="demo_parser",
    num_workers=5,
    use_smart_manager=True,
    timeout=60
)

# Process URLs with automatic proxy assignment
async def url_processor(url: str, context: dict) -> dict:
    http_manager = context['http_manager']
    response = await http_manager.get_html(url)
    return {
        'success': response['success'],
        'data': response['content'],
        'url': url
    }

results = await worker_manager.process_urls_batch(
    urls=["https://demo.com/1", "https://demo.com/2"],
    url_processor=url_processor
)
```

## Data Server Integration

```python
from parsers.parser_demo.module.adapter import DemoDataServerAdapter
from parsers.parser_demo.module.config import DemoConfig

# Create adapter
config = DemoConfig(max_brands=3, fake_mode=True)
adapter = DemoDataServerAdapter(
    service_id="demo_service_001",
    config=config
)

# Execute task
result = await adapter.execute_task({
    "urls": ["https://demo.com"],
    "brands": ["brand1", "brand2"]
})
```

## Testing with Sample HTML

```python
from pathlib import Path
from parsers.parser_demo.module.core.listing_parser.extractor import DemoListingExtractor

# Load sample HTML
samples_dir = Path("parsers/parser_demo/samples/html")
with open(samples_dir / "listing_page.html", "r") as f:
    html_content = f.read()

# Test extractor
extractor = DemoListingExtractor()
cars = extractor.extract_cars_from_html(html_content)
print(f"Found {len(cars)} cars in sample HTML")
```

## Configuration

```python
class DemoConfig(BaseModel):
    # Parser settings
    max_brands: int = 5
    max_pages_per_brand: int = 3
    max_urls: int = 100

    # HTTP client settings
    max_workers: int = 3
    timeout: int = 60
    max_retries: int = 2
    use_smart_manager: bool = True

    # Demo settings
    fake_mode: bool = False
    enable_random_errors: bool = False
```

## Running Tests

```bash
# Run all tests
cd backend/django
pytest parsers/parser_demo/tests/ -v

# Run async tests only
pytest parsers/parser_demo/tests/ -v -k "async"

# Run specific test
pytest parsers/parser_demo/tests/test_database.py::test_async_database_operations -v
```

## 🎯 Learning Path

1. **Start with Tutorial** (`python tutorial.py`) - Interactive guided tour
2. **Explore Samples** (`samples/html/`) - Study HTML structure
3. **Run CLI** (`python cli.py`) - Test functionality
4. **Read Documentation** (`@docs/`) - Deep dive into components
5. **Run Tests** - Understand testing patterns
6. **Create Your Parser** - Apply what you learned 