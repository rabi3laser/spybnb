-- =============================================
-- SPYBNB - Database Schema
-- Run this in Supabase SQL Editor
-- =============================================

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'starter', 'pro')),
    scan_credits INTEGER DEFAULT 3,
    stripe_customer_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scans table
CREATE TABLE IF NOT EXISTS public.scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    location TEXT NOT NULL,
    checkin_date DATE,
    checkout_date DATE,
    filters JSONB DEFAULT '{}',
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    listings_count INTEGER DEFAULT 0,
    stats JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Listings table
CREATE TABLE IF NOT EXISTS public.listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES public.scans(id) ON DELETE CASCADE,
    airbnb_id TEXT NOT NULL,
    name TEXT,
    url TEXT,
    price_per_night DECIMAL(10,2),
    total_price DECIMAL(10,2),
    rating DECIMAL(3,2),
    reviews_count INTEGER DEFAULT 0,
    host_name TEXT,
    room_type TEXT,
    bedrooms INTEGER DEFAULT 0,
    bathrooms INTEGER DEFAULT 0,
    max_guests INTEGER DEFAULT 0,
    amenities JSONB DEFAULT '[]',
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    image_url TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alerts table
CREATE TABLE IF NOT EXISTS public.alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    location TEXT NOT NULL,
    target_price DECIMAL(10,2) NOT NULL,
    alert_type TEXT DEFAULT 'below' CHECK (alert_type IN ('below', 'change', 'new')),
    filters JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    last_triggered TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions table (for Stripe)
CREATE TABLE IF NOT EXISTS public.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT,
    plan TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_scans_user_id ON public.scans(user_id);
CREATE INDEX IF NOT EXISTS idx_scans_status ON public.scans(status);
CREATE INDEX IF NOT EXISTS idx_listings_scan_id ON public.listings(scan_id);
CREATE INDEX IF NOT EXISTS idx_listings_price ON public.listings(price_per_night);
CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON public.alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_active ON public.alerts(is_active);

-- Insert demo user for testing
INSERT INTO public.users (id, email, plan, scan_credits)
VALUES ('00000000-0000-0000-0000-000000000001', 'demo@spybnb.com', 'pro', 100)
ON CONFLICT (id) DO NOTHING;
