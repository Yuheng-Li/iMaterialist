import json
import requests
import random
import torchvision.transforms.functional as TF
from PIL import Image
import os 
from torchvision import utils
import torch 

with open('train.json') as f:
     data = json.load(f)


images = data['images']
annotations = data['annotations']
assert len(images) == len(annotations)
total = len(images)



# create a mapping (dict) from image_id to url
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




# vis purpose: sample 16 images per class to see what are they 
# vis purpose: sample 16 images per class to see what are they 
possble_ext = ['jpg', 'png']  # I've checked that jpg (180133) and png(5016) account more than 95% of total. Just throw away rest ext for simplicity
for label, urls in label_to_url.items():
    print(label)
    count = 0 
    saved_images = []
    for url in urls:
        
        if count == 16:
            break
        
        ext = url.split('.')[-1]
        if ext in possble_ext:

            try:
                img_data = requests.get( url ).content
                yes = True
            except:
                yes = False 
            
            if yes:
                count += 1 
                temp_name = 'temp_'+str(count).zfill(5)+'.'+ext
                with open( temp_name, 'wb') as handler:
                    handler.write(img_data)
                saved_images.append(temp_name)
    

    save = []
    for saved_image in saved_images:
        try:
            img = Image.open(saved_image).resize((256,256)).convert('RGB')
        except:
            pass 
        save.append( TF.to_tensor(img)  )
        os.remove(saved_image)    
    torch.stack(save)    
    utils.save_image( save, str(label)+'.png' )

        
            
            
            
            
            
