#!/usr/bin/env python3
"""
Startup script for the Telegram Medical Data Analytics API.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def start_api():
    """Start the FastAPI server."""
    print("🚀 Starting Telegram Medical Data Analytics API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation: http://localhost:8000/redoc")
    print("-" * 60)
    
    # Change to api directory
    api_dir = project_root / "api"
    os.chdir(api_dir)
    
    # Start uvicorn server
    try:
        subprocess.run([
            "uvicorn", 
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 API server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_api()
