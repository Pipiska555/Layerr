import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Папка для загруженных файлов (создастся сама)
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Главная страница (теперь берем index.html из корня)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Загрузка файла
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "filename": file.filename}

# Список файлов для сетки
@app.get("/api/files")
async def get_files():
    if not os.path.exists(UPLOAD_DIR): return []
    files = os.listdir(UPLOAD_DIR)
    return [{"name": f} for f in files]

# Раздача самих файлов (если захочешь их скачивать)
@app.get("/download/{name}")
async def download_file(name: str):
    return FileResponse(os.path.join(UPLOAD_DIR, name))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)