# Geometrize API

A powerful RESTful API service for transforming images into geometric art using shape-based evolutionary algorithms. This API converts images into geometric primitives (triangles, rectangles, circles, ellipses, and more) and returns the results in multiple formats: SVG, PNG, or JSON.

## Features

- **Multiple Shape Types**: Support for triangles, rectangles, ellipses, circles, rotated rectangles, rotated ellipses, lines, and Bézier curves
- **Flexible Output Formats**: Generate SVG (vector), PNG (raster), or JSON (shape data)
- **Customizable Parameters**: Control shape count, opacity, mutations, and more
- **Image Resizing**: Automatically resize images before processing
- **Background Color Control**: Specify custom background colors
- **Evolutionary Algorithm**: Uses hill-climbing optimization to find the best shapes for approximating the input image

## Installation

### Prerequisites

- Python 3.7+
- Go 1.15+ (for the `primitive` command-line tool)
- pip (Python package manager)

### Setup

1. **Install the primitive command-line tool**:

```bash
go install github.com/fogleman/primitive@latest
```

Make sure the `primitive` binary is in your PATH. If not, add it:

```bash
export PATH=$PATH:~/go/bin
```

2. **Clone or download this project**:

```bash
git clone <repository-url>
cd geometrize-api
```

3. **Create a virtual environment** (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

## Running the API

Start the API server using uvicorn:

```bash
uvicorn geometrize_api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### Health Check

To verify the API is running correctly:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "primitive_binary": "/path/to/primitive"
}
```

## API Endpoints

### POST /api/generate

Transform an image into geometric art.

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | File | Yes | - | The image file to transform (PNG, JPG, JPEG, WebP) |
| `output_format` | String | Yes | - | Output format: `svg`, `png`, or `json` |
| `shape_types` | List[String] | No | `["triangle"]` | Shape types to use. Options: `triangle`, `rectangle`, `ellipse`, `circle`, `rotated_rectangle`, `rotated_ellipse`, `line`, `quadratic_bezier` |
| `opacity` | Integer | No | 128 | Shape opacity (0-255) |
| `shape_count` | Integer | No | 200 | Total number of shapes to generate |
| `mutations_per_step` | Integer | No | 30 | Number of mutations per generation step |
| `random_shapes` | Integer | No | 50 | Number of random shapes to test each step |
| `background_color` | String | No | Auto-detected | Hex color for background (e.g., `#FFFFFF`) |
| `resize_width` | Integer | No | - | Resize image width before processing |
| `resize_height` | Integer | No | - | Resize image height before processing |

**Response Formats:**

#### SVG Output

Returns an SVG image as `image/svg+xml`:

```bash
curl -X POST http://localhost:8000/api/generate \
  -F "image=@photo.jpg" \
  -F "output_format=svg" \
  -F "shape_types=triangle" \
  -F "shape_count=200" > output.svg
```

#### PNG Output

Returns a PNG image as `image/png`:

```bash
curl -X POST http://localhost:8000/api/generate \
  -F "image=@photo.jpg" \
  -F "output_format=png" \
  -F "shape_types=rectangle" \
  -F "shape_count=150" > output.png
```

#### JSON Output

Returns shape data as `application/json`:

```bash
curl -X POST http://localhost:8000/api/generate \
  -F "image=@photo.jpg" \
  -F "output_format=json" \
  -F "shape_types=circle" \
  -F "shape_count=100"
```

**JSON Response Example:**

```json
{
  "shapes": [
    {
      "type": "triangle",
      "color": "#ff0000",
      "opacity": 128,
      "points": [[10, 20], [40, 25], [15, 45]]
    },
    {
      "type": "circle",
      "color": "#0000ff",
      "opacity": 200,
      "center": [100, 100],
      "radius": 50
    },
    {
      "type": "rectangle",
      "color": "#00ff00",
      "opacity": 150,
      "x": 50,
      "y": 50,
      "width": 100,
      "height": 75
    }
  ],
  "canvas_size": [400, 400],
  "background_color": "#ffffff",
  "shape_types": ["triangle", "circle", "rectangle"],
  "shape_count": 100,
  "opacity": 128
}
```

### GET /

API information endpoint.

Returns basic information about the API:

```bash
curl http://localhost:8000/
```

**Response:**

```json
{
  "name": "Geometrize API",
  "version": "1.0.0",
  "description": "Transform images into geometric art using shape-based evolutionary algorithms",
  "endpoints": {
    "generate": {
      "path": "/api/generate",
      "method": "POST",
      "description": "Generate a geometrized version of an image"
    },
    "health": {
      "path": "/health",
      "method": "GET",
      "description": "Health check endpoint"
    }
  }
}
```

### GET /health

Health check endpoint.

Returns the current status of the API and the path to the primitive binary:

```bash
curl http://localhost:8000/health
```

**Response:**

```json
{
  "status": "healthy",
  "primitive_binary": "/home/user/go/bin/primitive"
}
```

## Shape Types

The API supports the following shape types:

| Shape Type | Description | Example |
|------------|-------------|---------|
| `triangle` | Three-point polygon | Points: `[[x1, y1], [x2, y2], [x3, y3]]` |
| `rectangle` | Axis-aligned rectangle | Properties: `x`, `y`, `width`, `height` |
| `rotated_rectangle` | Rotated rectangle | Properties: `x`, `y`, `width`, `height`, `angle` |
| `ellipse` | Axis-aligned ellipse | Properties: `center`, `rx`, `ry` |
| `rotated_ellipse` | Rotated ellipse | Properties: `center`, `rx`, `ry`, `angle` |
| `circle` | Circle | Properties: `center`, `radius` |
| `line` | Line segment | Points: `[[x1, y1], [x2, y2]]` |
| `quadratic_bezier` | Quadratic Bézier curve | Points: `[[x1, y1], [x2, y2], [x3, y3]]` |

## Usage Examples

### Python

```python
import requests
import json

# Prepare the request
with open('image.jpg', 'rb') as f:
    files = {'image': f}
    data = {
        'output_format': 'json',
        'shape_types': ['triangle', 'rectangle'],
        'shape_count': 200,
        'opacity': 150
    }
    
    response = requests.post(
        'http://localhost:8000/api/generate',
        files=files,
        data=data
    )
    
    result = response.json()
    print(json.dumps(result, indent=2))
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function geometrizeImage() {
  const form = new FormData();
  form.append('image', fs.createReadStream('image.jpg'));
  form.append('output_format', 'json');
  form.append('shape_types', 'triangle');
  form.append('shape_count', '200');
  form.append('opacity', '150');

  try {
    const response = await axios.post(
      'http://localhost:8000/api/generate',
      form,
      { headers: form.getHeaders() }
    );
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

geometrizeImage();
```

### cURL

```bash
# Generate JSON output
curl -X POST http://localhost:8000/api/generate \
  -F "image=@image.jpg" \
  -F "output_format=json" \
  -F "shape_types=triangle" \
  -F "shape_count=200" \
  -F "opacity=150"

# Generate SVG output
curl -X POST http://localhost:8000/api/generate \
  -F "image=@image.jpg" \
  -F "output_format=svg" \
  -F "shape_types=rectangle,circle" \
  -F "shape_count=150" \
  -o output.svg

# Generate PNG output with custom background
curl -X POST http://localhost:8000/api/generate \
  -F "image=@image.jpg" \
  -F "output_format=png" \
  -F "shape_types=ellipse" \
  -F "shape_count=250" \
  -F "background_color=#000000" \
  -o output.png
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters or image) |
| 500 | Internal Server Error (processing failed) |

**Error Response Example:**

```json
{
  "detail": "Invalid image file: cannot identify image file"
}
```

## Performance Considerations

- **Image Size**: Smaller input images (256x256 to 512x512) process faster
- **Shape Count**: More shapes take longer to compute. Start with 50-200 shapes
- **Timeout**: Processing can take 10-60 seconds depending on image size and shape count
- **Parallelization**: The primitive tool uses all available CPU cores by default

## Troubleshooting

### "primitive binary not found"

Ensure the `primitive` binary is installed and in your PATH:

```bash
which primitive
export PATH=$PATH:~/go/bin
```

### "Invalid image file"

Ensure the image file is a valid PNG, JPG, JPEG, or WebP file.

### "Timeout" errors

Reduce the `shape_count` parameter or resize the image to a smaller size.

### Empty shapes in JSON output

This can occur if the SVG parsing fails. Check the server logs for detailed error messages.

## API Status and Monitoring

Monitor the API health using the `/health` endpoint:

```bash
watch -n 5 'curl -s http://localhost:8000/health | jq .'
```

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or feature requests, please refer to the documentation or contact the development team.

## Version History

### v1.0.0 (2025-11-26)

- Initial release
- Support for 8 shape types
- SVG, PNG, and JSON output formats
- Image resizing and background color customization
- Comprehensive API documentation
- Full test coverage for all shape types
