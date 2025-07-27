# 🗄️ Database CLI Documentation

## 📖 Overview

Database CLI tools for Demo Parser provide comprehensive database management including migrations, data loading, and administration. Built with SQLite3 and async architecture.

## 📦 Modules

### simple_cli_db.py

**Purpose**:
Simple database management CLI without external dependencies.

**Dependencies**:
- `sqlite3`
- `questionary`
- `asyncio`

**Exports**:
- `SimpleDemoDatabaseCLI`

**Features**:
- Database setup and initialization
- Statistics and monitoring
- Test data loading
- Search and filtering
- Database reset and cleanup

---

### simple_migrate_cli.py

**Purpose**:
Migration management CLI for database schema evolution.

**Dependencies**:
- `sqlite3`
- `questionary`
- `asyncio`

**Exports**:
- `SimpleMigrationCLI`

**Features**:
- Migration status tracking
- Schema versioning
- Rollback capabilities
- Database reset with migrations

---

### module/database/migrations/

**Purpose**:
Migration system with version control and rollback support.

**Structure**:
```
migrations/
├── __init__.py
├── base_migration.py
├── migration_manager.py
└── migrations.py
```

**Exports**:
- `BaseMigration`
- `MigrationManager`
- `MIGRATIONS`

---

## 🧾 APIs (ReadMe.LLM Format)

%%README.LLM id=database_cli%%

## 🧭 Library Description

Database management CLI for Demo Parser with SQLite3 backend. Provides migration system, data loading, and administration tools.

## ✅ Rules

- Always use async/await for database operations
- Use simple_cli_db.py for basic operations
- Use simple_migrate_cli.py for schema changes
- Database file: `module/data/demo_parser.db`

## 🧪 Functions

### SimpleDemoDatabaseCLI

**Main database management interface.**

```python
cli = SimpleDemoDatabaseCLI()
await cli.main_menu()
```

**Methods**:
- `setup_database()` - Create tables and indexes
- `show_statistics()` - Display database stats
- `load_test_data()` - Insert sample data
- `search_items(term)` - Search in database
- `clear_all_data()` - Remove all records
- `reset_database()` - Delete and recreate

---

### SimpleMigrationCLI

**Migration management interface.**

```python
migrate_cli = SimpleMigrationCLI()
await migrate_cli.run_all_migrations()
```

**Methods**:
- `run_all_migrations()` - Apply pending migrations
- `show_status()` - Display migration status
- `reset_database()` - Reset with migrations
- `load_test_data()` - Insert test data

---

### MigrationManager

**Advanced migration system.**

```python
manager = MigrationManager(db_path)
await manager.migrate(target_version="003")
```

**Methods**:
- `migrate(target_version=None)` - Run migrations
- `rollback(target_version=None)` - Rollback migrations
- `get_migration_status()` - Get current status
- `reset_database()` - Complete reset

%%END%%

---

## 🔁 Flows

### Database Initialization

1. Run `simple_migrate_cli.py`
2. Select "Run All Migrations"
3. System creates tables and indexes
4. Migration status tracked in `migrations` table

**Modules**:
- `SimpleMigrationCLI`
- `MigrationManager`
- `migrations.py`

---

### Test Data Loading

1. Run `simple_cli_db.py`
2. Select "Load Test Data"
3. System inserts sample car listings
4. Data includes brands, prices, specifications

**Data Structure**:
```json
{
  "id": "toyota_0_0",
  "title": "Toyota Model 2020",
  "brand": "Toyota",
  "price": 25000,
  "year": 2020,
  "mileage": 50000
}
```

---

### Migration Workflow

1. **Create Migration**: Add new class in `migrations.py`
2. **Implement Methods**: `up()` and `down()` methods
3. **Add to List**: Include in `MIGRATIONS` array
4. **Run Migration**: Use CLI to apply changes
5. **Verify**: Check status and rollback if needed

**Example Migration**:
```python
class Migration005_AddNewField(BaseMigration):
    def __init__(self):
        super().__init__("005", "Add new field")
    
    async def up(self, connection):
        cursor = connection.cursor()
        cursor.execute('ALTER TABLE demo_items ADD COLUMN new_field TEXT')
        connection.commit()
        return True
    
    async def down(self, connection):
        # Rollback logic
        return True
```

---

### Database Reset Process

1. **Backup** (optional): Copy database file
2. **Delete**: Remove database file
3. **Recreate**: Run all migrations from scratch
4. **Load Data**: Insert fresh test data
5. **Verify**: Check tables and records

---

## 🧠 Notes

- **SQLite3**: File-based database, no server required
- **Async**: All CLI operations use async/await
- **Migrations**: Version-controlled schema changes
- **Test Data**: Sample car listings for development
- **Indexes**: Performance optimization for queries
- **Rollback**: Support for migration reversal
- **Status Tracking**: Migration history in database

## 🎯 Usage Examples

### Basic Database Setup
```bash
cd backend/django
python parsers/parser_demo/simple_migrate_cli.py
# Select: Run All Migrations
```

### Load Test Data
```bash
python parsers/parser_demo/simple_cli_db.py
# Select: Load Test Data
```

### Check Migration Status
```bash
python parsers/parser_demo/simple_migrate_cli.py
# Select: Show Status
```

### Reset Database
```bash
python parsers/parser_demo/simple_migrate_cli.py
# Select: Reset Database
```

## 📊 Database Schema

### demo_items
- `id` - Primary key
- `item_id` - Unique identifier
- `title` - Item title
- `brand` - Car brand
- `category` - Item category
- `status` - Processing status
- `listing_data` - JSON listing data
- `detail_data` - JSON detail data
- `metadata` - Additional metadata
- `tags` - Item tags
- `priority` - Processing priority
- `is_active` - Active status

### demo_statistics
- `id` - Primary key
- `parser_type` - Parser type
- `total_items` - Total items processed
- `processed_items` - Successfully processed
- `failed_items` - Failed items
- `duration_seconds` - Processing duration

### migrations
- `id` - Primary key
- `version` - Migration version
- `description` - Migration description
- `applied_at` - Application timestamp 