# Geometrize API - Windows Setup Guide

This guide will help you set up and run the Geometrize API on Windows systems.

## Prerequisites

- **Windows 10/11** (or Windows Server 2016+)
- **Python 3.7+** (download from https://www.python.org/downloads/)
- **Go 1.15+** (download from https://golang.org/dl/)
- **Git Bash or Windows Terminal** (for running commands)

## Step 1: Install Go

1. Download Go from https://golang.org/dl/
2. Run the installer and follow the prompts
3. Go will be installed to `C:\Program Files\Go`
4. The Go bin directory will be automatically added to PATH

Verify installation:
```bash
go version
```

## Step 2: Install the Primitive Tool

Open Git Bash or Windows Terminal and run:

```bash
go install github.com/fogleman/primitive@latest
```

This will install `primitive.exe` to `C:\Users\<YourUsername>\go\bin\`

Verify installation:
```bash
where primitive.exe
```

You should see output like:
```
C:\Users\User\go\bin\primitive.exe
```

## Step 3: Add Go Bin to PATH (if not automatic)

If `where primitive.exe` doesn't work, add Go bin to PATH:

1. Open **Environment Variables**:
   - Right-click **This PC** or **My Computer**
   - Select **Properties**
   - Click **Advanced system settings**
   - Click **Environment Variables**

2. Under **User variables** or **System variables**, click **New**

3. Create a new variable:
   - **Variable name**: `GOPATH`
   - **Variable value**: `C:\Users\<YourUsername>\go`

4. Edit the **PATH** variable:
   - Select **PATH** and click **Edit**
   - Click **New**
   - Add: `C:\Users\<YourUsername>\go\bin`
   - Click **OK** and close all dialogs

5. Restart your terminal/IDE for changes to take effect

## Step 4: Install Python Dependencies

1. Extract the `geometrize-api-TESTED.zip` file to a folder (e.g., `C:\geometrize-api`)

2. Open Git Bash or Windows Terminal in that folder

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   # In Git Bash
   source venv/Scripts/activate
   
   # Or in Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Or in PowerShell
   venv\Scripts\Activate.ps1
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Test the Installation

### Test 1: Check Primitive Binary
```bash
where primitive.exe
primitive -h
```

### Test 2: Check Python Dependencies
```bash
python -c "import fastapi; import uvicorn; import PIL; print('All dependencies OK')"
```

### Test 3: Run the API
```bash
python run.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test 4: Test the API (in another terminal)
```bash
# First, activate the virtual environment in a new terminal
source venv/Scripts/activate

# Then test the health endpoint
curl http://localhost:8000/health
```

You should see:
```json
{"status":"healthy","primitive_binary":"C:\\Users\\User\\go\\bin\\primitive.exe"}
```

## Step 6: Test with an Image

1. Place a test image (e.g., `photo.jpg`) in your project folder

2. Run the comprehensive test:
   ```bash
   python comprehensive_test.py
   ```

3. Or test manually with curl:
   ```bash
   curl -X POST http://localhost:8000/api/generate \
     -F "image=@photo.jpg" \
     -F "output_format=json" \
     -F "shape_types=circle" \
     -F "shape_count=100"
   ```

## Troubleshooting

### "primitive binary not found"

**Solution 1**: Check if primitive is in PATH
```bash
where primitive.exe
```

If not found, ensure Go bin is in PATH:
```bash
echo %GOPATH%\bin
```

**Solution 2**: Reinstall primitive
```bash
go install github.com/fogleman/primitive@latest
```

**Solution 3**: Manually set the path in the code
Edit `geometrize_api.py` and add your path to the `windows_paths` list:
```python
windows_paths = [
    os.path.expanduser("~/go/bin/primitive.exe"),
    "C:\\Users\\YourUsername\\go\\bin\\primitive.exe",  # Add your path here
    # ... other paths
]
```

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
source venv/Scripts/activate
pip install -r requirements.txt
```

### "Address already in use" error

**Solution**: The port 8000 is already in use. Try a different port:
```bash
python run.py --port 9000
```

Or kill the process using port 8000:
```bash
# In PowerShell (as Administrator)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Or in Git Bash
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### "Connection refused" when testing

**Solution**: Ensure the API server is running in another terminal:
```bash
# Terminal 1: Start the API
python run.py

# Terminal 2: Run tests
python comprehensive_test.py
```

### Primitive execution fails

**Solution 1**: Check the debug output
The API will print debug information. Look for error messages about the primitive command.

**Solution 2**: Test primitive directly
```bash
primitive -h
primitive -i test.jpg -o output.svg -n 100
```

**Solution 3**: Check file permissions
Ensure the input image is readable and the output directory is writable.

## Using with VS Code

1. Open the project folder in VS Code

2. Install the Python extension

3. Select the Python interpreter:
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the one from `venv/Scripts/python.exe`

4. Open a terminal in VS Code (`Ctrl+` `)

5. The virtual environment should activate automatically

6. Run the API:
   ```bash
   python run.py
   ```

## Using with PowerShell

If you encounter execution policy errors:

```bash
# Check current policy
Get-ExecutionPolicy

# Set to allow scripts (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the virtual environment:
```bash
venv\Scripts\Activate.ps1
```

## Next Steps

1. Read the [README.md](README.md) for API documentation
2. Check [INSTALLATION.md](INSTALLATION.md) for general setup
3. Review [TEST_REPORT.md](TEST_REPORT.md) for test results
4. Start using the API in your applications!

## Support

If you encounter issues:

1. Check the debug output (the API prints helpful error messages)
2. Verify primitive is installed: `where primitive.exe`
3. Verify Python dependencies: `pip list`
4. Check the troubleshooting section above
5. Review the error messages carefully - they often indicate the solution

## Environment Variables (Optional)

You can set environment variables to customize behavior:

```bash
# Set custom primitive path (if auto-detection fails)
set PRIMITIVE_PATH=C:\Users\User\go\bin\primitive.exe

# Set custom port
set API_PORT=9000

# Set custom host
set API_HOST=0.0.0.0
```

Then run:
```bash
python run.py --host %API_HOST% --port %API_PORT%
```

---

**Last Updated**: November 27, 2025  
**Windows Support**: Fully tested and verified
