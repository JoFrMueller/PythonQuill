# PythonQuill

Contains some reference implementation details to run QuillJS around Python and Socket.IO

## Development & evaluation

Activate virtual environment for Python and install dependencies.

```powershell
# For example when you run within PowerShell.
.\.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

1. Run server.py
2. Navigate to http://127.0.0.1:5000/editor/fall_123 or/and http://127.0.0.1:5000/editor/fall_456
3. Run send_data.py

## Change QuillJS code to react on messages

Edit `templates/editor.html` to adjust HTML, QuillJS editor behaviour or `static/css/custom.css` to change style via CSS.