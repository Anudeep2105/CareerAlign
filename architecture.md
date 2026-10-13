# Resume Parser Architecture

## Tech Stack
- **Backend**: Python (FastAPI) - High performance, asynchronous, and excellent AI/NLP ecosystem.
- **OCR/File Parsing**: 
  - `PyMuPDF` / `pdfplumber` (Digital PDFs)
  - `python-docx` (Word documents)
  - `Tesseract OCR` / `EasyOCR` (Scanned images/PDFs)
- **AI/NLP Engine**: 
  - `spaCy` (Named Entity Recognition & Rule-based matching)
  - `OpenAI GPT-4o` or `Llama 3` (Contextual extraction, synonym mapping, and structured JSON output)
- **Database**: 
  - `PostgreSQL` (Structured candidate profiles)
  - `Elasticsearch` / `pgvector` (Searchable skills and semantic matching)
- **Task Queue**: `Celery` + `Redis` (For bulk import and asynchronous processing)

## Module Design
1. **Ingestion Layer**: API endpoints and Bulk Importers (Email/FTP/API).
2. **Normalization Layer**: Converts all inputs (.pdf, .docx, .png, .jpg) into raw text using OCR or direct extraction.
3. **Extraction Layer (AI Pipeline)**:
   - NER (Named Entity Recognition) for basic entities.
   - LLM-based parsing for complex sections (Work History, Education).
   - PII Filtering for bias reduction.
4. **Persistence Layer**: Structured data storage in PostgreSQL.
5. **Integration Layer**: REST API for ATS/CRM sync.

## Data Flow
`File` -> `OCR/Extractor` -> `Raw Text` -> `AI Parsing` -> `PII Filter` -> `Database` -> `ATS API`
