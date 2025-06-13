from fastapi import APIRouter, UploadFile, File, HTTPException
import os, shutil, uuid
from app.services.file_processor import extract_text, chunk_text
from app.db.database import get_db_connection
from fastapi import BackgroundTasks

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Only PDF or TXT files allowed.")

    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(save_path)
    chunks = chunk_text(text)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (id, filename) VALUES (?, ?)", (file_id, file.filename))
    for idx, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO chunks (id, file_id, chunk_index, chunk_text) VALUES (?, ?, ?, ?)",
            (chunk_id, file_id, idx, chunk)
        )
    conn.commit()
    return {"file_id": file_id, "filename": file.filename}

@router.get("/")
def list_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM files")
    rows = cursor.fetchall()
    return [{"id": row[0], "filename": row[1]} for row in rows]

@router.delete("/{file_id}/")
def delete_file(file_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks WHERE file_id = ?", (file_id,))
    cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
    conn.commit()
    return {"deleted": file_id}
