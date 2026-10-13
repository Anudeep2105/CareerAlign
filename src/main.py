from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Form
from .parser_manager import ParserFactory
from .nlp.ai_engine import AIParser
from .nlp.pii_filter import PIIFilter
from .database.models import init_db, Candidate
import shutil
import os
from docx import Document
import requests
from bs4 import BeautifulSoup

app = FastAPI()
db_session = init_db()
ai_parser = AIParser(api_key=os.getenv("OPENAI_API_KEY", "your-key-here"))
pii_filter = PIIFilter(disabled_fields=["gender", "age", "photo"])

def extract_jd_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "html.parser")
        # Try to find the main content (common JD tags)
        for tag in ["main", "article", "div[class*='job-description']", "div[id*='job-description']"]:
            content = soup.find(tag)
            if content:
                return content.get_text(separator=" ", strip=True)
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"Error extracting JD from {url}: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Resume Parser API is running. Go to /docs for the interactive UI."}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    background_tasks.add_task(process_resume, temp_path)
    return {"status": "Processing started", "filename": file.filename}

@app.post("/optimize")
async def optimize_resume(file: UploadFile = File(...), jd: str = Form(...), model: str = Form("llama-3.1-8b-instant")):
    # 1. Extract Text from Resume
    temp_path = f"temp_opt_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        parser = ParserFactory.get_parser(temp_path)
        resume_text = parser.extract_text(temp_path)
        
        # 2. Optimize using AI
        optimized_text = ai_parser.optimize_resume(resume_text, jd, model=model)
        
        # 3. Save to .docx
        doc = Document()
        doc.add_paragraph(optimized_text)
        output_filename = f"optimized_{file.filename.split('.')[0]}.docx"
        output_path = os.path.join("outputs", output_filename)
        
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
            
        doc.save(output_path)
        
        return {
            "status": "Success", 
            "optimized_text": optimized_text, 
            "download_url": output_filename
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/optimize-batch")
async def optimize_batch(file: UploadFile = File(...), links_file: UploadFile = File(...), model: str = Form("llama-3.1-8b-instant")):
    # 1. Read the links file
    links_content = (await links_file.read()).decode("utf-8")
    urls = [url.strip() for url in links_content.splitlines() if url.strip()]
    
    # 2. Save the resume temporarily
    temp_resume_path = f"temp_batch_{file.filename}"
    with open(temp_resume_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    results = []
    try:
        parser = ParserFactory.get_parser(temp_resume_path)
        resume_text = parser.extract_text(temp_resume_path)
        
        for i, url in enumerate(urls):
            jd_text = extract_jd_from_url(url)
            if "Error extracting JD" in jd_text:
                results.append({"url": url, "status": "Failed", "error": jd_text})
                continue
                
            optimized_text = ai_parser.optimize_resume(resume_text, jd_text, model=model)
            
            # Save individual file
            doc = Document()
            doc.add_paragraph(optimized_text)
            filename = f"optimized_{i+1}_{file.filename.split('.')[0]}.docx"
            output_path = os.path.join("outputs", filename)
            
            if not os.path.exists("outputs"):
                os.makedirs("outputs")
            doc.save(output_path)
            
            results.append({"url": url, "status": "Success", "text": optimized_text, "file": filename})
            
    finally:
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)
            
    return {"results": results}

def process_resume(file_path: str):
    try:
        # 1. Extract Text
        parser = ParserFactory.get_parser(file_path)
        raw_text = parser.extract_text(file_path)
        
        # 2. AI Parsing
        structured_data = ai_parser.parse_resume_text(raw_text)
        
        # 3. PII Filtering
        clean_data = pii_filter.filter_data(structured_data)
        
        # 4. Database Entry
        contact = clean_data.get("contact_details", {})
        candidate = Candidate(
            full_name=contact.get("name"),
            email=contact.get("email"),
            phone=contact.get("phone"),
            location=contact.get("location"),
            raw_text=raw_text,
            structured_data=clean_data
        )
        db_session.add(candidate)
        db_session.commit()
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

