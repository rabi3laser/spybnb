"""
SpyBnB - Apify Service
Handles all Airbnb scraping via Apify actors
"""

import logging
from typing import List, Optional
from datetime import datetime
from apify_client import ApifyClientAsync
from config import get_settings

logger = logging.getLogger(__name__)


class ApifyService:
    """Service for scraping Airbnb data via Apify"""
    
    AIRBNB_SCRAPER = "tri_angle/airbnb-scraper"
    
    def __init__(self):
        settings = get_settings()
        self.token = settings.apify_api_token
        self.client = ApifyClientAsync(self.token)
    
    async def scrape_listings(
        self,
        location: str,
        checkin: Optional[str] = None,
        checkout: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        guests: int = 2,
        max_listings: int = 100,
        currency: str = "EUR"
    ) -> List[dict]:
        """Scrape Airbnb listings for a given location."""
        logger.info(f"Starting Airbnb scrape for: {location}")
        
        run_input = {
            "locationQuery": location,
            "maxListings": max_listings,
            "currency": currency,
        }
        
        if checkin:
            run_input["checkIn"] = checkin
        if checkout:
            run_input["checkOut"] = checkout
        if min_price:
            run_input["minPrice"] = min_price
        if max_price:
            run_input["maxPrice"] = max_price
        if guests:
            run_input["adults"] = guests
        
        try:
            actor_client = self.client.actor(self.AIRBNB_SCRAPER)
            run = await actor_client.call(run_input=run_input)
            
            if not run:
                logger.error("Apify Actor run failed")
                return []
            
            logger.info(f"Actor run completed: {run.get('id')}")
            
            dataset_client = self.client.dataset(run["defaultDatasetId"])
            items = await dataset_client.list_items()
            
            listings = items.items if items else []
            logger.info(f"Scraped {len(listings)} listings for {location}")
            
            return listings
            
        except Exception as e:
            logger.error(f"Apify scraping error: {str(e)}")
            raise
    
    def transform_listing(self, raw: dict) -> dict:
        """Transform raw Apify data to clean listing format."""
        price_data = raw.get("price", {})
        if isinstance(price_data, dict):
            price_per_night = price_data.get("rate", 0)
            total_price = price_data.get("total", 0)
        else:
            price_per_night = price_data if isinstance(price_data, (int, float)) else 0
            total_price = 0
        
        location_data = raw.get("location", {})
        if isinstance(location_data, dict):
            latitude = location_data.get("lat", 0)
            longitude = location_data.get("lng", 0)
        else:
            latitude = 0
            longitude = 0
        
        host_data = raw.get("host", {})
        host_name = host_data.get("name") if isinstance(host_data, dict) else None
        
        images = raw.get("images", [])
        image_url = images[0] if images else None
        
        return {
            "airbnb_id": str(raw.get("id", "")),
            "name": raw.get("name", ""),
            "url": raw.get("url", ""),
            "price_per_night": float(price_per_night or 0),
            "total_price": float(total_price or 0),
            "rating": float(raw.get("rating", 0) or 0),
            "reviews_count": int(raw.get("reviewsCount", 0) or 0),
            "host_name": host_name,
            "room_type": raw.get("roomType", ""),
            "bedrooms": int(raw.get("bedrooms", 0) or 0),
            "bathrooms": int(raw.get("bathrooms", 0) or 0),
            "max_guests": int(raw.get("persons", 0) or 0),
            "amenities": raw.get("amenities", []),
            "latitude": float(latitude or 0),
            "longitude": float(longitude or 0),
            "image_url": image_url,
            "scraped_at": datetime.utcnow().isoformat()
        }
    
    async def test_connection(self) -> bool:
        """Test if Apify connection works"""
        try:
            user = await self.client.user().get()
            logger.info(f"Apify connection OK - User: {user.get('username')}")
            return True
        except Exception as e:
            logger.error(f"Apify connection failed: {str(e)}")
            return False


_apify_service: Optional[ApifyService] = None


def get_apify_service() -> ApifyService:
    """Get or create ApifyService singleton"""
    global _apify_service
    if _apify_service is None:
        _apify_service = ApifyService()
    return _apify_service
