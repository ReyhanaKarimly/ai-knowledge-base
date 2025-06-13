from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import files, ask
from app.db.database import init_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(ask.router, prefix="/api", tags=["ask"])

# @app.get("/")
# def root():
#     return {"message": "Simple AI Knowledge Base API is running"}
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

