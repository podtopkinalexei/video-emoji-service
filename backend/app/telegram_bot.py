import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import tempfile

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = "http://localhost:8000/api/add-emoji"  # Измените на ваш бэкенд URL

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.video:
        await update.message.reply_text("Пожалуйста, отправьте видеофайл.")
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
            video_file = await update.message.video.get_file()
            await video_file.download_to_drive(temp_input.name)
            video_path = temp_input.name

        processing_message = await update.message.reply_text("Обрабатываю видео...")

        with open(video_path, 'rb') as video:
            files = {'file': (f"{update.message.video.file_id}.mp4", video, 'video/mp4')}
            response = requests.post(BACKEND_URL, files=files)

        try:
            os.unlink(video_path)
        except:
            pass

        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output:
                temp_output.write(response.content)
                output_path = temp_output.name

            try:
                await update.message.reply_video(
                    video=open(output_path, 'rb'),
                    caption="Ваше видео с эмодзи готово!"
                )
                await processing_message.delete()
            finally:
                try:
                    os.unlink(output_path)
                except:
                    pass

        else:
            error_text = response.json().get('detail', 'Произошла ошибка при обработке видео')
            await update.message.reply_text(f"Ошибка: {error_text}")
            await processing_message.delete()

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
        try:
            await processing_message.delete()
        except:
            pass

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Не найден TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    application.run_polling()

if __name__ == "__main__":
    main()