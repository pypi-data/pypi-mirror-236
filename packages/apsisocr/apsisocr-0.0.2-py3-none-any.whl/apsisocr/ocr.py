#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
from .utils import localize_box,LOG_INFO
from .apsisnet import ApsisNet
from .paddledbnet import PaddleDBNet
from .paddlesvtr import SVTRLCNet
from .densenet121bnencls import DenseNet121BnEnClassifier
import cv2
import copy
import pandas as pd
import numpy as np
#-------------------------
# class
#------------------------
class ApsisOCR(object):
    """
    ApsisOCR processes images for Optical Character Recognition (OCR) using
    models for Bangla and English text recognition, a text detector, and a language classifier.

    Attributes:
        bn_rec (ApsisNet): Instance of ApsisNet for Bangla text recognition.
        en_rec (SVTRLCNet): Instance of SVTRLCNet for English text recognition.
        detector (PaddleDBNet): Instance of PaddleDBNet for text detection.
        lang_cls (DenseNet121BnEnClassifier): Instance of DenseNet121BnEnClassifier for language classification.
    """

    def __init__(self) -> None:
        """
        Initialize ApsisOCR object with models for Bangla and English text recognition,
        a text detector, and a language classifier.
        """        
        self.bn_rec=ApsisNet()
        LOG_INFO("Loaded Bangla Model")
        self.en_rec=SVTRLCNet()
        LOG_INFO("Loaded English Model")
        self.detector=PaddleDBNet()        
        LOG_INFO("Loaded Paddle detector")
        self.lang_cls=DenseNet121BnEnClassifier()
        LOG_INFO("Loaded Language classifier")
        
    def process_boxes(self, word_boxes: np.ndarray, line_boxes: np.ndarray) -> pd.DataFrame:
        """
        Process word and line boxes to organize them into a DataFrame where line no and word no is determined

        Args:
            word_boxes (np.ndarray): List of word bounding boxes.
            line_boxes (np.ndarray): List of line bounding boxes.

        Returns:
            pd.DataFrame: DataFrame containing processed word boxes and line associations.
        """
        # line_boxes
        line_orgs=[]
        line_refs=[]
        for bno in range(len(line_boxes)):
            tmp_box = copy.deepcopy(line_boxes[bno])
            tmp_box=np.array(tmp_box).reshape(4,2)
            x2,x1=int(max(tmp_box[:,0])),int(min(tmp_box[:,0]))
            y2,y1=int(max(tmp_box[:,1])),int(min(tmp_box[:,1]))
            line_orgs.append([x1,y1,x2,y2])
            line_refs.append([x1,y1,x2,y2])
        
        # merge
        for lidx,box in enumerate(line_refs):
            if box is not None:
                for nidx in range(lidx+1,len(line_refs)):
                    x1,y1,x2,y2=box    
                    x1n,y1n,x2n,y2n=line_orgs[nidx]
                    dist=min([abs(y2-y1),abs(y2n-y1n)])
                    if abs(y1-y1n)<dist and abs(y2-y2n)<dist:
                        x1,x2,y1,y2=min([x1,x1n]),max([x2,x2n]),min([y1,y1n]),max([y2,y2n])
                        box=[x1,y1,x2,y2]
                        line_refs[lidx]=None
                        line_refs[nidx]=box
                        
        line_refs=[lr for lr in line_refs if lr is not None]
        # sort line refs based on Y-axis
        line_refs=sorted(line_refs,key=lambda x:x[1])     
        # word_boxes
        word_refs=[]
        for bno in range(len(word_boxes)):
            tmp_box = copy.deepcopy(word_boxes[bno])
            tmp_box=np.array(tmp_box).reshape(4,2)
            x2,x1=int(max(tmp_box[:,0])),int(min(tmp_box[:,0]))
            y2,y1=int(max(tmp_box[:,1])),int(min(tmp_box[:,1]))
            word_refs.append([x1,y1,x2,y2])
            
        
        data=pd.DataFrame({"words":word_refs,"word_ids":[i for i in range(len(word_refs))]})
        # detect line-word
        data["lines"]=data.words.apply(lambda x:localize_box(x,line_refs))
        data["lines"]=data.lines.apply(lambda x:int(x))
        # register as crop
        text_dict=[]
        for line in data.lines.unique():
            ldf=data.loc[data.lines==line]
            _boxes=ldf.words.tolist()
            _bids=ldf.word_ids.tolist()
            _,bids=zip(*sorted(zip(_boxes,_bids),key=lambda x: x[0][0]))
            for idx,bid in enumerate(bids):
                _dict={"line_no":line,"word_no":idx,"crop_id":bid,"poly":word_boxes[bid]}
                text_dict.append(_dict)
        data=pd.DataFrame(text_dict)
        return data
    
    def __call__(self, img_path: str) -> dict:
        """
        Perform OCR on an image.

        Args:
            img_path (str): Path to the image file.

        Returns:
            dict: OCR results containing recognized text and associated information. The dictionary has the following structre
                  {
                    "text" : multiline text with newline separators
                    "result" : list a dictionaries that contains the following structre:
                              {
                                "line_no" : the line number of the word
                                "word_no" : the word number in the line 
                                "poly"    : the four point polygonal bounding box of the word in the image
                                "text"    : the recognized text 
                                "lang"    : the classified language code
                              }
                  }
        """  
        result=[]
        # -----------------------start-----------------------
        img=cv2.imread(img_path)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # text detection
        line_boxes=self.detector.get_line_boxes(img)
        word_boxes=self.detector.get_word_boxes(img)
        crops=self.detector.get_crops(img,word_boxes)
        # line-word sorting
        df=self.process_boxes(word_boxes,line_boxes)

        #--------------------------------classification------------------------------------
        langs=self.lang_cls.infer(crops)
        df["lang"]=langs
        # language classification
        bn_df=df.loc[df.lang=="bn"]
        en_df=df.loc[df.lang=="en"]
        bn_ids=bn_df.crop_id.tolist()
        bn_word_crops=[crops[i] for i  in bn_ids]
        en_ids=en_df.crop_id.tolist()
        en_word_crops=[crops[i] for i  in en_ids]
        
        #--------------------------------bangla------------------------------------
        bn_text=self.bn_rec.infer(bn_word_crops)
        bn_df["text"]=bn_text
        #--------------------------------english------------------------------------
        en_text=self.en_rec.infer(en_word_crops)
        en_df["text"]=en_text
        #--------------------------------combine data------------------------------------
        df=pd.concat([bn_df,en_df],ignore_index=True)
        df=df.sort_values('line_no')
        # format
        for idx in range(len(df)):
            data={}
            data["line_no"]=int(df.iloc[idx,0])
            data["word_no"]=int(df.iloc[idx,1])
            # array 
            poly_res=  []
            poly    =  df.iloc[idx,3]
            poly    = np.array(poly).reshape(4,2)
            for pair in poly:
                _pair=[float(pair[0]),float(pair[1])]
                poly_res.append(_pair)
            
            data["poly"]   =poly_res
            data["text"]   =df.iloc[idx,5]
            data["lang"]   =df.iloc[idx,4]
            result.append(data)
        #--------------------------------combine------------------------------------
        # lines
        df=pd.DataFrame(result)
        df=df[["text","line_no","word_no"]]
        lines=[]
        for line in df.line_no.unique():
            ldf=df.loc[df.line_no==line]
            ldf.reset_index(drop=True,inplace=True)
            ldf=ldf.sort_values('word_no')
            _ltext=''
            for idx in range(len(ldf)):
                text=ldf.iloc[idx,0]
                _ltext+=' '+text
            lines.append(_ltext)
        text="\n".join(lines)

        # format output
        output={}
        output["result"]=result
        output["text"]=text  
        return output
