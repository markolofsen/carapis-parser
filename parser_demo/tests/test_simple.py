#!/usr/bin/env python3
"""
Simple test script for demo parser (no Django setup)
"""

import asyncio
import sys
import os
import pytest

# Add root project to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from ..core.parser import DemoParser
from ..config import DemoConfig


@pytest.mark.asyncio
async def test_demo_parser():
    """Test demo parser functionality"""
    print("🚀 Testing Demo Parser (Simple)...")

    # Create config
    config = DemoConfig(
        max_brands=2,
        max_pages_per_brand=2,
        max_workers=3,
        timeout=30,
        listing_delay=0.1,
        detail_delay=0.2,
    )

    # Create parser
    parser = DemoParser("test_service", config, fake_mode=True)

    try:
        # Initialize
        print("📋 Initializing parser...")
        await parser.initialize()

        # Test listings parsing
        print("📋 Testing listings parsing...")
        listings_count = await parser.parse_listings(
            max_brands=2, max_pages_per_brand=1
        )
        print(f"✅ Parsed {listings_count} listings")

        # Test details parsing
        print("📋 Testing details parsing...")
        details_count = await parser.parse_details(max_urls=5)
        print(f"✅ Parsed {details_count} details")

        # Get statistics
        stats = parser.get_statistics()
        print("📊 Statistics:")
        print(f"   - Listings: {stats['listings']['total_listings']}")
        print(f"   - Details: {stats['details']['total_details']}")
        print(f"   - Duration: {stats['total_duration']}")

        # Get saved data
        saved_listings = parser.get_saved_listings()
        saved_details = parser.get_saved_details()

        print(f"💾 Saved data:")
        print(f"   - Listings: {len(saved_listings)}")
        print(f"   - Details: {len(saved_details)}")

        # Show sample data
        if saved_listings:
            print("📋 Sample listing:")
            sample_listing = saved_listings[0]
            print(f"   - Title: {sample_listing.get('title')}")
            print(f"   - Brand: {sample_listing.get('brand')}")
            print(f"   - Price: {sample_listing.get('price')}")

        if saved_details:
            print("📋 Sample detail:")
            sample_detail = saved_details[0]
            print(f"   - Title: {sample_detail.get('title')}")
            print(f"   - Brand: {sample_detail.get('brand')}")
            print(f"   - Year: {sample_detail.get('year')}")
            print(f"   - Engine: {sample_detail.get('engine')}")

        print("✅ Demo parser test completed successfully!")

    except Exception as e:
        print(f"❌ Error testing demo parser: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Cleanup - parsers don't have persistent worker managers
        print("🧹 Cleanup completed")


if __name__ == "__main__":
    asyncio.run(test_demo_parser())
