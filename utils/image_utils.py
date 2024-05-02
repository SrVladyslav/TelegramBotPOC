from data.database_handler import DatabaseHandler
import numpy as np
import cv2
import os 

class ImageUtils:
    def __init__(self):
        self._BASE_DIR = os.path.dirname( os.path.dirname(os.path.realpath(__file__)) )
        self._audio_data_path = self._BASE_DIR + '/data/image_data/'
        self._dh = DatabaseHandler()  

    def count_directory_files(self) -> int:
        """ Counts the number of files in the image_data 
            NOTE: I assume that this directory only will contain images and .gitignore
        """
        if not os.path.isdir(self._audio_data_path):
            print(f"Error: '{self._audio_data_path}' is not a valid directory.")
            return -1
        return len(os.listdir(self._audio_data_path)) - 1
    
    def resize_to_fit(self,image, max_width:int, max_height:int):
        """
        Resize the input image to fit within the specified maximum width and height,
        while maintaining the aspect ratio.
        
        Args:
            image (numpy.ndarray): Input image as a NumPy array.
            max_width (int): Maximum width constraint.
            max_height (int): Maximum height constraint.
        
        Returns:
            numpy.ndarray: Resized image.
        """
        if max_height < 1 or max_width < 1:
            return
        # Get the original image dimensions
        height, width = image.shape[:2]
        # Determine the aspect ratio of the original image
        aspect_ratio = width / float(height)
        
        # Calculate new dimensions based on the maximum width and height
        if width > max_width or height > max_height:
            if aspect_ratio > 1:                            # Landscape orientation
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            else:                                           # Portrait or square orientation
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
        else:
            # No resizing needed if the image already fits within the constraints
            new_width = width
            new_height = height
        
        # Resize the image using the calculated dimensions
        resized_image = cv2.resize(image, (new_width, new_height))
        
        return resized_image

    def hasFaces(self, gray_img, scale_factor=1.2, min_neighbors=6, min_size=(30,30)) -> bool:
        """Applies Haar on a given image that searches for faces, 
            returns True if the image has faces, False otherwise.

        Args:
            gray_img (numpy.ndarray): Gray scaled image
            scale_factor (float, optional): Determines the factor of increase in window size. Defaults to 1.2.
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
        """Process the input image to enhance features for face detection using Haar Cascade.

        Args:
            img (bytearray): Input image data in the form of a bytearray.

        Returns:
            bool: True if the processed image contains detected faces, otherwise False.
        """
        # Loading the image 
        bytes_arr = bytes(img)
        # Create the pixel matrix
        np_arr = np.frombuffer(bytes_arr, dtype=np.uint8)
        # Decode the matrix in grayscale because of the benefits for the algorithm
        gray_img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        # Resize the image to a smaller one if it's big enough
        gray_img = self.resize_to_fit(gray_img, 500, 500)
        # Apply histogram equalization to improve the contrast
        gray_img = cv2.equalizeHist(gray_img)
        # Reduce some noise and blemishes that can interfece with face detection
        smooth = cv2.GaussianBlur(gray_img, (25,25), 0)
        gray_img = cv2.divide(gray_img, smooth, scale=255)

        if gray_img is None:
            # Log: Failed to process 
            print("Failed processing")
            return 
        
        # Search for faces in the image
        # NOTE: Here I'm using Haar Cascade Algorithm included in cv2 since
        # is pretty good for the given task, it's trading precision for time.
        # If we have a good server, we can user some ML models instead here,
        # For example, see: insightface.ai
        return self.hasFaces(gray_img)