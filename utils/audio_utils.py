from data.database_handler import DatabaseHandler
import soundfile as sf
import librosa
import io
import os 

class AudioUtils:
    def __init__(self):
        self._BASE_DIR = os.path.dirname( os.path.dirname(os.path.realpath(__file__)) )
        self._audio_data_path = self._BASE_DIR + '/data/audio_data/'
        self._new_sampling_rate = 16000 # Sampling rate of 16kHz  
        self._dh = DatabaseHandler()                                       

    def createNewFolder(self, folder_path:str):
        """Create a new folder at the specified path if it does not already exist.

        Args:
            folder_path (str): Path of the folder to be created.

        Raises:
            OSError: If an error occurs during folder creation.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
        except OSError as e:
            # Log: Error on folder creation.
            print(f'Error on folder creation {folder_path}: {e}')

    async def processAudio(self, audio_data:bytearray, user_id:int):
        """Process audio data and save it in the designated user's audio folder.

        Args:
            audio_data (bytearray): Raw audio data to be processed and saved.
            user_id (int): Unique Telegram identifier of the user associated with the audio.
        """
        if self._new_sampling_rate <= 0:
            return None
        
        # Load the data and resample to 16KHz rate.
        # NOTE: Use 'soxr_hq' to minimaze the Aliasing effect
        audio_wave, samplerate = librosa.load(io.BytesIO(audio_data), sr=self._new_sampling_rate, res_type='soxr_hq')
    
        # Create new Audio item in the DB and return the new User's audio name
        user_audio_filename = self._dh.postUserAudio(user_id)

        # The Audio recording format is: uid -> [audio_message_0, audio_message_1, ..., audio_message_N]
        usr_audio_folder_path = f'{self._BASE_DIR}/data/audio_data/{user_id}/'
        # Create new folder if it does not already exist.
        self.createNewFolder(usr_audio_folder_path)
        user_audio_path = f'{usr_audio_folder_path}/{user_audio_filename}.wav'
        # Store the audio in the corresponding PATH, with a sampling rate of 16kHz and in .WAV format
        sf.write(user_audio_path, audio_wave, self._new_sampling_rate, subtype='PCM_24')
        
        # NOTE: Descomment only for Dev purposes
        # self.get_sample_rate(user_audio_path) # Check      

    # DEVELOPMENT PURPOSES ======================================================================
    def get_sample_rate(self, path:str):
        """Check function to obtain the sample rate from audio of the given path"""
        data, samplerate = sf.read(path)
        print("New Sampling RATE: ",samplerate)

