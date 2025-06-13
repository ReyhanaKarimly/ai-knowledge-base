import fitz, re, string

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"[PDF EXTRACT ERROR] {e}")
            return ""
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print(f"[TXT READ ERROR] {e}")
            return ""
    return clean_text(text)


def chunk_text(text, max_len=300):
    words = text.split()
    return [" ".join(words[i:i+max_len]) for i in range(0, len(words), max_len)]