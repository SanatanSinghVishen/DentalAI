# QuensultingAI Dental Clinic Voice Agent Backend

This is the FastAPI backend for the Retell AI voice agent. It handles custom functions called by the agent during conversation flow.

## Setup Instructions

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in the values based on the setup guide.
4. Run the server locally: `uvicorn app.main:app --reload`

## Deploying to Render

This repository includes a `render.yaml` file. You can deploy it to Render by connecting your GitHub repository and creating a new Web Service. Make sure to supply the required environment variables in the Render dashboard.

## Tests
Run the test suite using pytest:
```bash
pytest
```
