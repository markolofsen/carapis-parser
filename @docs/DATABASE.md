# 🗄️ Database Usage

## Stack
- ORM: Peewee
- DB: SQLite3 (file `data/demo_parser.db`)

## Main Classes
- `DemoDatabaseManager` — operations manager
- `DemoItem`, `DemoStatistics` — ORM models

## Save Example
```python
from parsers.parser_demo.module.database import DemoDatabaseManager

db = DemoDatabaseManager()
await db.save_listing_to_db({"id": "car1", "title": "Toyota"})
```

## Get Statistics Example
```python
stats = await db.get_statistics_from_db()
print(stats["total_items"])
```

## Best Practices
- Always use the manager for operations
- Use async/await
- For tests — use a separate DB or mocks 