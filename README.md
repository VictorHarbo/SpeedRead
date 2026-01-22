<h1 align="center">
  <img src="src/assets/speedreadLogo.png" alt="Logo" width="40" />
  SpeedRead
</h1>

A modern Python GUI application for speed reading practice and improvement.

## Features

- Modern, clean user interface built with CustomTkinter
- Cross-platform compatibility (Windows, macOS, Linux)
- Standalone application ready for distribution

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository
2. Set up Python environment with pyenv:
   ```bash
   pyenv install 3.11.0  # or your preferred Python 3.8+ version
   pyenv local 3.11.0
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python src/main.py
```

## Building a Standalone Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SpeedRead src/main.py
```

The executable will be created in the `dist/` directory.

## Project Structure

```
SpeedRead/
├── src/
│   ├── main.py          # Application entry point
│   └── app/             # Application modules
│       ├── __init__.py
│       ├── gui.py       # GUI components
│       └── text_extractor.py  # Text extraction
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_gui.py
│   └── test_text_extractor.py
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
├── pyproject.toml      # Project configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Testing

Comprehensive unit tests are provided for all modules.

### Running Tests

Using pytest (recommended):
```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_text_extractor.py
```

Using unittest:
```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_text_extractor -v
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Development

This project uses:
- **CustomTkinter** - Modern, customizable tkinter widgets
- **Python 3.8+** - Core programming language

## Troubleshooting

### tkinter not available on macOS with pyenv

If you get a `ModuleNotFoundError: No module named '_tkinter'` error, your Python was installed without tkinter support. To fix this:

1. Install tcl-tk via Homebrew:
   ```bash
   brew install tcl-tk
   ```

2. Reinstall Python with tkinter support:
   ```bash
   env PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
     LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
     CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
     PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
     CFLAGS="-I$(brew --prefix tcl-tk)/include" \
     PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
     pyenv install 3.13.7
   ```

3. Set it as your local version:
   ```bash
   pyenv local 3.13.7
   ```

4. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```
