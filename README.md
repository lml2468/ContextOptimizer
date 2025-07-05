# ContextOptimizer

Intelligent context engineering assistant for Multi-Agent Systems (MAS).

## Overview

ContextOptimizer is designed to optimize System Prompts and tool return information in Multi-Agent Systems to ensure clear and coherent context flow. It provides intelligent diagnosis and coordinated optimization to improve the performance of multi-agent workflows.

## Key Features

1. **Context Logic Diagnosis** - Identify context breakage issues in multi-agent conversations
2. **Coordinated Optimization** - Optimize prompts and tool information together for better coherence
3. **Actionable Solutions** - Generate ready-to-use optimized configurations
4. **Best Practices Accumulation** - Learn and apply proven optimization patterns

## Architecture

- **Backend**: Python + FastAPI with async processing
- **Frontend**: React + Next.js + Tailwind CSS
- **Storage**: Local file system with JSON persistence
- **LLM Integration**: OpenAI API
- **Deployment**: Single Docker container

## Input Data

- `agents_config.json` - Agent configurations with system prompts and tools
- `messages_dataset.json` - Complete multi-agent conversation flows

## Output Data

- `evaluation_report.json` - 5-dimension quantified scores and issue analysis
- `optimization_result.json` - Optimized agent configs and tool format standards

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenAI API key

### Installation

#### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/contextoptimizer.git
cd contextoptimizer
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. Build and run with Docker Compose:
```bash
docker-compose up -d
```

The application will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

#### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/contextoptimizer.git
cd contextoptimizer
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

3. Set up frontend:
```bash
cd frontend
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

5. Run the backend:
```bash
cd backend
python start_backend.py
```

6. Run the frontend (in a separate terminal):
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

### API Documentation

Once the backend is running, visit:
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Usage Guide

1. **Prepare Your Data**:
   - Export your agent configurations to a JSON file
   - Export your conversation history to a JSON file
   - See `backend/test_data/` for example files

2. **Upload Your Data**:
   - Go to the upload page
   - Drag and drop your JSON files
   - Click "Start Analysis"

3. **Review Analysis**:
   - View overall score and dimension scores
   - Examine priority issues
   - Read recommendations

4. **Apply Optimization**:
   - Generate optimization results
   - Copy optimized system prompts
   - Implement tool format recommendations
   - Download complete optimization report

## Development

### Project Structure

```
contextoptimizer/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   ├── data/              # Data storage
│   ├── logs/              # Log files
│   └── test_data/         # Example files
├── frontend/              # Next.js frontend
│   ├── src/               # Source code
│   └── public/            # Static assets
├── docker-compose.yml     # Docker configuration
└── Dockerfile             # Container definition
```

### Running Tests

```bash
cd backend
pytest
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.
