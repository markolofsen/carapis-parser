"""
Demo Parser Logger
Simple and efficient logging for demo parser module
"""
import logging
import os
from datetime import datetime
import shutil

from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
from rich.console import Console

os.environ["DEMO_PARSER_LOGS"] = "true"

# Log directory for demo parser
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')


class DemoParserLogger:
    """Logger for demo parser with rich progress support"""

    def __init__(self, name: str, use_global: bool = False):
        self.name = name
        self.logger = logging.getLogger(name)
        self.use_global = use_global

        # Set log level
        self.logger.setLevel(logging.INFO)

        # CRITICAL: Prevent propagation to parent loggers (especially root)
        self.logger.propagate = False

        # Remove all StreamHandlers (никогда не добавляем их!)
        self.logger.handlers = [h for h in self.logger.handlers if not isinstance(h, logging.StreamHandler)]

        # File handler (always create)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Rich console for progress (always create, but control output via _console)
        self.rich_console = Console()
        self.progress = None

    def _console(self, message: str, level: str = "info"):
        # Always check environment variable for console output
        env_console = os.environ.get("DEMO_PARSER_LOGS", "false").lower() == "true"

        # Always show errors, regardless of verbose setting
        if level == "error":
            self.rich_console.print(f"[bold red]{message}[/bold red]")
            return

        # Only print other messages to console if env is enabled
        if not env_console:
            return

        if level == "warning":
            self.rich_console.print(f"[yellow]{message}[/yellow]")
        elif level == "success":
            self.rich_console.print(f"[green]{message}[/green]")
        else:
            self.rich_console.print(message)

    def info(self, message: str):
        self.logger.info(message)
        self._console(message, "info")

    def error(self, message: str):
        self.logger.error(message)
        self._console(message, "error")

    def warning(self, message: str):
        self.logger.warning(message)
        self._console(message, "warning")

    def debug(self, message: str):
        self.logger.debug(message)
        self._console(message, "debug")

    def success(self, message: str):
        msg = f"✅ {message}"
        self.logger.info(msg)
        self._console(msg, "success")

    def fail(self, message: str):
        msg = f"❌ {message}"
        self.logger.error(msg)
        self._console(msg, "error")

    def create_progress(self, total: int, description: str = "Progress"):
        """Create and return a rich progress bar"""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.rich_console,
            transient=True
        )
        task_id = self.progress.add_task(description, total=total)
        return self.progress, task_id


def get_logger(name: str, use_global: bool = False) -> DemoParserLogger:
    """Get or create a logger instance"""
    return DemoParserLogger(name, use_global)


def clear_logs():
    """Clear all logs"""
    if os.path.exists(log_dir):
        # Remove all files in log_dir
        for file in os.listdir(log_dir):
            file_path = os.path.join(log_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("🧹 Demo parser logs cleared")


def set_logger_level(enabled: bool):
    """Enable or disable console output for all loggers via env variable."""
    value = "true" if enabled else "false"
    os.environ["DEMO_PARSER_LOGS"] = value

    if enabled:
        print("🔧 Demo parser verbose mode enabled")
    else:
        print("🔇 Demo parser verbose mode disabled") 