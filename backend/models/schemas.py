"""
SpyBnB - Pydantic Models
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AlertType(str, Enum):
    BELOW = "below"
    CHANGE = "change"
    NEW = "new"


class SubscriptionPlan(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"


class ScanRequest(BaseModel):
    """Request to start a new scan"""
    location: str = Field(..., min_length=2, max_length=200, example="Paris, France")
    checkin: Optional[str] = Field(None, example="2025-02-01")
    checkout: Optional[str] = Field(None, example="2025-02-05")
    min_price: Optional[int] = Field(None, ge=0, example=50)
    max_price: Optional[int] = Field(None, ge=0, example=300)
    guests: int = Field(2, ge=1, le=16, example=2)
    currency: str = Field("EUR", example="EUR")


class AlertCreate(BaseModel):
    """Request to create a price alert"""
    location: str = Field(..., min_length=2, max_length=200)
    target_price: float = Field(..., gt=0)
    alert_type: AlertType = AlertType.BELOW
    checkin: Optional[str] = None
    checkout: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class Listing(BaseModel):
    """Airbnb listing data"""
    id: str
    airbnb_id: str
    name: str
    url: str
    price_per_night: float
    total_price: Optional[float] = 0
    rating: Optional[float] = 0
    reviews_count: Optional[int] = 0
    host_name: Optional[str] = None
    room_type: Optional[str] = None
    bedrooms: Optional[int] = 0
    bathrooms: Optional[int] = 0
    max_guests: Optional[int] = 0
    amenities: Optional[List[str]] = []
    latitude: Optional[float] = 0
    longitude: Optional[float] = 0
    image_url: Optional[str] = None
    scraped_at: datetime


class ScanStats(BaseModel):
    """Statistics for a scan"""
    total_listings: int
    avg_price: float
    min_price: float
    max_price: float
    median_price: float
    avg_rating: float


class Scan(BaseModel):
    """Scan record"""
    id: str
    user_id: str
    location: str
    checkin_date: Optional[str] = None
    checkout_date: Optional[str] = None
    filters: Optional[Dict[str, Any]] = {}
    status: ScanStatus
    listings_count: int = 0
    stats: Optional[ScanStats] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class ScanResponse(BaseModel):
    """Response for a completed scan"""
    scan: Scan
    listings: List[Listing]


class Alert(BaseModel):
    """Price alert"""
    id: str
    user_id: str
    location: str
    target_price: float
    alert_type: AlertType
    filters: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    last_triggered: Optional[datetime] = None
    created_at: datetime


class User(BaseModel):
    """User profile"""
    id: str
    email: str
    plan: SubscriptionPlan = SubscriptionPlan.FREE
    scan_credits: int = 1
    created_at: datetime


class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
