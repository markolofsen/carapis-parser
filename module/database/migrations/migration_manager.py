"""
Migration Manager for Demo Parser Database
"""

import asyncio
import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from .base_migration import BaseMigration
from .migrations import MIGRATIONS


class MigrationManager:
    """Manages database migrations"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))

    async def setup_migrations_table(self) -> bool:
        """Create migrations table if it doesn't exist"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup migrations table: {e}")
            return False

    async def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT version FROM migrations ORDER BY version')
            versions = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            return versions
            
        except Exception as e:
            print(f"❌ Failed to get applied migrations: {e}")
            return []

    async def mark_migration_applied(self, migration: BaseMigration) -> bool:
        """Mark migration as applied"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO migrations (version, description, applied_at)
                VALUES (?, ?, ?)
            ''', (migration.version, migration.description, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed to mark migration applied: {e}")
            return False

    async def mark_migration_rolled_back(self, version: str) -> bool:
        """Mark migration as rolled back"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM migrations WHERE version = ?', (version,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed to mark migration rolled back: {e}")
            return False

    async def get_migration_status(self) -> Dict[str, Any]:
        """Get migration status"""
        try:
            applied = await self.get_applied_migrations()
            all_migrations = [m.version for m in MIGRATIONS]
            
            pending = [v for v in all_migrations if v not in applied]
            
            return {
                'applied': applied,
                'pending': pending,
                'total': len(all_migrations),
                'applied_count': len(applied),
                'pending_count': len(pending)
            }
            
        except Exception as e:
            print(f"❌ Failed to get migration status: {e}")
            return {}

    async def migrate(self, target_version: Optional[str] = None) -> bool:
        """Run migrations up to target version (or latest if None)"""
        try:
            # Setup migrations table
            await self.setup_migrations_table()
            
            # Get current status
            status = await self.get_migration_status()
            applied = status.get('applied', [])
            pending = status.get('pending', [])
            
            if not pending:
                print("✅ Database is up to date")
                return True
            
            # Determine target version
            if target_version:
                if target_version in applied:
                    print(f"✅ Target version {target_version} already applied")
                    return True
                target_migrations = [v for v in pending if v <= target_version]
            else:
                target_migrations = pending
            
            print(f"🔄 Running {len(target_migrations)} migrations...")
            
            # Apply migrations
            for version in target_migrations:
                migration = next((m for m in MIGRATIONS if m.version == version), None)
                if not migration:
                    print(f"❌ Migration {version} not found")
                    continue
                
                print(f"🔄 Applying {migration}...")
                
                conn = self.get_connection()
                try:
                    success = await migration.up(conn)
                    if success:
                        await self.mark_migration_applied(migration)
                        print(f"✅ Applied {migration}")
                    else:
                        print(f"❌ Failed to apply {migration}")
                        return False
                finally:
                    conn.close()
            
            print("✅ All migrations applied successfully")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False

    async def rollback(self, target_version: Optional[str] = None) -> bool:
        """Rollback migrations to target version"""
        try:
            # Get current status
            status = await self.get_migration_status()
            applied = status.get('applied', [])
            
            if not applied:
                print("✅ No migrations to rollback")
                return True
            
            # Determine target version
            if target_version:
                if target_version not in applied:
                    print(f"❌ Target version {target_version} not applied")
                    return False
                target_migrations = [v for v in applied if v > target_version]
            else:
                # Rollback last migration
                target_migrations = [applied[-1]] if applied else []
            
            print(f"🔄 Rolling back {len(target_migrations)} migrations...")
            
            # Rollback migrations (in reverse order)
            for version in reversed(target_migrations):
                migration = next((m for m in MIGRATIONS if m.version == version), None)
                if not migration:
                    print(f"❌ Migration {version} not found")
                    continue
                
                print(f"🔄 Rolling back {migration}...")
                
                conn = self.get_connection()
                try:
                    success = await migration.down(conn)
                    if success:
                        await self.mark_migration_rolled_back(version)
                        print(f"✅ Rolled back {migration}")
                    else:
                        print(f"❌ Failed to rollback {migration}")
                        return False
                finally:
                    conn.close()
            
            print("✅ All rollbacks completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False

    async def show_status(self):
        """Show migration status"""
        try:
            status = await self.get_migration_status()
            
            print("\n📊 Migration Status:")
            print("=" * 50)
            print(f"   Total migrations: {status.get('total', 0)}")
            print(f"   Applied: {status.get('applied_count', 0)}")
            print(f"   Pending: {status.get('pending_count', 0)}")
            
            if status.get('applied'):
                print("\n✅ Applied migrations:")
                for version in status['applied']:
                    migration = next((m for m in MIGRATIONS if m.version == version), None)
                    if migration:
                        print(f"   {version}: {migration.description}")
            
            if status.get('pending'):
                print("\n⏳ Pending migrations:")
                for version in status['pending']:
                    migration = next((m for m in MIGRATIONS if m.version == version), None)
                    if migration:
                        print(f"   {version}: {migration.description}")
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Failed to show status: {e}")

    async def reset_database(self) -> bool:
        """Reset database (delete all data and migrations)"""
        try:
            # Close any existing connections
            conn = self.get_connection()
            conn.close()
            
            # Delete database file
            if self.db_path.exists():
                self.db_path.unlink()
                print("🗑️ Deleted database file")
            
            # Recreate with initial migration
            await self.migrate()
            print("✅ Database reset successfully")
            return True
            
        except Exception as e:
            print(f"❌ Database reset failed: {e}")
            return False 