# SpeedRead Tests

This directory contains comprehensive unit tests for the SpeedRead application.

## Test Structure

- `test_text_extractor.py` - Tests for the text extraction module
  - Tests for `clean_word_list()` function
  - Tests for PDF text extraction
  - Tests for TXT file reading
  - Tests for Word document handling
  - Tests for the main `extract_text()` function

- `test_gui.py` - Tests for the GUI module
  - Tests for SpeedReadApp initialization
  - Tests for file loading functionality
  - Tests for reading controls (start/stop)
  - Tests for word display functionality

- `test_main.py` - Tests for the main entry point
  - Tests for successful application startup
  - Tests for error handling
  - Tests for KeyboardInterrupt handling

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with coverage report
```bash
pytest --cov=src --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_text_extractor.py
```

### Run specific test class
```bash
pytest tests/test_text_extractor.py::TestCleanWordList
```

### Run specific test method
```bash
pytest tests/test_text_extractor.py::TestCleanWordList::test_basic_word_list
```

### Run with verbose output
```bash
pytest -v
```

### Generate HTML coverage report
```bash
pytest --cov=src --cov-report=html
```
The HTML report will be generated in `htmlcov/index.html`

## Test Coverage

The test suite aims for comprehensive coverage of:
- Core functionality
- Edge cases
- Error handling
- File I/O operations
- GUI interactions
- User input validation

## Dependencies

Testing dependencies are listed in `requirements.txt`:
- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `pytest-mock` - Mocking utilities

## Writing New Tests

When adding new functionality to the application:
1. Create corresponding test cases in the appropriate test file
2. Follow the existing naming conventions (`test_*`)
3. Use descriptive test names that explain what is being tested
4. Include docstrings explaining the test purpose
5. Test both success and failure cases
6. Mock external dependencies (file system, GUI components)

## Continuous Integration

These tests can be integrated into CI/CD pipelines to ensure code quality:
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=src --cov-report=xml

# Check coverage threshold
pytest --cov=src --cov-fail-under=80
```
