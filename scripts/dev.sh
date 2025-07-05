#!/bin/bash

# ContextOptimizer Development Script
# This script helps with common development tasks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python3; then
    echo "Python3 is not installed. Please install Python 3.12 or later."
    exit 1
fi

if ! command_exists node; then
    echo "Node.js is not installed. Please install Node.js 18 or later."
    exit 1
fi

if ! command_exists npm; then
    echo "npm is not installed. Please install Node.js which includes npm."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$python_version < 3.10" | bc) -eq 1 ]]; then
    echo "Python 3.10 or later is required. You have Python $python_version."
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the ContextOptimizer root directory"
    exit 1
fi

# Function to setup backend
setup_backend() {
    print_status "Setting up backend environment..."
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install it first:"
        echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    # Create virtual environment and install dependencies
    cd backend
    print_status "Creating virtual environment with uv..."
    uv venv
    
    print_status "Installing backend dependencies..."
    uv pip install -e .
    
    cd ..
    print_success "Backend setup complete!"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend environment..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    else
        print_status "Frontend dependencies already installed"
    fi
    
    cd ..
    print_success "Frontend setup complete!"
}

# Function to run backend
run_backend() {
    print_status "Starting backend server..."
    
    cd backend

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env file with your API keys before running the backend"
    fi

    # Activate virtual environment and run server
    source .venv/bin/activate
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to run frontend
run_frontend() {
    print_status "Starting frontend development server..."
    
    cd frontend
    npm run dev
}

# Function to run both backend and frontend
run_dev() {
    print_status "Starting both backend and frontend servers..."
    
    # Start backend in background
    print_status "Starting backend server in background..."
    cd backend

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env file with your API keys"
    fi

    source .venv/bin/activate
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    print_status "Starting frontend development server..."
    cd frontend
    # Use port 3000 as requested
    PORT=3000 npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Both servers started!"
    print_status "Backend: http://localhost:8000"
    print_status "Frontend: http://localhost:3000"
    print_status "Press Ctrl+C to stop both servers"
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    wait
}

# Function to build for production
build_prod() {
    print_status "Building for production..."
    
    # Build frontend
    print_status "Building frontend..."
    cd frontend
    npm run build
    cd ..
    
    print_success "Production build complete!"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    print_status "Running backend tests..."
    cd backend
    source .venv/bin/activate
    python -m pytest tests/ -v
    cd ..
    
    print_success "Tests complete!"
}

# Function to clean up
clean() {
    print_status "Cleaning up development files..."
    
    # Clean backend
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean frontend
    cd frontend
    rm -rf .next node_modules 2>/dev/null || true
    cd ..
    
    # Clean data directories
    rm -rf data logs temp 2>/dev/null || true
    
    print_success "Cleanup complete!"
}

# Function to show help
show_help() {
    echo "ContextOptimizer Development Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup-backend    Setup backend environment with uv"
    echo "  setup-frontend   Setup frontend environment with npm"
    echo "  setup            Setup both backend and frontend"
    echo "  backend          Run backend server only"
    echo "  frontend         Run frontend server only"
    echo "  dev              Run both backend and frontend servers"
    echo "  build            Build for production"
    echo "  test             Run tests"
    echo "  clean            Clean up development files"
    echo "  help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup        # Setup both environments"
    echo "  $0 dev          # Start development servers"
    echo "  $0 backend      # Start only backend"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "setup-backend")
        setup_backend
        ;;
    "setup-frontend")
        setup_frontend
        ;;
    "setup")
        setup_backend
        setup_frontend
        ;;
    "backend")
        run_backend
        ;;
    "frontend")
        run_frontend
        ;;
    "dev")
        run_dev
        ;;
    "build")
        build_prod
        ;;
    "test")
        run_tests
        ;;
    "clean")
        clean
        ;;
    "help"|*)
        show_help
        ;;
esac
