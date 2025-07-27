# 🧠 Notes & Best Practices

## Async Patterns

### Django 5.2 Async ORM
- Use `a`-prefixed methods (`aget`, `acreate`, `aupdate`, `adelete`) for async database operations
- Use `async for` to iterate over QuerySets without blocking
- Always check async/sync context before operations with `is_async_context()`

### Context-Aware Operations
```python
import asyncio

def is_async_context():
    """Check if we're in an async context."""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

async def context_aware_operation():
    """Perform operation based on context."""
    if is_async_context():
        # Use async operations
        result = await async_operation()
    else:
        # Use sync operations with sync_to_async
        result = await sync_to_async(sync_operation)()
    return result
```

## Common Issues

### Event Loop Closed
**Problem**: `RuntimeError: Event loop is closed`

**Solution**: Create new event loops in threads
```python
def run_parser_in_thread(self, service_id: str):
    """Run parser with adapter in new event loop"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.execute_parser_tasks(service_id))
    finally:
        if loop and not loop.is_closed():
            loop.close()
```

### Async/Await Errors
**Problem**: `SyntaxError: 'await' outside async function`

**Solution**: Ensure all methods using `await` are declared as `async def`
```python
# Correct
async def get_statistics(self):
    return await self.db_manager.get_statistics_from_db()

# Wrong
def get_statistics(self):
    return await self.db_manager.get_statistics_from_db()  # Error!
```

### Database Connection Issues
**Problem**: `Database access not allowed` in tests

**Solution**: Use `@pytest.mark.django_db` decorator
```python
@pytest.mark.django_db(transaction=True)
async def test_async_database_operations():
    """Test async database operations."""
    db_manager = DemoDatabaseManager()
    result = await db_manager.save_listings_batch_to_db(test_data)
    assert result > 0
```

### Import Path Issues
**Problem**: `ModuleNotFoundError` for parser modules

**Solution**: Run tests from Django project root
```bash
cd backend/django
pytest parsers/parser_demo/tests/ -v
```

## Best Practices

### Type Safety
- Use Pydantic v2 validation for configuration integrity
- Always define proper type hints for async functions

### Modular Design
- Clear separation between extraction, parsing, and storage
- Each module has a single responsibility (KISS principle)

### Error Handling
- Comprehensive error handling for async operations
- Use try/catch blocks with proper logging
- Implement fallback strategies for failed operations

### Performance
- Use non-blocking I/O operations for better scalability
- Implement batch processing for database operations
- Use worker pools for concurrent HTTP requests

### Testing
- Write comprehensive async test coverage
- Mock external services in tests
- Test edge cases and error scenarios
- Use isolated test databases

### Database Operations
- Always use the database manager for operations
- Use async/await for all database calls
- Implement proper transaction handling
- Use batch operations for better performance

### HTTP Client
- Always use the worker manager for parsing
- Enable auto-proxy rotation for reliability
- Implement proper retry logic
- Monitor proxy success/failure rates

### Configuration
- Use Pydantic for configuration validation
- Provide sensible defaults
- Support environment variable overrides
- Document all configuration options

### Logging
- Use structured logging throughout
- Log async operations with proper context
- Include error details in log messages
- Use appropriate log levels

### Code Organization
- Follow the established pipeline structure
- Keep functions small and focused
- Use descriptive variable and function names
- Add comprehensive docstrings

### Data Server Integration
- Implement proper adapter patterns
- Handle async task execution
- Provide progress tracking
- Emit events for monitoring

### CLI Management
- Provide interactive CLI for testing
- Include database management tools
- Show clear progress indicators
- Handle user input gracefully 