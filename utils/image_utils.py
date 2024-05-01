from data.database_handler import DatabaseHandler
import numpy as np
import uuid
import cv2
import os 

class ImageUtils:
    def __init__(self):
        self._BASE_DIR = os.path.dirname( os.path.dirname(os.path.realpath(__file__)) )
        self._audio_data_path = self._BASE_DIR + '/data/image_data/'
        self._dh = DatabaseHandler()  

    def count_directory_files(self) -> int:
        """ Counts the number of files in the image_data 
            NOTE: I assume that this directory only will contain images
        """
        if not os.path.isdir(self._audio_data_path):
            print(f"Error: '{self._audio_data_path}' is not a valid directory.")
            return -1
        return len(os.listdir(self._audio_data_path))

    def hasFaces(self, gray_img, scale_factor=1.1, min_neighbors=8, min_size=(30,30)) -> bool:
        """Applies Haar on a given image that searches for faces, 
            returns True if the image has faces, False otherwise.

        Args:
            gray_img (numpy.ndarray): Gray scaled image
            scale_factor (float, optional): Determines the factor of increase in window size. Defaults to 1.1.
            min_neighbors (int, optional): Defaults to 6.
            min_size (tuple, optional): Initial window size. Defaults to (30,30).

        Returns:
            bool: True if the image has faces, False otherwise.
        """
        haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces_info = haar_cascade.detectMultiScale(
            gray_img, 
            scaleFactor=scale_factor, 
            minNeighbors=min_neighbors, # Higher the value, less will be the number of FP. However, there is a chance of missing some unclear face traces.
            minSize=min_size
        )
        if len(faces_info) > 0:
            return True 
        return False
    
    async def processImage(self, img:bytearray) -> bool:
        # Loading the image 
        bytes_arr = bytes(img)
        # Rescaling
        # TODO?
        # Create the pixel matrix
        np_arr = np.frombuffer(bytes_arr, dtype=np.uint8)
        # Decode the matrix in grayscale because of the benefits for the algorithm
        gray_img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        if gray_img is None:
            # Log: Failed to process 
            print("Failed processing")
            return 
        
        # Save the photo if it contains a face in it
        # NOTE: 
        return self.hasFaces(gray_img)