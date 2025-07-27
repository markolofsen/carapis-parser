# 🌐 HTTP Client

## Features
- Asynchronous HTTP requests
- Worker pool
- Automatic proxy rotation (SmartProxyManager)
- Progress and retry logic

## Example
```python
from parsers.http_client.module import HttpWorkerManager

worker_manager = await HttpWorkerManager.create_for_service(
    service_name="demo_parser",
    num_workers=5,
    use_smart_manager=True
)

results = await worker_manager.process_urls_batch(
    urls=["https://demo.com/1", "https://demo.com/2"],
    url_processor=my_processor
)
```

## Key Points
- Always use the worker manager for parsing
- Proxy and retry are handled automatically 