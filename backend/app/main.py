import os
import threading
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import asyncio

from telegram_bot import main as run_bot
from utils import add_emoji_to_video

app = FastAPI()


@app.on_event("startup")
def startup_event():
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
    else:
        print("TELEGRAM_BOT_TOKEN not set, bot disabled")


@app.post("/api/add-emoji")
async def add_emoji(file: UploadFile = File(...)):
    if file.content_type not in ["video/mp4", "video/quicktime"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an MP4 video.")

    input_filename = f"/tmp/{uuid.uuid4()}.mp4"
    output_filename = f"/tmp/{uuid.uuid4()}.mp4"

    try:
        with open(input_filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        success = add_emoji_to_video(input_filename, output_filename)
        if not success:
            raise HTTPException(status_code=500, detail="Video processing failed.")

        if not os.path.exists(output_filename):
            raise HTTPException(status_code=500, detail="Processed video file was not created.")

        if os.path.exists(input_filename):
            os.remove(input_filename)

        response = FileResponse(
            path=output_filename,
            media_type='video/mp4',
            filename=f"emoji_{file.filename}"
        )

        asyncio.create_task(delayed_cleanup(output_filename))

        return response

    except Exception as e:
        cleanup_file(input_filename)
        cleanup_file(output_filename)
        raise HTTPException(status_code=500, detail=str(e))


async def delayed_cleanup(file_path: str):
    """Удаляет файл после задержки"""
    await asyncio.sleep(10)
    cleanup_file(file_path)


def cleanup_file(file_path: str):
    """Безопасно удаляет файл если он существует"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up: {file_path}")
    except Exception as e:
        print(f"Error cleaning up file {file_path}: {e}")
