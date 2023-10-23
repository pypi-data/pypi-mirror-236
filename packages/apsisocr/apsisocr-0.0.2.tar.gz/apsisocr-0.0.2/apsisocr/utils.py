#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#---------------------------------------------------------------
# imports
#---------------------------------------------------------------
from termcolor import colored
import cv2
import os 
import gdown
import sys
import tarfile
import requests
import numpy as np
from tqdm import tqdm
from typing import List, Tuple, Union
#---------------------------------------------------------------
def LOG_INFO(msg: str, mcolor: str = 'blue') -> None:
    """
    Log information with colored output.

    Args:
        msg (str): Message to be logged.
        mcolor (str): Color for the log message (default is 'blue').
    """
    print(colored("#LOG     :", 'green') + colored(msg, mcolor))

#---------------------------------------------------------------
def create_dir(base: str, ext: str) -> str:
    """
    Create a directory if it doesn't exist.

    Args:
        base (str): Base directory.
        ext (str): Extension or subdirectory name.

    Returns:
        str: Path to the created directory.
    """
    _path = os.path.join(base, ext)
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path

#---------------------------------------------------------------
def download(id: str, save_dir: str) -> None:
    """
    Download a file using its ID to the specified directory.

    Args:
        id (str): File ID or URL for download.
        save_dir (str): Directory to save the downloaded file.

    """
    gdown.download(id=id, output=save_dir, quiet=False)

#---------------------------------------------------------------
class dotdict(dict):
    """
    A dictionary with dot notation for attribute access.

    Attributes:
        __getattr__: Get attribute using dot notation.
        __setattr__: Set attribute using dot notation.
        __delattr__: Delete attribute using dot notation.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
#---------------------------------------------------------------
# localization helpers
#---------------------------------------------------------------

def intersection(boxA: Tuple[int, int, int, int], boxB: Tuple[int, int, int, int]) -> float:
    """
    Calculate the intersection over self area of two bounding boxes.

    Args:
        boxA (Tuple[int, int, int, int]): Bounding box coordinates (x_min, y_min, x_max, y_max).
        boxB (Tuple[int, int, int, int]): Bounding box coordinates (x_min, y_min, x_max, y_max).

    Returns:
        float: Intersection over self area.
    """    
    # boxA=ref
    # boxB=sig
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    x_min,y_min,x_max,y_max=boxB
    selfArea  = abs((y_max-y_min)*(x_max-x_min))
    return interArea/selfArea
#---------------------------------------------------------------
def localize_box(box: Tuple[int, int, int, int], region_boxes: List[Tuple[int, int, int, int]]) -> Union[int, None]:
    """
    Localize a bounding box within a list of region boxes.

    Args:
        box (Tuple[int, int, int, int]): Bounding box coordinates (x_min, y_min, x_max, y_max).
        region_boxes (List[Tuple[int, int, int, int]]): List of region bounding boxes.

    Returns:
        Union[int, None]: Index of the localized box in the region boxes, or None if no intersection found.
    """    
    max_ival=0
    box_id=None
    for idx,region_box in enumerate(region_boxes):
        ival=intersection(region_box,box)
        if ival==1:
            return idx
        if ival>max_ival:
            max_ival=ival
            box_id=idx
    if max_ival==0:
        return None
    return box_id
#-------------------------
# helpers from paddle ppocr network: 
# https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppocr/utils/network.py
#-------------------------
def download_with_progressbar(url: str, save_path: str) -> None:
    """
    Download a file from the given URL with a progress bar.

    Args:
        url (str): URL of the file to download.
        save_path (str): Path to save the downloaded file.

    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size_in_bytes = int(response.headers.get('content-length', 1))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(
            total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(save_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    else:
        # Log an error message and exit if the download fails.
        LOG_INFO("Something went wrong while downloading models", mcolor="red")
        sys.exit(0)


def maybe_download(model_storage_directory: str, url: str) -> None:
    """
    Download the model if it doesn't exist in the specified directory.

    Args:
        model_storage_directory (str): Directory to store the downloaded model.
        url (str): URL of the model.
    """
    # Check if the model files exist in the specified directory.
    tar_file_name_list = ['.pdiparams', '.pdiparams.info', '.pdmodel']
    params_file = os.path.join(model_storage_directory, 'inference.pdiparams')
    model_file = os.path.join(model_storage_directory, 'inference.pdmodel')
    
    # If the model files do not exist, proceed with downloading and extraction.
    if not os.path.exists(params_file) or not os.path.exists(model_file):
        assert url.endswith('.tar'), 'Only supports tar compressed package'
        tmp_path = os.path.join(model_storage_directory, url.split('/')[-1])
        print('download {} to {}'.format(url, tmp_path))
        os.makedirs(model_storage_directory, exist_ok=True)
        
        # Download the model with a progress bar.
        download_with_progressbar(url, tmp_path)
        
        # Extract and save the model files.
        with tarfile.open(tmp_path, 'r') as tarObj:
            for member in tarObj.getmembers():
                filename = None
                for tar_file_name in tar_file_name_list:
                    if member.name.endswith(tar_file_name):
                        filename = 'inference' + tar_file_name
                if filename is None:
                    continue
                file = tarObj.extractfile(member)
                with open(os.path.join(model_storage_directory, filename), 'wb') as f:
                    f.write(file.read())
        os.remove(tmp_path)

#-------------------------
# crop processing helpers
#------------------------

def padWordImage(img: np.ndarray, pad_loc: str, pad_dim: int, pad_val: int) -> np.ndarray:
    """
    Pad the word image based on specified padding location and dimensions.

    Args:
        img (numpy.ndarray): Input image.
        pad_loc (str): Location for padding, 'lr' for left-right or 'tb' for top-bottom.
        pad_dim (int): Dimension for padding.
        pad_val (int): Padding value.

    Returns:
        numpy.ndarray: Padded image.
    """    
    if pad_loc == "lr":
        # Padding on left-right (horizontal)
        h, w, d = img.shape
        # Calculate pad widths
        pad_width = pad_dim - w
        # Create the pad
        pad = np.ones((h, pad_width, 3)) * pad_val
        # Concatenate the pad to the image
        img = np.concatenate([img, pad], axis=1)
    else:
        # Padding on top-bottom (vertical)
        h, w, d = img.shape
        # Calculate pad heights
        if h >= pad_dim:
            return img
        else:
            pad_height = pad_dim - h
            # Create the pad
            pad = np.ones((pad_height, w, 3)) * pad_val
            # Concatenate the pad to the image
            img = np.concatenate([img, pad], axis=0)
    return img.astype("uint8")    
#---------------------------------------------------------------
def correctPadding(img: np.ndarray, dim: Tuple[int, int], pvalue: int = 255) -> Tuple[np.ndarray, int]:
    """
    Correct the padding of the word image based on the specified dimensions.

    Args:
        img (numpy.ndarray): Input image.
        dim (Tuple[int, int]): Desired dimensions (height, width).
        pvalue (int): Padding value.

    Returns:
        tuple: Resized and padded image, mask indicating the width after padding.
    """    
    img_height, img_width = dim
    mask = 0
    
    # Check for padding
    h, w, d = img.shape
    
    # Resize image based on aspect ratio
    w_new = int(img_height * w / h)
    img = cv2.resize(img, (w_new, img_height))
    h, w, d = img.shape
    
    if w > img_width:
        # For larger width, resize based on aspect ratio
        h_new = int(img_width * h / w)
        img = cv2.resize(img, (img_width, h_new))
        # Pad the image (top-bottom)
        img = padWordImage(img, pad_loc="tb", pad_dim=img_height, pad_val=pvalue)
        mask = img_width
    elif w < img_width:
        # Pad the image (left-right)
        img = padWordImage(img, pad_loc="lr", pad_dim=img_width, pad_val=pvalue)
        mask = w
    
    # Resize the image to the desired dimensions
    img = cv2.resize(img, (img_width, img_height))
    
    return img, mask