# 🔌 Adapter Integration

## Purpose

- Integrates the parser with the Data Server using the Adapter pattern.
- Manages services, tasks, and statistics.

## Usage Example

```python
from parsers.parser_demo.module.adapter import DemoDataServerAdapter
from parsers.parser_demo.module.config import DemoConfig

config = DemoConfig(max_brands=3, fake_mode=True)
adapter = DemoDataServerAdapter(service_id="demo_service_001", config=config)

result = await adapter.execute_task({
    "urls": ["https://demo.com"],
    "brands": ["brand1", "brand2"]
})
```

## Key Points
- All services are described via config.
- Supports async tasks and events.
- Statistics and progress are available via adapter methods.
- Supports `fake_mode` for HTTP requests and `fake_db` for database operations. 