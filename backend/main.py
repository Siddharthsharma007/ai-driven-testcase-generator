from fastapi import FastAPI, File, UploadFile, Form, Body, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import shutil
import os
import uuid
from utils import file_utils, ocr_utils, ai_utils, export_utils, jira_utils, kb_utils
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Extract text
    ext = file.filename.split('.')[-1].lower()
    if ext == 'pdf':
        text = file_utils.extract_text_from_pdf(file_path)
    elif ext == 'docx':
        text = file_utils.extract_text_from_docx(file_path)
    elif ext in ['png', 'jpg', 'jpeg', 'bmp']:
        text = ocr_utils.extract_text_from_image(file_path)
    else:
        return JSONResponse({"error": "Unsupported file type."}, status_code=400)
    os.remove(file_path)
    return {"text": text}

@app.post("/generate")
def generate_cases(text: str = Form(...)):
    cases = ai_utils.generate_test_cases(text)
    return {"cases": cases}


@app.post("/generate_ui_suite")
def generate_ui_suite(
    file: UploadFile = File(...),
):
    """
    Generate a comprehensive UI-based test suite from an uploaded UI screenshot.
    The image is OCR'd to text and then passed to OpenAI to infer elements and test cases.
    """
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"ui_{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ext = file.filename.split(".")[-1].lower()
    if ext not in ["png", "jpg", "jpeg", "bmp"]:
        os.remove(file_path)
        return JSONResponse({"error": "Unsupported file type for UI suite. Please upload an image."}, status_code=400)

    try:
        ui_text = ocr_utils.extract_text_from_image(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    suite = ai_utils.generate_ui_test_suite(ui_text)
    return {"suite": suite}

@app.post("/export")
def export_cases(cases: List[dict], formats: List[str]):
    zip_path = export_utils.export_all_formats(cases, formats)
    return FileResponse(zip_path, filename="test_cases.zip")

@app.post("/jira")
def send_to_jira(cases: List[dict], jira_url: str, api_token: str, project_key: str):
    result = jira_utils.send_cases_to_jira(cases, jira_url, api_token, project_key)
    return result 

@app.post("/kb/upload")
def kb_upload(file: UploadFile = File(...), tag: str = Form(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"kb_{file_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    ext = file.filename.split('.')[-1].lower()
    if ext == 'pdf':
        text = file_utils.extract_text_from_pdf(file_path)
    elif ext == 'docx':
        text = file_utils.extract_text_from_docx(file_path)
    elif ext in ['png', 'jpg', 'jpeg', 'bmp']:
        text = ocr_utils.extract_text_from_image(file_path)
    else:
        os.remove(file_path)
        return JSONResponse({"error": "Unsupported file type."}, status_code=400)
    os.remove(file_path)
    kb_utils.add_kb_entry(tag, file.filename, text)
    return {"message": "KB document uploaded and indexed."}

@app.get("/kb/list")
def kb_list():
    return kb_utils.list_kb_entries()

@app.get("/kb/get_text")
def kb_get_text(tag: str):
    return {"text": kb_utils.get_text_by_tag(tag)} 

@app.post("/kb/ask")
def kb_ask(question: str = Body(...), tags: list = Body(default=[])):
    # Get relevant KB text (all or by tags)
    if tags:
        context = ""
        for tag in tags:
            context += kb_utils.get_text_by_tag(tag) + "\n\n"
    else:
        # All KB entries
        context = "\n\n".join([entry['text'] for entry in kb_utils.list_kb_entries()])
    # Compose prompt
    prompt = f"""You are a helpful assistant. Based on the following knowledge base, answer the user's question.\n\nKnowledge Base:\n{context}\n\nQuestion: {question}\n\nAnswer:"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2
    )
    answer = response.choices[0].message.content.strip()
    return {"answer": answer} 

@app.delete("/kb/delete")
def kb_delete(tag: str = Query(...), filename: str = Query(...)):
    kb_utils.delete_kb_entry(tag, filename)
    return {"message": "KB entry deleted."} 