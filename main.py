from fastapi import FastAPI, File, UploadFile
import whisper
import os

app = FastAPI()

# مدل whisper رو بارگذاری می‌کنیم
model = whisper.load_model("small")

@app.post("/process-audio/")
async def process_audio(task: str, file: UploadFile = File(...)):
    
    audio_path = f"temp_audio_{file.filename}"
    with open(audio_path, "wb") as audio_file:
        audio_file.write(await file.read())

    
    if task == "transcribe":
       
        result = model.transcribe(audio_path)
    elif task == "translate":
       
        result = model.transcribe(audio_path, task="translate")
    else:       
        return {"error": "Invalid task. Use 'transcribe' or 'translate'."}

    os.remove(audio_path)

    return {"result": result["text"]}
