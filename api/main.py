from fastapi import FastAPI, UploadFile, File
from app.inference import clone_voice

app = FastAPI()

@app.post("/clone")
async def clone(file: UploadFile = File(...), text: str = "Hello there!"):
    with open("input.wav", "wb") as f:
        f.write(await file.read())
    out_path = clone_voice("input.wav", text)
    return {"output": out_path}
