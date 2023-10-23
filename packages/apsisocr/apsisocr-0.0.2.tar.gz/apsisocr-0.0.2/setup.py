
#-*- coding: utf-8 -*-
#------------------------------------------------------------
from __future__ import print_function
#------------------------------------------------------------
from setuptools import setup, find_packages
import sys

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='apsisocr',
  version='0.0.2',
  description='Bangla English Mixed Languge Scene / printed OCR Toolkit',
  long_description=open('README.md',encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt',encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/mnansary/apsis-ocr/',  
  author='Nazmuddoha Ansary',
  author_email='nazmuddoha.ansary@apsissolutions.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['ocr','multilingual-ocr','scene ocr','apsisnet'], 
  packages=find_packages(),
  install_requires=['numpy', 
                    "matplotlib", 
                    "opencv-python",
                    "pandas",
                    "tqdm",
                    "termcolor",
                    "gdown",
                    "bnunicodenormalizer",
                    "flask",
                    "flask_cors",
                    "streamlit"]
)