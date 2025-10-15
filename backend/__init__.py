"""
SilentSignal Backend Package
Core AI engine for emotional abuse detection
"""

__version__ = "1.0.0"
__author__ = "SilentSignal Team"

# Ensure local .env values are loaded into the process environment when the
# backend package is imported. This makes values from a project-level `.env`
# available to modules that call `os.getenv(...)` without requiring every
# entrypoint to call `load_dotenv()` individually.
try:
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	# If python-dotenv is not available, silently continue — callers will
	# still pick up environment variables from the real environment.
	pass


