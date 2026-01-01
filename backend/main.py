"""
SpyBnB - FastAPI Main Application
Airbnb competitor price monitoring for smart hosts
"""

import logging
from typing import List, Optional
from datetime import datetime
import statistics

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Query
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from models.schemas import (
    ScanRequest, ScanResponse, Scan, ScanStats, Listing,
    AlertCreate, Alert, APIResponse, ErrorResponse
)
from services import get_apify_service, get_supabase_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SpyBnB API",
    description="🕵️ Airbnb competitor price monitoring for smart hosts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check"""
    return {"status": "ok", "service": "SpyBnB API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "up",
            "database": "up",
            "scraper": "up"
        }
    }


# ============================================
# SCANS
# ============================================

async def run_scan_task(scan_id: str, request: ScanRequest, user_id: str):
    """Background task to run the actual scan"""
    apify = get_apify_service()
    supabase = get_supabase_service()
    
    try:
        # Update status to running
        await supabase.update_scan(scan_id, "running")
        
        # Scrape listings
        raw_listings = await apify.scrape_listings(
            location=request.location,
            checkin=request.checkin,
            checkout=request.checkout,
            min_price=request.min_price,
            max_price=request.max_price,
            guests=request.guests,
            currency=request.currency
        )
        
        # Transform listings
        listings = [apify.transform_listing(raw) for raw in raw_listings]
        
        # Calculate stats
        if listings:
            prices = [l["price_per_night"] for l in listings if l["price_per_night"] > 0]
            ratings = [l["rating"] for l in listings if l["rating"] > 0]
            
            stats = {
                "total_listings": len(listings),
                "avg_price": round(statistics.mean(prices), 2) if prices else 0,
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
                "median_price": round(statistics.median(prices), 2) if prices else 0,
                "avg_rating": round(statistics.mean(ratings), 2) if ratings else 0
            }
        else:
            stats = {
                "total_listings": 0,
                "avg_price": 0,
                "min_price": 0,
                "max_price": 0,
                "median_price": 0,
                "avg_rating": 0
            }
        
        # Save listings
        await supabase.save_listings(scan_id, listings)
        
        # Update scan as completed
        await supabase.update_scan(scan_id, "completed", len(listings), stats)
        
        logger.info(f"Scan {scan_id} completed with {len(listings)} listings")
        
    except Exception as e:
        logger.error(f"Scan {scan_id} failed: {str(e)}")
        await supabase.update_scan(scan_id, "failed")


@app.post("/api/scan", response_model=APIResponse, tags=["Scans"])
async def create_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Query("demo-user", description="User ID")
):
    """
    Start a new competitor scan.
    
    This will scrape Airbnb listings for the given location and return
    pricing data for all competitors.
    """
    supabase = get_supabase_service()
    
    # Create scan record
    scan = await supabase.create_scan(
        user_id=user_id,
        location=request.location,
        checkin=request.checkin,
        checkout=request.checkout,
        filters={
            "min_price": request.min_price,
            "max_price": request.max_price,
            "guests": request.guests,
            "currency": request.currency
        }
    )
    
    # Start background task
    background_tasks.add_task(run_scan_task, scan["id"], request, user_id)
    
    return APIResponse(
        success=True,
        message="Scan started successfully",
        data={"scan_id": scan["id"], "status": "pending"}
    )


@app.get("/api/scan/{scan_id}", tags=["Scans"])
async def get_scan(scan_id: str):
    """Get scan results by ID"""
    supabase = get_supabase_service()
    
    scan = await supabase.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Get listings if completed
    listings = []
    if scan.get("status") == "completed":
        listings = await supabase.get_scan_listings(scan_id)
    
    return {
        "scan": scan,
        "listings": listings
    }


@app.get("/api/scans", tags=["Scans"])
async def list_scans(
    user_id: str = Query("demo-user"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List all scans for a user"""
    supabase = get_supabase_service()
    scans = await supabase.get_user_scans(user_id, limit, offset)
    return {"scans": scans, "count": len(scans)}


# ============================================
# ALERTS
# ============================================

@app.post("/api/alerts", response_model=APIResponse, tags=["Alerts"])
async def create_alert(
    request: AlertCreate,
    user_id: str = Query("demo-user")
):
    """Create a new price alert"""
    supabase = get_supabase_service()
    
    alert = await supabase.create_alert(
        user_id=user_id,
        location=request.location,
        target_price=request.target_price,
        alert_type=request.alert_type.value,
        filters=request.filters
    )
    
    return APIResponse(
        success=True,
        message="Alert created successfully",
        data=alert
    )


@app.get("/api/alerts", tags=["Alerts"])
async def list_alerts(
    user_id: str = Query("demo-user"),
    active_only: bool = Query(True)
):
    """List all alerts for a user"""
    supabase = get_supabase_service()
    alerts = await supabase.get_user_alerts(user_id, active_only)
    return {"alerts": alerts, "count": len(alerts)}


@app.delete("/api/alerts/{alert_id}", tags=["Alerts"])
async def delete_alert(
    alert_id: str,
    user_id: str = Query("demo-user")
):
    """Delete an alert"""
    supabase = get_supabase_service()
    success = await supabase.delete_alert(alert_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return APIResponse(success=True, message="Alert deleted")


# ============================================
# STARTUP
# ============================================

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info("🕵️ SpyBnB API starting...")
    settings = get_settings()
    logger.info(f"Environment: {settings.app_env}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
