"""
Demo Data Server Adapter - Simplified implementation
"""

from typing import Dict, Any, Optional
import asyncio
import random
from datetime import datetime

from src.data_server.core.adapters.base_adapter import BaseParserAdapter
from src.data_server.core.adapters.config import (
    AdapterType,
    ServiceType,
    SchedulerConfig,
    DefaultPreset,
    AdapterConfig,
    BaseServiceConfig,
)
from src.data_server.core.managers.service import ServiceManager
from parsers.tools.module.logger import get_logger
from ..module.core.parser import DemoParser
from ..module.config import DemoConfig

logger = get_logger("demo_adapter")


class DemoDataServerAdapter(BaseParserAdapter):
    """Demo adapter for testing and development"""

    # Adapter configuration
    ADAPTER_CONFIG = AdapterConfig(
        adapter_type="demo",
        name="Demo Parser Adapter",
        description="Demo parser adapter for testing and development purposes",
        services_configs=[
            BaseServiceConfig(
                service_id="demo_listing_001",
                name="Demo Listing Service",
                service_type=ServiceType.LISTING,
                max_workers=2,
                timeout=300,
                scheduler=SchedulerConfig(
                    enabled=True,
                    auto_start=False,
                    check_interval=3600,
                    max_retries=3,
                    retry_delay=300,
                    default_preset=DefaultPreset.DAILY_MORNING,
                ),
            ),
            BaseServiceConfig(
                service_id="demo_detail_001",
                name="Demo Detail Service",
                service_type=ServiceType.DETAIL,
                max_workers=1,
                timeout=600,
                scheduler=SchedulerConfig(
                    enabled=True,
                    auto_start=False,
                    check_interval=7200,
                    max_retries=3,
                    retry_delay=300,
                    default_preset=DefaultPreset.WEEKLY_DEEP_SCAN,
                ),
            ),
            BaseServiceConfig(
                service_id="demo_html_001",
                name="Demo Html_Pages Service",
                service_type=ServiceType.HTML_PAGES,
                max_workers=1,
                timeout=300,
                scheduler=SchedulerConfig(
                    enabled=True,
                    auto_start=False,
                    check_interval=7200,
                    max_retries=3,
                    retry_delay=300,
                    default_preset=DefaultPreset.WEEKLY_DEEP_SCAN,
                ),
            ),
            BaseServiceConfig(
                service_id="demo_search_001",
                name="Demo Search Service",
                service_type=ServiceType.SEARCH,
                max_workers=1,
                timeout=300,
                scheduler=SchedulerConfig(
                    enabled=False,
                    auto_start=False,
                    check_interval=3600,
                    max_retries=3,
                    retry_delay=300,
                    default_preset=DefaultPreset.MANUAL_CONTROL,
                ),
            ),
        ],
        default_presets={
            ServiceType.LISTING: DefaultPreset.DAILY_MORNING,
            ServiceType.DETAIL: DefaultPreset.WEEKLY_DEEP_SCAN,
            ServiceType.SEARCH: DefaultPreset.MANUAL_CONTROL,
            ServiceType.HTML_PAGES: DefaultPreset.WEEKLY_DEEP_SCAN,
        },
        version="1.0.0",
        author="Development Team",
    )

    def __init__(self, service_id: str, config=None):
        # Create DemoConfig from dict or use default
        demo_config = DemoConfig(**(config or {}))

        super().__init__(
            self.ADAPTER_CONFIG,
            demo_config.model_dump(),
            service_id=service_id,
        )
        self.config = demo_config
        # Pass service_id AND fake_mode to DemoParser so it can use it for HttpWorkerManager
        self.parser = DemoParser(
            service_id=self.service_id,
            config=self.config,
            fake_mode=self.config.fake_mode,
        )
        self.parser_type = AdapterType.DEMO

        self.logger.info(
            "DemoDataServerAdapter",
            f"Created DemoParser with service_id: {self.service_id}, fake_mode={self.config.fake_mode}",
        )

    def start(self) -> bool:
        """Start the adapter with dynamic configuration from DB"""
        # Call parent start method which gets workers and scheduler config from DB
        result = super().start()

        # Simple scheduler check - if enabled, just log it
        if self.is_scheduler_enabled():
            self.logger.info(
                "DemoDataServerAdapter",
                f"Scheduler enabled for service {self.service_id}",
            )

        return result

    async def execute_task(
        self, task_type: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute demo task"""
        self.logger.info(f"🚀 DEMO ADAPTER: execute_task called")
        self.logger.info(f"   Task type: {task_type}")
        self.logger.info(f"   Parameters: {parameters}")
        self.logger.info(f"   Fake mode: {self.config.fake_mode}")
        self.logger.info(f"   Fake DB: {self.config.fake_db}")

        try:
            self.logger.info(
                "DemoDataServerAdapter",
                f"Executing task {task_type} for service {self.service_id}",
            )
            await self._log_task_start(task_type, parameters)

            # Initialize parser before executing tasks to ensure HttpWorkerManager is ready
            self.logger.info(f"🚀 DEMO ADAPTER: Initializing parser...")
            await self.parser.initialize()
            self.logger.info(f"✅ DEMO ADAPTER: Parser initialized")

            # Simulate processing delay
            await asyncio.sleep(random.uniform(0.1, 0.5))

            if task_type == "parse_listings":
                self.logger.info(f"🚀 DEMO ADAPTER: Starting parse_listings task")
                result = await self._parse_listings(parameters)
            elif task_type == "parse_details":
                self.logger.info(f"🚀 DEMO ADAPTER: Starting parse_details task")
                result = await self._parse_details(parameters)
            elif task_type == "parse_html":
                self.logger.info(f"🚀 DEMO ADAPTER: Starting parse_html task")
                result = await self._parse_html(parameters)
            elif task_type == "parse_search":
                self.logger.info(f"🚀 DEMO ADAPTER: Starting parse_search task")
                result = await self._parse_search(parameters)
            else:
                raise ValueError(f"Unknown task type: {task_type}")

            self.logger.info(f"✅ DEMO ADAPTER: Task completed successfully")
            self.logger.info(f"   Result: {result}")
            await self._log_task_completion(task_type, result)
            return result

        except Exception as e:
            self.logger.info(f"❌ DEMO ADAPTER: Task failed: {e}")
            await self._log_task_failure(task_type, str(e))
            raise

    def get_parser_statistics(self) -> Dict[str, Any]:
        """Get demo parser statistics with manager integration"""
        # Get base statistics
        base_stats = {
            "total_processed": self.state.total_tasks,
            "successful": self.state.completed_tasks,
            "failed": self.state.failed_tasks,
            "success_rate": (
                self.state.completed_tasks / max(self.state.total_tasks, 1)
            )
            * 100,
            "current_task": self.state.current_task,
            "is_running": self.state.is_running,
            "scheduler_enabled": self.is_scheduler_enabled(),
            "num_workers": self.get_num_workers(),
        }

        # Get service task statistics from manager
        try:
            service_task_stats = ServiceManager().get_service_task_statistics(
                self.service_id
            )
            base_stats["service_task_stats"] = service_task_stats
        except Exception as e:
            self.logger.warning(f"Failed to get service task stats: {e}")
            base_stats["service_task_stats"] = {}

        return base_stats

    async def _parse_listings(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse listings using real demo parser with HttpWorkerManager"""
        max_brands = parameters.get("max_brands", self.config.max_brands)
        max_pages = parameters.get(
            "max_pages_per_brand", self.config.max_pages_per_brand
        )

        # Use real parser method that utilizes HttpWorkerManager
        listings_count = await self.parser.parse_listings(max_brands, max_pages)

        return {
            "task_type": "parse_listings",
            "listings_count": listings_count,
            "parameters": parameters,
        }

    async def _parse_details(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse details using real demo parser with HttpWorkerManager"""
        max_urls = parameters.get("max_urls", self.config.max_urls)

        # Use real parser method that utilizes HttpWorkerManager
        details_count = await self.parser.parse_details(max_urls)

        return {
            "task_type": "parse_details",
            "details_count": details_count,
            "parameters": parameters,
        }

    async def _parse_html(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse HTML using real demo parser with HttpWorkerManager"""
        max_urls = parameters.get("max_urls", self.config.max_urls)

        # Use real parser method that utilizes HttpWorkerManager
        html_count = await self.parser.parse_html_pages(max_urls)

        return {
            "task_type": "parse_html",
            "pages_count": html_count,
            "parameters": parameters,
        }

    async def _parse_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse search demo"""
        max_results = parameters.get("max_results", 10)

        search_results = []
        for i in range(min(max_results, 10)):
            search_results.append(
                {
                    "id": f"search_{i}",
                    "query": parameters.get("query", f"search query {i}"),
                    "title": f"Search Result {i}",
                    "url": f"https://demo.com/search/result/{i}",
                    "snippet": f"This is a search result snippet for result {i}",
                    "relevance_score": random.uniform(0.1, 1.0),
                }
            )

        return {
            "task_type": "parse_search",
            "results_count": len(search_results),
            "results": search_results,
            "parameters": parameters,
        }
