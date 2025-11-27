#!/usr/bin/env python3
"""
Standalone runner for the Geometrize API.
Usage: python run.py [--host 0.0.0.0] [--port 8000]
"""

import sys
import argparse
import uvicorn
from geometrize_api import app

def main():
    parser = argparse.ArgumentParser(description='Geometrize API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload on code changes')
    
    args = parser.parse_args()
    
    print(f"Starting Geometrize API on {args.host}:{args.port}")
    print(f"API documentation available at http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == '__main__':
    main()
