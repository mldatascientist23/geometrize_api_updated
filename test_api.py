#!/usr/bin/env python3
"""
Comprehensive test suite for the Geometrize API.
"""

import json
import requests
import sys
from pathlib import Path
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:8001"

def create_test_image(filename="test_image.png"):
    """Create a simple test image."""
    img = Image.new('RGB', (256, 256), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 100, 100], fill='red')
    draw.ellipse([150, 20, 230, 100], fill='blue')
    draw.polygon([(50, 150), (150, 150), (100, 230)], fill='green')
    img.save(filename)
    return filename

def test_health_check():
    """Test the health check endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", "API should be healthy"
    print("✓ Health check passed")

def test_root_endpoint():
    """Test the root endpoint."""
    print("Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "name" in data, "Response should contain 'name'"
    assert data["name"] == "Geometrize API", "API name should be 'Geometrize API'"
    print("✓ Root endpoint passed")

def test_json_output_triangle():
    """Test JSON output with triangle shapes."""
    print("Testing JSON output with triangle shapes...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['triangle'],
            'shape_count': 5
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()
    assert "shapes" in result, "Response should contain 'shapes'"
    assert len(result["shapes"]) == 5, f"Expected 5 shapes, got {len(result['shapes'])}"
    assert result["shapes"][0]["type"] == "triangle", "Shape type should be 'triangle'"
    print(f"✓ JSON output with triangles passed ({len(result['shapes'])} shapes)")

def test_json_output_rectangle():
    """Test JSON output with rectangle shapes."""
    print("Testing JSON output with rectangle shapes...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['rectangle'],
            'shape_count': 3
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()
    assert "shapes" in result, "Response should contain 'shapes'"
    assert len(result["shapes"]) == 3, f"Expected 3 shapes, got {len(result['shapes'])}"
    assert result["shapes"][0]["type"] == "rectangle", "Shape type should be 'rectangle'"
    print(f"✓ JSON output with rectangles passed ({len(result['shapes'])} shapes)")

def test_json_output_circle():
    """Test JSON output with circle shapes."""
    print("Testing JSON output with circle shapes...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['circle'],
            'shape_count': 3
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()
    assert "shapes" in result, "Response should contain 'shapes'"
    print(f"✓ JSON output with circles passed ({len(result['shapes'])} shapes)")

def test_svg_output():
    """Test SVG output."""
    print("Testing SVG output...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'svg',
            'shape_types': ['triangle'],
            'shape_count': 5
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.headers['content-type'] == 'image/svg+xml', "Content-Type should be 'image/svg+xml'"
    assert b'<svg' in response.content, "Response should contain SVG content"
    print("✓ SVG output passed")

def test_png_output():
    """Test PNG output."""
    print("Testing PNG output...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'png',
            'shape_types': ['triangle'],
            'shape_count': 5
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.headers['content-type'] == 'image/png', "Content-Type should be 'image/png'"
    print("✓ PNG output passed")

def test_opacity_parameter():
    """Test opacity parameter."""
    print("Testing opacity parameter...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['triangle'],
            'shape_count': 3,
            'opacity': 200
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()
    assert result["opacity"] == 200, "Opacity should be 200"
    print("✓ Opacity parameter passed")

def test_background_color():
    """Test background color parameter."""
    print("Testing background color parameter...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['triangle'],
            'shape_count': 3,
            'background_color': '#000000'
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    result = response.json()
    assert result["background_color"] == "#000000", "Background color should be #000000"
    print("✓ Background color parameter passed")

def test_invalid_output_format():
    """Test invalid output format error handling."""
    print("Testing invalid output format error handling...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'invalid',
            'shape_types': ['triangle'],
            'shape_count': 5
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✓ Invalid output format error handling passed")

def test_invalid_opacity():
    """Test invalid opacity error handling."""
    print("Testing invalid opacity error handling...")
    image_file = create_test_image()
    
    with open(image_file, 'rb') as f:
        files = {'image': f}
        data = {
            'output_format': 'json',
            'shape_types': ['triangle'],
            'shape_count': 5,
            'opacity': 300  # Invalid: > 255
        }
        response = requests.post(f"{BASE_URL}/api/generate", files=files, data=data)
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✓ Invalid opacity error handling passed")

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Geometrize API Test Suite")
    print("=" * 60)
    
    tests = [
        test_health_check,
        test_root_endpoint,
        test_json_output_triangle,
        test_json_output_rectangle,
        test_json_output_circle,
        test_svg_output,
        test_png_output,
        test_opacity_parameter,
        test_background_color,
        test_invalid_output_format,
        test_invalid_opacity,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
