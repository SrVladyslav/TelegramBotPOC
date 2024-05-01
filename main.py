from data.database_handler import DatabaseHandler
from utils.audio_utils import AudioUtils
from utils.image_utils import ImageUtils
from dotenv import load_dotenv
import os 

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# .env
load_dotenv()
TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')
IMAGE_DATA_PATH = './data/image_data/'

# =========================================================================================== BOT FUNCTION HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def audioDBCount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the DB Audio Count for your ID."""
    db = DatabaseHandler()          
    res = f'We have {db.getUserAudioCount(update.effective_user.id)} audios from you'              
    await update.message.reply_text(res)

async def audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive an audio message, changes the sampling rate to 16kHz and 
    saves it in .wav format.

    Args:
        update (Update): This object represents an incoming update.
        context (ContextTypes.DEFAULT_TYPE): Determines the type of the context argument.
    """
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
    await au.processAudio(audio_data=audio_data, user_id=user_id)
    await update.message.reply_text("Let's check this audio!")

async def image_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Determines whether there is a face in the photos being sent or not, 
    saves only those where it is.

    NOTE: According to the statement: "Determines whether there is a face in 
    the photos being sent or not, saves only those where it is" it's not clear 
    if we need to record the image relations with the User into a DB, neither
    if the images should have some user_id, or if we need to rescale those images. 
    
    Here I'm assuming that we are making a face Dataset, so all the images 
    are named as [image_<0>.jpg, ..., image_<N>.jpg] with its original sizes. 
    
    Also no information about the userid will be included (it would be the same 
    code like in the audio part, if needed).

    Args:
        update (Update): This object represents an incoming update.
        context (ContextTypes.DEFAULT_TYPE): Determines the type of the context argument.
    """
    # Edge case of the message been edited
    if not update.message:
        return 
    
    iu = ImageUtils()
    # for photo_obj in update.message.photo:
    photo_obj = update.message.photo[-1]
    new_file = await context.bot.get_file(photo_obj.file_id)

    # NOTE: Here I ASSUME that the photo will be small enough to be stored as bytearray in RAM, 
    # allowing us to directly if there is a face without additional I/O latency
    # of saving the file, reading it, and saving it again after preprocessing.
    image_data = await new_file.download_as_bytearray()
    has_face = await iu.processImage(img=image_data)

    # Telegram converts all the images to .jpg, which is good for making the Dataset
    # and we don't need to preprocess it further.
    if has_face:
        files_in_dir = iu.count_directory_files()
        new_img_id = f'{IMAGE_DATA_PATH}image_{files_in_dir}.jpg'

        # NOTE: Saving the original file from internet without rescaling could be
        # a problem if someone starts sending very big images. But with 
        # "saves only those where it is" I understand that is original Image. 
        # At least Telegram downsizes big images, it's a plus in this task.
        await new_file.download_to_drive(new_img_id)

    if has_face:
        await update.message.reply_text("What a beautiful face!")
    else:
        await update.message.reply_text("Wow, thanks!")

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
    # telegram_bot.add_handler(CommandHandler("adb", audioDBCount))                           # /adb   returns the Audio Db count for your ID, (HELPER)
    
    telegram_bot.add_handler(MessageHandler(filters.VOICE, audio_message))                  # Audio filtering
    telegram_bot.add_handler(MessageHandler(filters.PHOTO, image_message))                  # Image filtering
    # --------------------------------------------------------------------------------------- Run the bot until Ctrl-C is pressed
    print("The bot is running... Press Ctrl-C to stop.")
    telegram_bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()