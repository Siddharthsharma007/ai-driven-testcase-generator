# AI Test Case Generator

## Overview
A web-based tool to generate detailed test cases from BRD documents or images using AI. Supports PDF, DOCX, image uploads, and manual input. Outputs test cases in CSV, Excel, and Jira Xray JSON formats, with ZIP download and optional Jira integration.

## Features
- Upload BRD (PDF, DOCX) or image (screenshot)
- Extracts requirements text automatically
- Generates Positive, Negative, Boundary, and Edge test cases
- Test case fields: Test ID, Title, Preconditions, Steps, Expected Result, Priority, Type
- Output: CSV, Excel, JSON (Jira Xray)
- Download as ZIP
- (Optional) Send to Jira via REST API
- Modular, extensible codebase

## Tech Stack
- **Backend:** Python, FastAPI, OpenAI API, PyMuPDF, docx2txt, pytesseract
- **Frontend:** Streamlit
- **Containerization:** Docker

## Setup Instructions

### Backend
1. `cd backend`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

### Docker (Full Stack)
- See backend and frontend Dockerfiles for build/run instructions.

## Example Jira Integration
See `backend/utils/jira_utils.py` for a sample API call to Jira. 