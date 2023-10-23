#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
import fastdeploy as fd
import numpy as np
import os

from .utils import create_dir,maybe_download,download
from .modules import Recognizer
#-------------------------
# helpers
#------------------------
class SVTRLCNet(Recognizer):
    """
    A class representing the SVTRLCNet OCR recognizer.

    Attributes:
        use_gpu (bool): Whether to use GPU for recognition.
        device_id (int): GPU device ID to use (if use_gpu is True).
        svtr_model_url (str): URL to download the SVTR model.
        label_gid (str): Google Drive ID for label file.

    Methods:
        load_model: Load the recognition model.
        infer: Perform inference on image crops.
    """

    def __init__(
        self,
        use_gpu: bool = True,
        device_id: int = 0,
        svtr_model_url: str = 'https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar',
        label_gid: str = "14Otzvv81_XYV7JQxsfUVXzXa2kZLxQmd"
    )-> None:
        """
        Initialize the SVTRLCNet OCR recognizer.

        Args:
            use_gpu (bool): Whether to use GPU for recognition.
            device_id (int): GPU device ID to use (if use_gpu is True).
            svtr_model_url (str): URL to download the SVTR model.
            label_gid (str): Google Drive ID for label file.
        """

        super().__init__() 
        # set detection options
        self.rec_option = fd.RuntimeOption()
        if use_gpu:
            self.rec_option.use_gpu(device_id)
        
        # get models
        base_dir = os.path.expanduser("~/.apsis_ocr/")
        model_path=create_dir(base_dir,"svtr")
        maybe_download(model_path,svtr_model_url)
        # get label file
        self.rec_label_file=os.path.join(model_path,"en_dict.txt")
        if not os.path.exists(self.rec_label_file):
            download(label_gid,self.rec_label_file)
        
        # Create the rec_model
        self.model=self.load_model(model_path)
        
    def load_model(self,model_path : str) -> fd.vision.ocr.Recognizer:
        """
        Load the recognition model.

        Args:
            model_path (str): Path to the model directory.

        Returns:
            fd.vision.ocr.Recognizer: Loaded recognition model.
        """
        rec_model_file = os.path.join(model_path, "inference.pdmodel")
        rec_params_file = os.path.join(model_path, "inference.pdiparams")
        rec_model = fd.vision.ocr.Recognizer(rec_model_file, rec_params_file, self.rec_label_file, runtime_option=self.rec_option)
        return rec_model
    
    def infer(self, crops: list[np.ndarray], batch_size: int = 32) -> list[str]:
        """
        Perform inference on image crops.

        Args:
            crops (list[np.ndarray]): List of image crops.
            batch_size (int): Batch size for inference.

        Returns:
            list[str]: List of recognized texts.
        """    
        texts=[]
        for idx in range(0,len(crops),batch_size):
            batch=crops[idx:idx+batch_size]
            result = self.model.batch_predict(batch)
            texts+=result.text
        return texts
        
        
        