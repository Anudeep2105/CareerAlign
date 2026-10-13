# Resume Parser AI - Technical Documentation

## 1. Overview
Resume Parser AI is a professional-grade software solution designed to convert unstructured resumes (PDF, Word, Images) into structured, searchable database entries. It leverages OCR for image processing and LLMs for high-accuracy contextual data extraction.

## 2. Core Features
- **Multi-Format Extraction**: Supports `.pdf`, `.docx`, `.txt`, `.jpg`, `.png`.
- **AI-Driven Parsing**: Uses GPT-4o to identify job titles, companies, dates, and skills, understanding synonyms and career trajectories.
- **Bias Reduction**: Configurable PII (Personally Identifiable Information) filtering to redact fields like age, gender, or photos.
- **Asynchronous Pipeline**: Uses background tasks to ensure the API remains responsive during heavy document processing.
- **Structured Storage**: Stores candidates in a relational database with JSON support for flexible profile schemas.

## 3. Technical Architecture

### System Flow
`Client Request` $\rightarrow$ `FastAPI Endpoint` $\rightarrow$ `Parser Factory` $\rightarrow$ `OCR/Text Extraction` $\rightarrow$ `AI NLP Engine` $\rightarrow$ `PII Filter` $\rightarrow$ `PostgreSQL/SQLite`

### Module Breakdown
- **`src/parsers/`**: Implements the Strategy Pattern. `BaseParser` defines the interface, while `PDFParser`, `DocxParser`, and `ImageParser` handle specific formats.
- **`src/nlp/`**: 
    - `ai_engine.py`: Handles prompt engineering and structured JSON output from the LLM.
    - `pii_filter.py`: Sanitizes extracted data based on HR policy.
- **`src/database/`**: Uses SQLAlchemy for ORM. The `Candidate` model stores both the raw text (for auditing) and the structured JSON (for searching).
- **`src/main.py`**: Orchestrates the pipeline and provides the REST API.

## 4. Installation & Setup

### Prerequisites
- Python 3.9+
- Tesseract OCR installed on the system (`sudo apt install tesseract-ocr` or Windows installer).
- OpenAI API Key.

### Setup Steps
1. **Clone and Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pdfplumber python-docx pytesseract openai sqlalchemy
   ```
2. **Environment Variables**:
   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```
3. **Run the Server**:
   ```bash
   uvicorn src.main:app --reload
   ```

## 5. API Reference

### Upload Resume
`POST /upload`
- **Payload**: `multipart/form-data` (file)
- **Response**: `200 OK` - Returns a status indicating processing has started in the background.

## 6. Future Roadmap
- **Bulk Import**: Integration with IMAP for email inbox monitoring.
- **Vector Search**: Implementation of `pgvector` for semantic candidate matching (e.g., searching for "Frontend Expert" and finding "React Developer").
- **Multilingual Support**: Expanding the AI prompt to handle non-English resumes with automatic translation.
