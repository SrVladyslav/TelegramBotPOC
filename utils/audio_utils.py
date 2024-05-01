from data.database_handler import DatabaseHandler
import soundfile as sf
import io
import os 

class AudioUtils:
    def __init__(self):
        self._BASE_DIR = os.path.dirname( os.path.dirname(os.path.realpath(__file__)) )
        self._audio_data_path = self._BASE_DIR + '/data/audio_data/'
        self._new_sampling_rate = 16000     
        self._dh = DatabaseHandler()                                              # Sampling rate of 16kHz

    def createNewFolder(self, folder_path:str):
        try:
            os.makedirs(folder_path, exist_ok=True)
        except OSError as e:
            # Add Loggs here
            print(f'Error on folder creation {folder_path}: {e}')

    async def processAudio(self, audio_data:bytearray, user_id:int):
        """"""
        # Create new Audio item in the DB and return the new User's audio name
        user_audio_filename = self._dh.postUserAudio(user_id)

        # The Audio recording format is: uid -> [audio_message_0, audio_message_1, ..., audio_message_N]
        usr_audio_folder_path = f'{self._BASE_DIR}/data/audio_data/{user_id}/'
        self.createNewFolder(usr_audio_folder_path)

        # NOTE: I assume that there won't be any problems on file creation, otherwise
        # some fail-checking implementations will be needed since we already created 
        # a DB record for this audio.
        user_audio_path = f'{usr_audio_folder_path}/{user_audio_filename}.wav'

        # NOTE: In the prod case it would be good to also preprocess the audio,
        # for example, apply the Anti-Aliasing filter, this could be done with Scipy.
        data, samplerate = sf.read(io.BytesIO(audio_data))
        print("New filename: ", user_audio_path, 'Sampling: ', samplerate)

        sf.write(user_audio_path, data, self._new_sampling_rate)
        self.get_sample_rate(user_audio_path)

    def get_sample_rate(self, path:str):
        data, samplerate = sf.read(path)
        print("New RATE: ",samplerate)

