"""
Demo Data Server Adapter - integrates with data server
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from unreal_utils.logger import get_logger
from unreal_adapter.configs.config import ServiceType, ServiceConfig, ParserConfig
from .config import DemoConfig
from .core.parser import DemoParser

logger = get_logger("demo_adapter")


class DemoDataServerAdapter:
    """Demo adapter for testing and development"""

    def __init__(self, service_id: str, config=None):
        self.service_id = service_id
        self.config = DemoConfig(**(config or {}))
        self.parser = DemoParser(
            service_id=self.service_id,
            config=self.config,
            fake_mode=self.config.fake_mode,
        )
        self.logger = get_logger("demo_adapter")

    def get_adapter_config(self):
        """Get adapter configuration"""
        return {
            "adapter_type": "demo",
            "name": "Demo Parser Adapter",
            "description": "Adapter for demo parser with async architecture",
            "version": "1.0.0",
            "author": "Development Team"
        }

    def get_service_configs(self):
        """Get service configurations using unreal_adapter configs"""
        parser_config = ParserConfig(
            parser_type="demo",
            name="Demo Parser",
            description="Demo parser for testing and development",
            capabilities={
                "parse_listings": True,
                "parse_details": True,
                "parse_html": True
            },
            methods=["parse_listings", "parse_details", "parse_html"],
            timeout=300,
            retry_attempts=3,
            retry_delay=5,
            max_concurrent_tasks=10
        )
        
        services = [
            ServiceConfig(
                service_type=ServiceType.LISTING,
                name="Demo Listing Service",
                parser_config=parser_config,
                num_workers=2,
                timeout=300
            ),
            ServiceConfig(
                service_type=ServiceType.DETAIL,
                name="Demo Detail Service", 
                parser_config=parser_config,
                num_workers=1,
                timeout=600
            ),
            ServiceConfig(
                service_type=ServiceType.HTML_PAGES,
                name="Demo HTML Service",
                parser_config=parser_config,
                num_workers=1,
                timeout=300
            )
        ]
        
        return services

    async def execute_task(self, task_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a parsing task"""
        try:
            self.logger.info(f"Executing task: {task_type}")
            
            if task_type == "parse_listings":
                return await self._parse_listings(parameters)
            elif task_type == "parse_details":
                return await self._parse_details(parameters)
            elif task_type == "parse_html":
                return await self._parse_html(parameters)
            else:
                return {
                    "success": False,
                    "error": f"Unknown task type: {task_type}"
                }
                
        except Exception as e:
            self.logger.error(f"Error executing task {task_type}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_parser_statistics(self) -> Dict[str, Any]:
        """Get parser statistics"""
        try:
            stats = self.parser.get_statistics()
            return {
                "success": True,
                "statistics": stats
            }
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _parse_listings(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse listings"""
        try:
            max_brands = parameters.get("max_brands", 2)
            max_pages_per_brand = parameters.get("max_pages_per_brand", 1)
            
            await self.parser.initialize()
            listings_count = await self.parser.parse_listings(max_brands, max_pages_per_brand)
            
            return {
                "success": True,
                "task": "parse_listings",
                "listings_count": listings_count,
                "statistics": self.parser.get_statistics(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _parse_details(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse details"""
        try:
            max_urls = parameters.get("max_urls", 5)
            
            await self.parser.initialize()
            details_count = await self.parser.parse_details(max_urls)
            
            return {
                "success": True,
                "task": "parse_details",
                "details_count": details_count,
                "statistics": self.parser.get_statistics(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _parse_html(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse HTML pages"""
        try:
            max_urls = parameters.get("max_urls", 5)
            
            await self.parser.initialize()
            html_count = await self.parser.parse_html_pages(max_urls)
            
            return {
                "success": True,
                "task": "parse_html",
                "html_count": html_count,
                "statistics": self.parser.get_statistics(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
