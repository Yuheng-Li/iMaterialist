import json
import requests
import random
from PIL import Image
import os 
import shutil
import argparse


"""

In the current folder, training and validation json must exist. 
They are from https://www.kaggle.com/c/imaterialist-challenge-furniture-2018/data.

By specifying class label, this script will download all images

"""


parser = argparse.ArgumentParser()
parser.add_argument( '--label_index', type=int )
args = parser.parse_args()
LABEL_INDEX = args.label_index


# create folder 
folder = str(LABEL_INDEX)
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)




def get_label_to_url(name):    
    
    with open(name) as f:
        data = json.load(f)
        
    images = data['images']
    annotations = data['annotations']
    assert len(images) == len(annotations)
    total = len(images)
    
    
    # create a mapping from image_id to url
    id_to_url = {}
    for image in images:
        image_id, url = image['image_id'], image['url']
        assert image_id not in id_to_url
        assert len(url)==1
        id_to_url[image_id] = url[0]
        
        
    # create a mapping (dict) from label to image_id
    label_to_id = {}
    for anno in annotations:
        image_id, label_id = anno['image_id'], anno['label_id']
        if label_id not in label_to_id:   
            label_to_id[label_id] = []
        label_to_id[label_id].append( image_id )
        
        
    # create a mapping (dict) from label to url
    label_to_url = {}
    for label, idxs in label_to_id.items():
        label_to_url[label] = []
        for idx in idxs:
            url = id_to_url[idx]
            label_to_url[label].append(url)
            
            
    return label_to_url




def merge_label_to_url( dict1, dict2 ):
    
    assert dict1.keys() == dict2.keys()
    
    new_dict = {}    
    for key in dict1:
        value1, value2 = dict1[key], dict2[key]
        new_dict[key] = value1+value2
        
    return new_dict



def filter_out_wrong_ext( urls, exts ):
    new_urls = []
    for url in urls:
        ext = url.split('.')[-1]
        if ext in exts:
            new_urls.append(url)
    return new_urls


# read and combine json files
training_label_to_url = get_label_to_url('train.json')
validation_label_to_url = get_label_to_url('validation.json')
label_to_url = merge_label_to_url(training_label_to_url, validation_label_to_url)

# select class
urls = label_to_url[LABEL_INDEX]
urls = filter_out_wrong_ext( urls, ['jpg', 'png', 'jpeg']  )


# download 
count = 0 
for url in urls:
    print(count)
    ext = url.split('.')[-1]
    
    try:
        img_data = requests.get(url).content
        yes = True
    except:
        yes = False 
        
    if yes:
        count += 1 
        name =   os.path.join(  folder, str(count).zfill(5)+'.'+ext  )
        with open( name, 'wb') as handler:
            handler.write(img_data)


print("total urls after filtering is", len(urls) )
print("total downladed images is", count )


# some downloaded images are not readable, remove them
images = os.listdir( folder ) 
images = [  os.path.join(folder, item) for item in all_images  ]
for image_path in images:

    try:
        img = Image.open(image_path).convert('RGB')
        img.close()
    except:
        os.remove(image_path)


print("total correctly downladed images is", len(os.listdir(folder)) )







