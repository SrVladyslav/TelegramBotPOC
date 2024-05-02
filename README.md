# Telegram bot for storing audio and images 

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat-square&logo=telegram&logoColor=white) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat-square&logo=opencv&logoColor=white) 	![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=flat-square&logo=sqlite&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat-square&logo=numpy&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)

## Tasks to do:
Develop a Telegram Bot that can:
- Save audio messages to a DB by user IDs. Audio should be converted to `.wav` format with a **16kHz sampling rate**. <br> Recording format: `uid -> [audio_message_0, audio_message_1, ..., audio_message_N]`.

- Determines whether there **is a face in the photos** being sent or not, saves only those where it is.

## Steps to start the bot

### Clone this repo
Open your terminal and ho to the folder where you want to save this bot and type:
```
git clone https://github.com/SrVladyslav/TelegramBotPOC.git
```

### Install venv
```
cd TelegramBotPOC
python -m venv .venv
source .venv/Scripts/activate
```

### Install all the dependencies
```
pip install -r requirements.txt
```
> **_NOTE:_** It might take some time, be patient 😅.

### Obtain telegram token with BotFather
In order to use the bot live, you need a Telegranm token, which is used to create your own Bot in Telegram. <br>

Follow the steps to obtain yours from scratch:

1. Search for `BotFather` in the Telegram search section.
2. Click on the `Start` button.`
3. Type `/newbot` and press enter to create your own bot. Then you will be asked to provide the bot name and username. To choose a username, you sould know that it must end with the word `bot` or `_bot`.
> **_NOTE:_** It is not possible to change the bot username later!
4. If BotFather approves your username, you will be prompted with a message that contains `YOUR_TELEGRAM_BOT_TOKEN` in it, copy this token.


```
echo "TELEGRAM_BOT_TOKEN='<YOUR_TELEGRAM_BOT_TOKEN here>'" > .env
```

### Run bot
```
python main.py
```
Press Ctrl-C to stop.

### Considerations before production 🤗
- Implement a connection to a remote database (e.g. [RDS](https://aws.amazon.com/es/rds/) + [S3](https://aws.amazon.com/es/s3/)).
- Implement a [logger](https://www.geeksforgeeks.org/logging-in-python/) to keep track of everything that happens in the program.

## Implementations
### Audio implementation
- Here is a [notebook](https://github.com/SrVladyslav/TelegramBotPOC/blob/main/dbVisualizer.ipynb) with readings from the DB.
- [Database handler](https://github.com/SrVladyslav/TelegramBotPOC/blob/main/data/database_handler.py) code here.
- [Audio processing](https://github.com/SrVladyslav/TelegramBotPOC/blob/main/utils/audio_utils.py) main code.

### Image implementation
- [Image processing](https://github.com/SrVladyslav/TelegramBotPOC/blob/main/utils/image_utils.py) main code.

> **_NOTE:_** According to the statement: "Determines whether there is a face in 
    the photos being sent or not, saves only those where it is" it's not clear 
    if we need to record the image relations with the User into a DB, neither
    if the images should have some user_id, or if we need to rescale those images. <br><br>
    Here I'm assuming that we are making a face Dataset, so all the images 
    are named as [image_<0>.jpg, ..., image_<N>.jpg] with its original sizes, since Telegram rescales large images to a maximum of 1280px, we should not be afraid that they will send us very large images. <br><br>
    Also no information about the userid will be included (it would be the same 
    code like in the audio part, if were needed).

> **_NOTE:_** I'm using Haar Cascade Algorithm included in cv2 since is pretty good for the given task, it's trading precision for time. If we have a good server, we can user some ML models instead here, for example, see: [insightface.ai](https://insightface.ai/).


## File structure you should get
```
📦TelegramBotPOC
 ┣ 📂.venv
 ┣ 📂data
 ┃ ┣ 📂audio_data                                    # Here will be stored all the preprocessed audio records
 ┃ ┃ ┣ 📂<USER_TELEGRAM_UID>
 ┃ ┃ ┃ ┣ 📜audio_message_0.wav
 ┃ ┃ ┃ ┣ ...
 ┃ ┃ ┃ ┗ 📜audio_message_N.wav
 ┃ ┃ ┗ 📜.gitkeep
 ┃ ┣ 📂db
 ┃ ┃ ┗ 📜database_prod.db                            # DB Tables will be created after running python main.py
 ┃ ┣ 📂image_data                                    # The images which have some face on it will be stored here
 ┃ ┃ ┣ 📜.gitkeep
 ┃ ┃ ┗ 📜image_0.jpg
 ┃ ┣ 📜database_handler.py                           # All the database SQL functions are here
 ┃ ┗ 📜__init__.py
 ┣ 📂docs
 ┃ ┗ 📜opencv24.pdf
 ┣ 📂utils
 ┃ ┣ 📜audio_utils.py                                # All the main functions related to the audio processing are here
 ┃ ┣ 📜image_utils.py                                # All the main functions related to the image processing are here
 ┃ ┗ 📜__init__.py
 ┣ 📜.env
 ┣ 📜.gitignore
 ┣ 📜audioVisualizer.ipynb                           # Contains some plots to check visually that some changes on the audio were made
 ┣ 📜dbVisualizer.ipynb                              # Contains GET SQLs with Pandas representation of the DB Tables
 ┣ 📜main.py
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜__init__.py
```

## External useful links
- [python-telegram-bot](https://docs.python-telegram-bot.org/en/v21.1.1/index.html) documentation page.
- [librosa.load](https://librosa.org/doc/0.10.1/generated/librosa.load.html) was used to read the audio data and automatically resample to 16kHz.
- [Haar Cascade](https://towardsdatascience.com/face-detection-with-haar-cascade-727f68dafd08) face detection explanation.
