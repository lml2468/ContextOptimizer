#!/usr/bin/env python3
"""
Simple script to start the ContextOptimizer backend with direct configuration.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Create data directories if they don't exist
data_dir = backend_dir / "data"
upload_dir = data_dir / "uploads"
session_dir = data_dir / "sessions"
logs_dir = backend_dir / "logs"

# Create directories with proper structure
upload_dir.mkdir(parents=True, exist_ok=True)
session_dir.mkdir(parents=True, exist_ok=True)
logs_dir.mkdir(parents=True, exist_ok=True)

# Create test data directory for sample files
test_data_dir = backend_dir / "test_data"
test_data_dir.mkdir(parents=True, exist_ok=True)

# Override the settings in app/config.py
os.environ["OVERRIDE_ALLOWED_ORIGINS"] = "true"
os.environ["SESSION_DIR"] = str(session_dir)
os.environ["UPLOAD_DIR"] = str(upload_dir)
os.environ["LOG_DIR"] = str(logs_dir)

# Set other environment variables if needed
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("LOG_LEVEL", "INFO")
os.environ.setdefault("LOG_FILE", str(logs_dir / "context_optimizer.log"))

if __name__ == "__main__":
    import uvicorn
    
    print("Starting ContextOptimizer Backend...")
    print(f"Data directory: {data_dir}")
    print(f"Session directory: {session_dir}")
    print(f"Logs directory: {logs_dir}")
    print("Host: 0.0.0.0")
    print("Port: 8080")
    print("Debug: True")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info",
        access_log=True
    )
