"""
SpeedRead - Main application entry point
A modern speed reading application with a GUI built using CustomTkinter.
"""

import sys
from app import SpeedReadApp


def main():
    """Main application entry point."""
    try:
        app = SpeedReadApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
