# 🧪 Testing

## Async Tests (pytest + Django 5.2)

- Use `@pytest.mark.asyncio` for async tests
- For DB access — use `@pytest.mark.django_db`
- Run tests from the Django project root

## Example
```python
import pytest
from parsers.parser_demo.module.database import DemoDatabaseManager

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_save_listing():
    db = DemoDatabaseManager()
    result = await db.save_listing_to_db({"id": "car1", "title": "Toyota"})
    assert result is True
```

## Run
```bash
cd backend/django
pytest parsers/parser_demo/tests/ -v
```

## Best Practices
- Isolate test data
- Mock external services
- Test edge cases 