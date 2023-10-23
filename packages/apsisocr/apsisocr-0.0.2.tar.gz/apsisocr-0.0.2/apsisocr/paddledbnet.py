#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
import fastdeploy as fd
import cv2
import copy
import numpy as np
import os

from .utils import create_dir,maybe_download
from .modules import Detector
#-------------------------
# main class
#-------------------------
class PaddleDBNet(Detector):
    """
    A class representing the PaddleDBNet OCR detector.

    Attributes:
        use_gpu (bool): Whether to use GPU for detection.
        device_id (int): GPU device ID to use (if use_gpu is True).
        max_side_len (int): Maximum side length for resizing images.
        det_db_thresh (float): Detection threshold for DB model.
        det_db_box_thresh (float): Detection box threshold for DB model.
        det_db_unclip_ratio (float): Detection unclip ratio for DB model.
        det_db_score_mode (str): Detection score mode for DB model.
        use_dilation (bool): Whether to use dilation in DB model.
        line_model_url (str): URL to download the line detection model.
        word_model_url (str): URL to download the word detection model.

    Methods:
        load_model: Load the detection model.
        get_rotate_crop_image: Get a rotated and cropped image.
        get_word_boxes: Detect word boxes in an image.
        get_line_boxes: Detect line boxes in an image.
        get_crops: Extract cropped regions based on detected boxes.
    """
    def __init__(
        self,
        use_gpu: bool = True,
        device_id: int = 0,
        max_side_len: int = 960,
        det_db_thresh: float = 0.3,
        det_db_box_thresh: float = 0.6,
        det_db_unclip_ratio: float = 1.5,
        det_db_score_mode: str = "slow",
        use_dilation: bool = False,
        line_model_url: str = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar',
        word_model_url: str = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/multilingual/Multilingual_PP-OCRv3_det_infer.tar'
    ) -> None:
        """
        Initialize the PaddleDBNet OCR detector.

        Args:
            use_gpu (bool): Whether to use GPU for detection.
            device_id (int): GPU device ID to use (if use_gpu is True).
            max_side_len (int): Maximum side length for resizing images (default: 960).
            det_db_thresh (float): Detection threshold for DB model (default: 0.3).
            det_db_box_thresh (float): Detection box threshold for DB model (default: 0.6).
            det_db_unclip_ratio (float): Detection unclip ratio for DB model (default: 1.5).
            det_db_score_mode (str): Detection score mode for DB model (default: "slow").
            use_dilation (bool): Whether to use dilation in DB model (default: False).
            line_model_url (str): URL to download the line detection model.
            word_model_url (str): URL to download the word detection model.

        """
        super().__init__()
        # set detection options
        self.det_option = fd.RuntimeOption()
        if use_gpu:
            self.det_option.use_gpu(device_id)
        # set processor params
        self.max_side_len           =   max_side_len
        self.det_db_thresh          =   det_db_thresh
        self.det_db_box_thresh      =   det_db_box_thresh
        self.det_db_unclip_ratio    =   det_db_unclip_ratio
        self.det_db_score_mode      =   det_db_score_mode
        self.use_dilation           =   use_dilation
        # model paths
        base_dir = os.path.expanduser("~/.apsis_ocr/")
        line_model_path=create_dir(base_dir,"line")
        word_model_path=create_dir(base_dir,"word")
        maybe_download(line_model_path,line_model_url)
        maybe_download(word_model_path,word_model_url)
        
        # get models
        self.line_model=self.load_model(line_model_path)
        self.word_model=self.load_model(word_model_path)


    def load_model(self, model_path: str) -> fd.vision.ocr.DBDetector:
        """
        Load the detection model.

        Args:
            model_path (str): Path to the model directory.

        Returns:
            fd.vision.ocr.DBDetector: Loaded detection model.
        """
        det_model_file = os.path.join(model_path, "inference.pdmodel")
        det_params_file = os.path.join(model_path, "inference.pdiparams")
        det_model = fd.vision.ocr.DBDetector(det_model_file, det_params_file, runtime_option=self.det_option)
        # Set the preporcessing parameters
        det_model.preprocessor.max_side_len         = self.max_side_len
        # Set the postporcessing parameters
        det_model.postprocessor.det_db_thresh       = self.det_db_thresh
        det_model.postprocessor.det_db_box_thresh   = self.det_db_box_thresh
        det_model.postprocessor.det_db_unclip_ratio = self.det_db_unclip_ratio
        det_model.postprocessor.det_db_score_mode   = self.det_db_score_mode
        det_model.postprocessor.use_dilation        = self.use_dilation
        return det_model
    
            
    def get_rotate_crop_image(self, img: np.ndarray, points: np.ndarray) -> np.ndarray:
        """
        Get a rotated and cropped image.

        Args:
            img (np.ndarray): Input image.
            points (np.ndarray): np.ndarray of four points defining the region to crop.

        Returns:
            np.ndarray: Rotated and cropped image.
        """    # Use Green's theory to judge clockwise or counterclockwise
        # author: biyanhua
        d = 0.0
        for index in range(-1, 3):
            d += -0.5 * (points[index + 1][1] + points[index][1]) * (
                        points[index + 1][0] - points[index][0])
        if d < 0: # counterclockwise
            tmp = np.array(points)
            points[1], points[3] = tmp[3], tmp[1]

        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                            [img_crop_width, img_crop_height],
                            [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points, pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img
        
    def get_word_boxes(self, image: np.ndarray) -> np.ndarray:
        """
        Detect word boxes in an image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Array of detected word boxes.
        """    
        result = self.word_model.predict(image)
        return result.boxes

    def get_line_boxes(self,image : np.ndarray) -> np.ndarray:
        """
        Detect line boxes in an image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Array of detected word boxes.
        """    
        result = self.line_model.predict(image)
        return result.boxes
    
    def get_crops(self, img: np.ndarray, boxes: np.ndarray) -> list[np.ndarray]:
        """
        Extract locations and crops from the image based on detected boxes.

        Args:
            img (np.ndarray): Input image.
            boxes (np.ndarray): np.ndarray of detected boxes.

        Returns:
            list (np.ndarray): list of np.ndarray cropped images based on detected boxes.
        """
        crops=[]
        for bno in range(len(boxes)):
            tmp_box = copy.deepcopy(boxes[bno])
            x1,y1,x2,y2,x3,y3,x4,y4=tmp_box
            tmp_box=np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]],dtype=np.float32)
            img_crop = self.get_rotate_crop_image(img,tmp_box)
            crops.append(img_crop)

        return crops

