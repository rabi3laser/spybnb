"""
SpyBnB - Supabase Service
Handles all database operations
"""

import logging
from typing import List, Optional
from datetime import datetime
import uuid
from supabase import create_client, Client
from config import get_settings

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for database operations via Supabase"""
    
    def __init__(self):
        settings = get_settings()
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
    
    async def create_scan(self, user_id: str, location: str, checkin: Optional[str] = None, checkout: Optional[str] = None, filters: Optional[dict] = None) -> dict:
        """Create a new scan record"""
        scan_id = str(uuid.uuid4())
        data = {
            "id": scan_id,
            "user_id": user_id,
            "location": location,
            "checkin_date": checkin,
            "checkout_date": checkout,
            "filters": filters or {},
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        result = self.client.table("scans").insert(data).execute()
        logger.info(f"Created scan: {scan_id}")
        return result.data[0] if result.data else data
    
    async def update_scan(self, scan_id: str, status: str, listings_count: int = 0, stats: Optional[dict] = None) -> dict:
        """Update scan status and results"""
        data = {
            "status": status,
            "listings_count": listings_count,
            "stats": stats or {},
            "completed_at": datetime.utcnow().isoformat() if status == "completed" else None
        }
        result = self.client.table("scans").update(data).eq("id", scan_id).execute()
        logger.info(f"Updated scan {scan_id}: {status}")
        return result.data[0] if result.data else {}
    
    async def get_scan(self, scan_id: str) -> Optional[dict]:
        """Get scan by ID"""
        result = self.client.table("scans").select("*").eq("id", scan_id).execute()
        return result.data[0] if result.data else None
    
    async def get_user_scans(self, user_id: str, limit: int = 20, offset: int = 0) -> List[dict]:
        """Get all scans for a user"""
        result = self.client.table("scans").select("*").eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        return result.data or []
    
    async def save_listings(self, scan_id: str, listings: List[dict]) -> int:
        """Save listings from a scan"""
        if not listings:
            return 0
        for listing in listings:
            listing["scan_id"] = scan_id
            listing["id"] = str(uuid.uuid4())
        result = self.client.table("listings").insert(listings).execute()
        count = len(result.data) if result.data else 0
        logger.info(f"Saved {count} listings for scan {scan_id}")
        return count
    
    async def get_scan_listings(self, scan_id: str, limit: int = 100, offset: int = 0) -> List[dict]:
        """Get listings for a scan"""
        result = self.client.table("listings").select("*").eq("scan_id", scan_id).order("price_per_night", desc=False).range(offset, offset + limit - 1).execute()
        return result.data or []
    
    async def create_alert(self, user_id: str, location: str, target_price: float, alert_type: str = "below", filters: Optional[dict] = None) -> dict:
        """Create a price alert"""
        alert_id = str(uuid.uuid4())
        data = {
            "id": alert_id,
            "user_id": user_id,
            "location": location,
            "target_price": target_price,
            "alert_type": alert_type,
            "filters": filters or {},
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        }
        result = self.client.table("alerts").insert(data).execute()
        logger.info(f"Created alert: {alert_id}")
        return result.data[0] if result.data else data
    
    async def get_user_alerts(self, user_id: str, active_only: bool = True) -> List[dict]:
        """Get alerts for a user"""
        query = self.client.table("alerts").select("*").eq("user_id", user_id)
        if active_only:
            query = query.eq("is_active", True)
        result = query.order("created_at", desc=True).execute()
        return result.data or []
    
    async def delete_alert(self, alert_id: str, user_id: str) -> bool:
        """Delete an alert"""
        result = self.client.table("alerts").update({"is_active": False}).eq("id", alert_id).eq("user_id", user_id).execute()
        return bool(result.data)


_supabase_service: Optional[SupabaseService] = None


def get_supabase_service() -> SupabaseService:
    """Get or create SupabaseService singleton"""
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service
