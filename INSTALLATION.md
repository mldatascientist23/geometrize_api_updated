# Geometrize API - Installation Guide

This guide will help you install and run the Geometrize API on your system.

## System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.7 or higher
- **Go**: 1.15 or higher (for the primitive command-line tool)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies and tools

## Step-by-Step Installation

### 1. Install Go (if not already installed)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install golang-go
```

**macOS:**
```bash
brew install go
```

**Windows:**
Download and install from https://golang.org/dl/

### 2. Install the Primitive Tool

```bash
go install github.com/fogleman/primitive@latest
```

Add the Go bin directory to your PATH:

**Linux/macOS:**
```bash
export PATH=$PATH:~/go/bin
```

Add this line to your `~/.bashrc` or `~/.zshrc` for permanent changes:
```bash
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
The Go bin directory should be automatically added to PATH during installation.

### 3. Clone or Extract the Project

```bash
git clone <repository-url>
cd geometrize-api
```

Or extract the provided zip file:
```bash
unzip geometrize-api.zip
cd geometrize-api
```

### 4. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Verify Installation

Test that everything is installed correctly:

```bash
# Check Python version
python --version

# Check Go version
go version

# Check primitive binary
which primitive
primitive -h

# Check Python dependencies
pip list
```

## Running the API

### Option 1: Using the run.py script

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py --host 0.0.0.0 --port 8000
```

### Option 2: Using uvicorn directly

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn geometrize_api:app --host 0.0.0.0 --port 8000
```

### Option 3: Using the main module

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python geometrize_api.py
```

The API will start and be available at `http://localhost:8000`.

## Testing the Installation

### Health Check

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

### Run the Test Suite

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install requests
python test_api.py
```

All 11 tests should pass.

## Troubleshooting

### "primitive binary not found"

**Solution**: Ensure the primitive binary is installed and in your PATH:
```bash
go install github.com/fogleman/primitive@latest
export PATH=$PATH:~/go/bin
```

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Ensure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Address already in use" error

**Solution**: The port is already in use. Try a different port:
```bash
python run.py --port 9000
```

Or kill the process using the port:
```bash
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### "Connection refused" when testing

**Solution**: Ensure the API server is running in another terminal:
```bash
# Terminal 1: Start the API
python run.py

# Terminal 2: Run tests
python test_api.py
```

## Configuration

### Environment Variables

You can set environment variables to customize the API behavior:

```bash
# Set the host and port
export API_HOST=0.0.0.0
export API_PORT=8000

# Run the API
python run.py --host $API_HOST --port $API_PORT
```

### Performance Tuning

For better performance with large images:

1. **Reduce image size**: Use the `resize_width` and `resize_height` parameters
2. **Reduce shape count**: Start with 50-100 shapes instead of 200
3. **Use faster shape types**: Triangles are faster than ellipses

## Next Steps

1. Read the [README.md](README.md) for API documentation
2. Check out the [examples](examples/) directory for usage examples
3. Run the test suite to verify everything works: `python test_api.py`
4. Start using the API in your applications!

## Support

For issues or questions, please refer to the documentation or check the troubleshooting section above.
