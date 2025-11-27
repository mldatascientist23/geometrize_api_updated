# Changelog

All notable changes to the Geometrize API project are documented in this file.

## [1.0.0] - 2025-11-26

### Added

#### Core Features
- **FastAPI Application**: RESTful API service for image geometrization
- **POST /api/generate Endpoint**: Main endpoint for transforming images into geometric art
- **Multiple Shape Types**: Full support for 8 shape types:
  - Triangle (3-point polygon)
  - Rectangle (axis-aligned)
  - Rotated Rectangle
  - Ellipse (axis-aligned)
  - Rotated Ellipse
  - Circle
  - Line (2-point)
  - Quadratic Bézier Curve
- **Output Formats**: Three output format options:
  - SVG (vector format)
  - PNG (raster format)
  - JSON (shape data)
- **Image Processing Parameters**:
  - `opacity`: Control shape transparency (0-255)
  - `shape_count`: Set total number of shapes to generate
  - `mutations_per_step`: Control evolutionary algorithm mutation rate
  - `random_shapes`: Control random shape testing per step
  - `background_color`: Specify custom background color
  - `resize_width` and `resize_height`: Pre-processing image resizing
- **SVG Parsing**: Comprehensive parser to extract shape data from generated SVG
- **Error Handling**: Proper HTTP status codes and error messages
- **Health Check**: GET /health endpoint for API status monitoring
- **API Information**: GET / endpoint with API metadata

#### Testing & Verification
- **Comprehensive Test Suite**: 11 automated tests covering:
  - Health check endpoint
  - Root endpoint information
  - JSON output with all shape types (triangle, rectangle, circle)
  - SVG output generation
  - PNG output generation
  - Parameter validation (opacity, background_color)
  - Error handling (invalid formats, invalid parameters)
- **All Tests Passing**: 100% test success rate

#### Documentation
- **README.md**: Complete API documentation with:
  - Feature overview
  - Installation instructions
  - API endpoint documentation
  - Parameter descriptions
  - Response format examples
  - Usage examples in Python, JavaScript, and cURL
  - Error handling guide
  - Performance considerations
  - Troubleshooting section
- **INSTALLATION.md**: Step-by-step installation guide covering:
  - System requirements
  - Go and primitive tool installation
  - Python environment setup
  - Dependency installation
  - Verification procedures
  - Troubleshooting common issues
  - Configuration options
  - Performance tuning tips
- **API Documentation**: Inline code documentation and docstrings
- **Test Documentation**: Comprehensive test script with clear test cases

#### Tools & Scripts
- **run.py**: Standalone runner script with command-line arguments
- **test_api.py**: Automated test suite with 11 test cases
- **requirements.txt**: Python dependency specification
- **.gitignore**: Git ignore patterns for clean repository

#### Integration
- **Primitive Tool Integration**: Seamless integration with the primitive command-line tool
- **Image Format Support**: Support for PNG, JPG, JPEG, WebP input formats
- **Multipart Form Data**: Proper handling of file uploads via HTTP

### Technical Details

#### Architecture
- **Framework**: FastAPI (modern, fast, production-ready)
- **Server**: Uvicorn (ASGI server)
- **Image Processing**: Pillow (PIL) for image manipulation
- **SVG Parsing**: XML ElementTree for shape extraction
- **External Tool**: Primitive (Go-based evolutionary algorithm)

#### Performance
- **Processing**: Leverages all available CPU cores via primitive tool
- **Timeout**: 300-second timeout for large image processing
- **Memory**: Efficient streaming responses for large outputs
- **Scalability**: Stateless design allows horizontal scaling

#### Code Quality
- **Type Hints**: Full type annotations throughout codebase
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Documentation**: Detailed docstrings and inline comments
- **Testing**: Automated test suite with 100% pass rate

### Bug Fixes
- **Shape Type Recognition**: Fixed bug where shape types were not correctly recognized and processed
- **SVG Parsing**: Improved polygon and shape data extraction from SVG output
- **Opacity Handling**: Correct conversion of opacity values (0-1 to 0-255)
- **Background Color**: Proper detection and handling of background colors

### Known Limitations
- PNG output currently uses PIL rendering (future versions may use more sophisticated rendering)
- Rotated shapes may require additional processing in some cases
- Very large images (>4000x4000) may require longer processing times

### Future Enhancements
- WebSocket support for real-time streaming
- Batch processing API for multiple images
- Advanced shape filtering and selection
- Custom color palettes
- GPU acceleration support
- Docker containerization
- Cloud deployment templates

## Version Information

- **Release Date**: November 26, 2025
- **Status**: Stable
- **Compatibility**: Python 3.7+, Go 1.15+
- **License**: Provided as-is for educational and commercial use

## Credits

This project builds upon the excellent work of:
- **Primitive**: https://github.com/fogleman/primitive (Go-based geometric art generator)
- **Geometrize**: https://github.com/Tw1ddle/geometrize-haxe (Original Haxe implementation)

## Support

For issues, questions, or feature requests, please refer to the documentation or contact the development team.
