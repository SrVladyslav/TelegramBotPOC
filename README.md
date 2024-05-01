# Develop a Telegram / WhatsApp Bot that can:

## Tasks to do:
- Save audio messages from dialogues to a database (DBMS or disk) by user IDs.
   Audio should be converted to wav format with a sampling rate of 16kHz. Recording format: uid -> [audio_message_0, audio_message_1, ..., audio_message_N].

- Determines whether there is a face in the photos being sent or not, saves only those where it is


## Steps to start the bot

### Install venv
```
python -m venv .venv
source .venv/Scripts/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

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
    are named as [image_<0>.jpg, ..., image_<N>.jpg] with its original sizes. <br><br>
    Also no information about the userid will be included (it would be the same 
    code like in the audio part, if were needed).

> **_NOTE:_** I'm using Haar Cascade Algorithm included in cv2 since is pretty good for the given task, it's trading precision for time. If we have a good server, we can user some ML models instead here, for example, see: [insightface.ai](https://insightface.ai/).
