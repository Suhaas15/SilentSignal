# SilentSignal Makefile
# Quick commands for development and deployment

.PHONY: setup run-ui run-api test clean install

# Setup environment
setup:
	@echo "Setting up SilentSignal environment..."
	pip install -r requirements.txt
	cp env_example.txt .env
	@echo "✅ Setup complete! Edit .env file with your configuration."

# Install dependencies
install:
	pip install -r requirements.txt

# Run Streamlit UI
run-ui:
	@echo "Starting SilentSignal UI..."
	streamlit run app.py --server.port 8501 --server.address localhost

# Run WhatsApp API
run-api:
	@echo "Starting WhatsApp API..."
	uvicorn integrations.whatsapp_fastapi:app --reload --host 0.0.0.0 --port $${PORT:-8000}

# Run both services
run-all: run-ui run-api

# Run tests
test:
	@echo "Running SilentSignal tests..."
	python -m pytest tests/ -v

# Test pattern detection
test-patterns:
	python -c "from backend.pattern_detector import PatternDetector; pd = PatternDetector(); print('Pattern detector loaded successfully')"

# Test MCP orchestrator
test-orchestrator:
	python -c "from backend.mcp_orchestrator import MCPOrchestrator; oc = MCPOrchestrator(); print('MCP orchestrator loaded successfully')"

# Test NIM client
test-nim:
	python -c "from backend.nimo_client import NimoClient; nc = NimoClient(); print('NIM client loaded successfully')"

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete

# Format code
format:
	black .
	isort .

# Lint code
lint:
	flake8 .
	mypy .

# Build for production
build:
	@echo "Building SilentSignal for production..."
	python -c "import backend, integrations; print('✅ All modules import successfully')"

# Health check
health:
	@echo "Checking SilentSignal health..."
	curl -s http://localhost:8501 > /dev/null && echo "✅ UI is running" || echo "❌ UI not running"
	curl -s http://localhost:$${PORT:-8000}/health > /dev/null && echo "✅ API is running" || echo "❌ API not running"

# Demo mode
demo:
	@echo "Starting SilentSignal demo..."
	@echo "UI: http://localhost:8501"
	@echo "API: http://localhost:8000"
	@echo "Health: http://localhost:8000/health"
	make run-all

# Help
help:
	@echo "SilentSignal Makefile Commands:"
	@echo "  setup     - Setup environment and install dependencies"
	@echo "  run-ui    - Start Streamlit UI on port 8501"
	@echo "  run-api   - Start WhatsApp API on port 8000"
	@echo "  run-all   - Start both UI and API"
	@echo "  test      - Run test suite"
	@echo "  test-*    - Test individual components"
	@echo "  clean     - Clean up temporary files"
	@echo "  format    - Format code with black and isort"
	@echo "  lint      - Lint code with flake8 and mypy"
	@echo "  build     - Build for production"
	@echo "  health    - Check service health"
	@echo "  demo      - Start demo mode"
	@echo "  help      - Show this help message"


