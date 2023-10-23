#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
import onnxruntime as ort
import numpy as np
import os
from pathlib import Path
from .utils import download,correctPadding
from .modules import LanguageClassifier
#-------------------------
# model class
#------------------------
class DenseNet121BnEnClassifier(LanguageClassifier):
    """
    A class representing the DenseNet121BnEn language classifier.

    Attributes:
        img_height (int): The height of the input image.
        img_width (int): The width of the input image.
        bnencls_gid (str): Google Drive ID for model weights.
        model (ort.InferenceSession): ONNX runtime inference session.
        label (list): List of language labels.

    Methods:
        get_model_weights: Get the path to the model weights.
        process_batch: Process a batch of image crops.
        infer: Perform inference on image crops.
    """

    def __init__(
        self,
        providers: list[str] = ['CUDAExecutionProvider', 'CPUExecutionProvider'],
        img_height: int = 32,
        img_width: int = 256,
        bnencls_gid: str = "15gEvkHNsoBQWSjNL7P5T1ehHM9ZPomro"
    )-> None:
        """
        Initialize the DenseNet121BnEn language classifier.

        Args:
            providers (list): List of execution providers for ONNX runtime.
            img_height (int): The height of the input image (default: 32).
            img_width (int): The width of the input image (default: 256).
            bnencls_gid (str): Google Drive ID for model weights (default: "15gEvk...").

        """
        super().__init__()
        self.img_height = img_height
        self.img_width = img_width
        self.bnencls_gid = bnencls_gid
        self.model = ort.InferenceSession(self.get_model_weights(), providers=providers)

        # Define the language labels
        self.label = ["bn", "en"]

    def get_model_weights(self) -> str:
        """
        Get the path to the model weights.

        Returns:
            str: Path to the model weights.
        """
        home_path = str(Path.home())
        weight_path = Path(home_path, ".apsis_ocr", "bnencls.onnx")
        weight_path = Path(weight_path).resolve()
        weight_path.parent.mkdir(exist_ok=True, parents=True)
        weight_path = str(weight_path)
        if not os.path.isfile(weight_path):
            download(self.bnencls_gid, weight_path)
        return weight_path

    def process_batch(self, crops: list[np.ndarray]) -> dict:
        """
        Process a batch of image crops.

        Args:
            crops (list[np.ndarray]): List of image crops.

        Returns:
            dict: Processed batch of image data. The dict is constructed as follows:
                 {
                    "input_1": np.ndarray of processed images
                 }
        """
        batch_img = []
        for img in crops:
            # Correct padding
            img, _ = correctPadding(img, (self.img_height, self.img_width))
            # Normalize
            img = img / 255.0
            # Extend batch
            img = np.expand_dims(img, axis=0)
            batch_img.append(img)

        # Stack images
        img = np.vstack(batch_img).astype(np.float32)
        return {'input_1': img}

    def infer(self, crops: list[np.ndarray], batch_size: int = 32) -> list[str]:
        """
        Perform inference on image crops.

        Args:
            crops (list[np.ndarray]): List of image crops.
            batch_size (int): Batch size for inference (default: 32).

        Returns:
            list[str]: List of inferred languages.
        """
        # Adjust batch size
        if len(crops) < batch_size:
            batch_size = len(crops)

        langs = []
        for idx in range(0, len(crops), batch_size):
            batch = crops[idx:idx + batch_size]
            inp = self.process_batch(batch)
            preds = self.model.run(None, inp)[0]
            preds = np.argmax(preds, axis=-1)
            labels = [self.label[int(pred)] for pred in preds]
            langs += labels

        return langs
