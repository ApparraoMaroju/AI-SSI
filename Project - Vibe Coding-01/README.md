# Test Case Generator

A full-stack web application that connects to Jira, fetches ticket user stories, and auto-generates structured test cases using Claude AI.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Frontend                                    │
│                     React + Vite + Tailwind CSS                         │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │ Connection  │  │   Input     │  │  Context    │  │    Output       │ │
│  │   Panel     │  │   Panel     │  │   Card      │  │    Panel        │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTP/REST
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              Backend                                     │
│                        Python + FastAPI                                  │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                         API Routes                                   ││
│  │  /api/jira/test-connection  │  /api/jira/fetch-issue               ││
│  │  /api/testcases/generate    │  /api/testcases/export               ││
│  │  /api/templates/*           │  /api/health                          ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│  │  Jira Service   │  │   LLM Service   │  │    Export Service       │  │
│  │  (REST API v3)  │  │  (Claude API)   │  │    (MD/CSV/TSV)         │  │
│  └────────┬────────┘  └────────┬────────┘  └─────────────────────────┘  │
└───────────┼────────────────────┼────────────────────────────────────────┘
            │                    │
            ▼                    ▼
    ┌───────────────┐    ┌───────────────┐
    │     Jira      │    │   Anthropic   │
    │   Cloud API   │    │   Claude AI   │
    └───────────────┘    └───────────────┘
```

## Features

- **Jira Integration**: Connect to any Jira Cloud instance and fetch tickets
- **AI-Powered Generation**: Uses Claude Sonnet to generate comprehensive test cases
- **Multiple Templates**: Functional, Regression, Smoke, Edge, and Security test templates
- **Editable Output**: Review and modify generated test cases in-browser
- **Export Options**: Copy to clipboard (TSV), export as Markdown or CSV
- **No Data Persistence**: API tokens held in session only, never stored server-side

## Prerequisites

- Python 3.11+
- Node.js 18+
- Jira Cloud account with API token
- Anthropic API key for Claude

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your Anthropic API key (optional - can be provided via UI)
# ANTHROPIC_API_KEY=sk-ant-...

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Open http://localhost:5173 in your browser.

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude API key (optional - can use UI) | - |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `false` |
| `LLM_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `LLM_MAX_TOKENS` | Max tokens for generation | `4096` |
| `LLM_TEMPERATURE` | LLM temperature | `0.3` |
| `LOG_LEVEL` | Logging level | `INFO` |

## API Reference

### POST `/api/jira/test-connection`
Test Jira connection with provided credentials.

**Request:**
```json
{
  "credentials": {
    "base_url": "https://company.atlassian.net",
    "email": "user@company.com",
    "api_token": "your-api-token"
  }
}
```

### POST `/api/jira/fetch-issue`
Fetch and parse a Jira issue by ID.

**Request:**
```json
{
  "credentials": { ... },
  "issue_id": "PROJ-123"
}
```

### POST `/api/testcases/generate`
Generate test cases using Claude.

**Request:**
```json
{
  "issue": { ... },
  "template_type": "Functional",
  "min_test_cases": 5,
  "anthropic_api_key": "sk-ant-..."
}
```

### POST `/api/testcases/export`
Export test cases to various formats.

**Request:**
```json
{
  "test_cases": [ ... ],
  "format": "markdown",
  "include_header": true
}
```

## Test Case Schema

```json
{
  "id": "TC_001",
  "title": "Verify successful login with valid credentials",
  "type": "Positive",
  "priority": "P0",
  "preconditions": "User has a valid account",
  "steps": [
    "Navigate to login page",
    "Enter valid username",
    "Enter valid password",
    "Click Login button"
  ],
  "test_data": "Username: testuser, Password: Test@123",
  "expected_result": "User is redirected to dashboard",
  "linked_jira_id": "PROJ-123"
}
```

## Template Types

| Type | Focus |
|------|-------|
| **Functional** | Comprehensive functional coverage, happy path, validation |
| **Regression** | Existing features, integration points, backward compatibility |
| **Smoke** | Critical path only, quick sanity checks |
| **Edge** | Boundary values, null/empty inputs, limits |
| **Security** | Authentication, authorization, injection, XSS |

## Docker Deployment

### Backend

```bash
cd backend
docker build -t test-case-generator-backend .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=sk-ant-... test-case-generator-backend
```

### Frontend

```bash
cd frontend
npm run build
# Serve the dist/ folder with any static file server
```

## Project Structure

```
Project - Vibe Coding-01/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry
│   │   ├── config.py         # Settings
│   │   ├── schemas.py        # Pydantic models
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── jira.py
│   │   │   ├── testcases.py
│   │   │   └── templates.py
│   │   └── services/
│   │       ├── jira_service.py
│   │       ├── llm_service.py
│   │       └── export_service.py
│   ├── templates/            # YAML test templates
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── types.ts
│   │   ├── index.css
│   │   └── components/
│   │       ├── ConnectionPanel.tsx
│   │       ├── InputPanel.tsx
│   │       ├── ContextCard.tsx
│   │       └── OutputPanel.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

## Getting Jira API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Test Case Generator")
4. Copy the token - you won't be able to see it again!

## Getting Anthropic API Key

1. Sign up at [Anthropic Console](https://console.anthropic.com)
2. Navigate to API Keys
3. Create a new key
4. Copy and store securely

## Troubleshooting

### "Connection failed" for Jira
- Verify your Jira base URL ends without a trailing slash
- Ensure you're using an API token, not your password
- Check that your email matches your Atlassian account

### "Invalid Anthropic API key"
- Ensure the key starts with `sk-ant-`
- Check for any extra whitespace
- Verify the key is active in Anthropic Console

### Test cases not generating
- Ensure the issue has a description or acceptance criteria
- Try a different template type
- Check the backend logs for detailed errors

## License

MIT
