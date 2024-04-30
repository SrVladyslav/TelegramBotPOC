from data.database_handler import DatabaseHandler
from utils.utils import AudioUtils
from dotenv import load_dotenv
import os 

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# .env
load_dotenv()
TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')
AUDIO_DATA_PATH = './data/audio_data/'


# =========================================================================================== BOT FUNCTION HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def bd1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    db = DatabaseHandler()                        
    await update.message.reply_text(db.getUserAudioCount(update.effective_user.id) )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    print("GIVEN USER: ", user)
    await update.message.reply_text(update.message.text)

async def audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive an audio message, that should be processed."""
    # Edge case of the message been edited
    if not update.message:
        return 
    
    # Obtain the user ID to know where to store its audio
    user_id = update.effective_user.id
    # Audio preprocessing and conversion
    file_id = update.message.voice.file_id
    audio_msg_file = await context.bot.get_file(file_id)

    # NOTE: Here I ASSUME that the audio will be short enough to be stored as bytearray in RAM, 
    # allowing us to directly preprocess the audio without additional I/O latency
    # of saving the file, reading it, and saving it again after preprocessing.
    audio_data = await audio_msg_file.download_as_bytearray()
    au = AudioUtils()
    await au.processAudio(audio_data, user_id)

    await update.message.reply_text("Let's check this audio!")


# =========================================================================================== MAIN APP
def main():
    # --------------------------------------------------------------------------------------- Database initialization
    db = DatabaseHandler()                                                                  # Database functions
    db.create_tables()                                                                      # Created tables: Users, Audios, Images               

    # ====================================================================================== Start the SrVladyslav Bot
    print("Starting the SrVladyslav Bot")
    telegram_bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # --------------------------------------------------------------------------------------- Adding the bot handlers
    telegram_bot.add_handler(CommandHandler("start", start))                                # /start handler
    telegram_bot.add_handler(CommandHandler("bd1", bd1))                                # /start handler
    
    
    telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))         # echo message
    telegram_bot.add_handler(MessageHandler(filters.VOICE, audio_message))                  # Audio filtering
    # --------------------------------------------------------------------------------------- Run the bot until Ctrl-C is pressed
    print("The bot is running... Press Ctrl-C to stop.")
    telegram_bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()