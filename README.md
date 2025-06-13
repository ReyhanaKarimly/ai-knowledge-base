A simple AI-powered Knowledge Base that allows you to upload `.txt` or `.pdf` documents and ask questions about their content. This project implements a semantic search-based question answering approach leveraging sentence embeddings from a pre-trained transformer model.

### Model
 - It uses the SentenceTransformer model "multi-qa-MiniLM-L6-cos-v1" which is a lightweight, efficient transformer designed specifically for generating embeddings suited to question-answering and semantic similarity tasks.
 - This model converts text chunks and input questions into dense vector representations in a shared embedding space.

### Data Processing
- Document content is pre-processed and split into smaller text chunks stored in a database.
- Each chunk is encoded into a fixed-size embedding vector using the model.

## Features
- Upload documents (PDF or text)
- Extract and store content in a local SQLite database
- Chunk documents and compute vector representations
- Ask questions via API and receive the most relevant answer
- Modularized FastAPI backend

## Setup Instructions
```bash
git clone https://github.com/ReyhanaKarimly/ai-knowledge-base.git
cd ai-knowledge-base
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints
### Upload a file
`POST /api/files/`
- Form-data: `file=(your .pdf or .txt)`

### List uploaded files
`GET /api/files/`

### Delete a file
`DELETE /api/files/{file_id}/`

### Ask a question
`POST /api/ask/`
```json
{
  "question": "What is this document about?"
}
```

## Docker Support
```bash
docker build -t ai-knowledge-base .
docker run -p 8000:8000 ai-knowledge-base
```

## Project Structure
```
ai_knowledge_base/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── files.py
│   │   └── ask.py
│   ├── services/
│   │   ├── file_processor.py
│   │   └── qa_engine.py
│   └── db/
│       └── database.py
├── Dockerfile
├── requirements.txt
└── README.md
```
