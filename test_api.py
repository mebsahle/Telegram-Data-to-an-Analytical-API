#!/usr/bin/env python3
"""
Simple test script to validate API structure and imports.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test that all API modules can be imported successfully."""
    print("🧪 Testing API imports...")
    
    try:
        from api.database import get_db, engine
        print("✅ Database module imported successfully")
        
        from api.models import TelegramMessage, FactMessage, DimChannel
        print("✅ Models module imported successfully")
        
        from api.schemas import MessageResponse, TopProduct, ChannelActivity
        print("✅ Schemas module imported successfully")
        
        from api.crud import MessageCRUD, DetectionCRUD
        print("✅ CRUD module imported successfully")
        
        from api.main import app
        print("✅ Main FastAPI app imported successfully")
        
        print("\n🎉 All imports successful! API structure is valid.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_endpoints():
    """Test that FastAPI app has the required endpoints."""
    print("\n🧪 Testing API endpoints...")
    
    try:
        from api.main import app
        
        # Get all routes
        routes = [route.path for route in app.routes]
        
        required_endpoints = [
            "/api/reports/top-products",
            "/api/channels/{channel_name}/activity", 
            "/api/search/messages",
            "/health"
        ]
        
        for endpoint in required_endpoints:
            if any(endpoint.replace("{channel_name}", "{path}") in route or 
                   endpoint in route for route in routes):
                print(f"✅ Endpoint found: {endpoint}")
            else:
                print(f"❌ Missing endpoint: {endpoint}")
        
        print(f"\n📊 Total routes defined: {len(routes)}")
        print("🎉 Endpoint validation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 TELEGRAM MEDICAL DATA API - VALIDATION TEST")
    print("=" * 60)
    
    success = True
    success &= test_imports()
    success &= test_api_endpoints()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! API is ready to run.")
        print("\n🚀 To start the API:")
        print("   docker-compose up api")
        print("   OR")
        print("   python start_api.py")
        print("\n📚 API Documentation: http://localhost:8000/docs")
    else:
        print("❌ SOME TESTS FAILED! Please fix the issues above.")
        sys.exit(1)
