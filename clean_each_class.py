import json
import requests
import random
from PIL import Image
import os 
import shutil
import argparse
import warnings
warnings.filterwarnings("error")
import numpy as np
"""

3
4
8
10
12
13
15
21
22
23
24
26
28
29
31
34
35
42
45
61
62
63
67
70
71
75
80
86
91
92
93
94
101
103
113
126

"""


parser = argparse.ArgumentParser()
parser.add_argument( '--label_index', type=int )
args = parser.parse_args()
LABEL_INDEX = args.label_index


# create folder 
folder = str(LABEL_INDEX)


# some downloaded images are not readable, remove them
images = os.listdir( folder ) 
images.sort()
images = [  os.path.join(folder, item) for item in images  ]
count = 0 
for image_path in images:

    try:
        img = Image.open(image_path).convert('RGB')
    except: 
        breakpoint()


    img.close() 

