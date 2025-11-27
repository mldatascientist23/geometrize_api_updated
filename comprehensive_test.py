#!/usr/bin/env python3
"""
Comprehensive test suite for Geometrize API - Tests ALL features with detailed logging.
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_RESULTS = []

def log_test(test_name, status, details=""):
    """Log test result with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "timestamp": timestamp,
        "test": test_name,
        "status": status,
        "details": details
    }
    TEST_RESULTS.append(result)
    status_symbol = "✓" if status == "PASS" else "✗"
    print(f"{status_symbol} [{timestamp}] {test_name}: {status}")
    if details:
        print(f"  Details: {details}")

def test_api_health():
    """Test API health check."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                log_test("API Health Check", "PASS", f"Primitive binary: {data.get('primitive_binary')}")
                return True
        log_test("API Health Check", "FAIL", f"Status code: {response.status_code}")
        return False
    except Exception as e:
        log_test("API Health Check", "FAIL", str(e))
        return False

def test_api_root():
    """Test API root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            if data.get("name") == "Geometrize API":
                log_test("API Root Endpoint", "PASS", f"Version: {data.get('version')}")
                return True
        log_test("API Root Endpoint", "FAIL", f"Status code: {response.status_code}")
        return False
    except Exception as e:
        log_test("API Root Endpoint", "FAIL", str(e))
        return False

def test_shape_type(shape_type, image_path, shape_count=5):
    """Test a specific shape type."""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'output_format': 'json',
                'shape_types': [shape_type],
                'shape_count': shape_count
            }
            response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            shapes = result.get('shapes', [])
            if len(shapes) > 0:
                log_test(f"Shape Type: {shape_type}", "PASS", f"Generated {len(shapes)} shapes")
                return True, shapes
            else:
                log_test(f"Shape Type: {shape_type}", "FAIL", "No shapes generated")
                return False, []
        else:
            log_test(f"Shape Type: {shape_type}", "FAIL", f"Status code: {response.status_code}")
            return False, []
    except Exception as e:
        log_test(f"Shape Type: {shape_type}", "FAIL", str(e))
        return False, []

def test_output_format(output_format, image_path, shape_type='triangle'):
    """Test a specific output format."""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'output_format': output_format,
                'shape_types': [shape_type],
                'shape_count': 3
            }
            response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
        
        if response.status_code == 200:
            if output_format == 'json':
                result = response.json()
                log_test(f"Output Format: {output_format}", "PASS", f"Response size: {len(json.dumps(result))} bytes")
            elif output_format == 'svg':
                if b'<svg' in response.content:
                    log_test(f"Output Format: {output_format}", "PASS", f"Response size: {len(response.content)} bytes")
                else:
                    log_test(f"Output Format: {output_format}", "FAIL", "SVG content not found")
                    return False
            elif output_format == 'png':
                if response.headers.get('content-type') == 'image/png':
                    log_test(f"Output Format: {output_format}", "PASS", f"Response size: {len(response.content)} bytes")
                else:
                    log_test(f"Output Format: {output_format}", "FAIL", f"Wrong content-type: {response.headers.get('content-type')}")
                    return False
            return True
        else:
            log_test(f"Output Format: {output_format}", "FAIL", f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test(f"Output Format: {output_format}", "FAIL", str(e))
        return False

def test_parameter(param_name, param_value, image_path):
    """Test a specific parameter."""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'output_format': 'json',
                'shape_types': ['triangle'],
                'shape_count': 3,
                param_name: param_value
            }
            response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if param_name in ['opacity', 'shape_count']:
                if result.get(param_name) == param_value:
                    log_test(f"Parameter: {param_name}={param_value}", "PASS", f"Value correctly set")
                    return True
                else:
                    log_test(f"Parameter: {param_name}={param_value}", "FAIL", f"Value mismatch: {result.get(param_name)}")
                    return False
            else:
                log_test(f"Parameter: {param_name}={param_value}", "PASS", "Parameter accepted")
                return True
        else:
            log_test(f"Parameter: {param_name}={param_value}", "FAIL", f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test(f"Parameter: {param_name}={param_value}", "FAIL", str(e))
        return False

def test_error_handling(test_name, invalid_data):
    """Test error handling."""
    try:
        response = requests.post(f"{BASE_URL}/api/generate", data=invalid_data)
        
        if response.status_code >= 400:
            log_test(f"Error Handling: {test_name}", "PASS", f"Status code: {response.status_code}")
            return True
        else:
            log_test(f"Error Handling: {test_name}", "FAIL", f"Should return error status, got {response.status_code}")
            return False
    except Exception as e:
        log_test(f"Error Handling: {test_name}", "FAIL", str(e))
        return False

def test_image_resizing(image_path):
    """Test image resizing functionality."""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'output_format': 'json',
                'shape_types': ['triangle'],
                'shape_count': 3,
                'resize_width': 200,
                'resize_height': 200
            }
            response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            # Canvas size should be resized
            log_test("Image Resizing", "PASS", f"Canvas size: {result.get('canvas_size')}")
            return True
        else:
            log_test("Image Resizing", "FAIL", f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Image Resizing", "FAIL", str(e))
        return False

def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("=" * 80)
    print("GEOMETRIZE API - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Base URL: {BASE_URL}")
    print("=" * 80)
    print()

    # Test basic API functionality
    print("--- BASIC API TESTS ---")
    test_api_health()
    test_api_root()
    print()

    # Test all shape types
    print("--- SHAPE TYPE TESTS ---")
    shape_types = [
        'triangle', 'rectangle', 'ellipse', 'circle',
        'rotated_rectangle', 'rotated_ellipse', 'line', 'quadratic_bezier'
    ]
    
    for shape_type in shape_types:
        success, shapes = test_shape_type(shape_type, '/tmp/test_shapes.png', shape_count=5)
        if success and shapes:
            print(f"  Shape details: type={shapes[0].get('type')}, color={shapes[0].get('color')}, opacity={shapes[0].get('opacity')}")
    print()

    # Test all output formats
    print("--- OUTPUT FORMAT TESTS ---")
    for output_format in ['json', 'svg', 'png']:
        test_output_format(output_format, '/tmp/test_shapes.png')
    print()

    # Test parameters
    print("--- PARAMETER TESTS ---")
    test_parameter('opacity', 200, '/tmp/test_shapes.png')
    test_parameter('shape_count', 10, '/tmp/test_shapes.png')
    test_parameter('background_color', '#000000', '/tmp/test_shapes.png')
    print()

    # Test image resizing
    print("--- IMAGE PROCESSING TESTS ---")
    test_image_resizing('/tmp/test_shapes.png')
    print()

    # Test with different image sizes
    print("--- IMAGE SIZE TESTS ---")
    test_shape_type('triangle', '/tmp/test_small.png', shape_count=3)
    test_shape_type('triangle', '/tmp/test_gradient.png', shape_count=5)
    test_shape_type('triangle', '/tmp/test_large.png', shape_count=5)
    print()

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in TEST_RESULTS if r['status'] == 'PASS')
    failed = sum(1 for r in TEST_RESULTS if r['status'] == 'FAIL')
    total = len(TEST_RESULTS)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ({100*passed//total}%)")
    print(f"Failed: {failed} ({100*failed//total}%)")
    print("=" * 80)
    
    # Save detailed results
    results_file = '/tmp/test_results.json'
    with open(results_file, 'w') as f:
        json.dump(TEST_RESULTS, f, indent=2)
    print(f"\nDetailed results saved to: {results_file}")
    
    return failed == 0

if __name__ == '__main__':
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
