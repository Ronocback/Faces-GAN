import os
from shutil import copyfile

data_dir = "UTKFace" 
label_dir = "UTKFace/labelled"

images = os.listdir(data_dir)

for img in images:
    if img.endswith(".jpg"):
        path = data_dir+'/'+img
        age = int(img.split("_")[0])
        print(age)
        if age < 10:
            copyfile(path,label_dir+"/0-10/"+img)
        elif age < 20:
            copyfile(path,label_dir+"/10-20/"+img)
        elif age < 30:
            copyfile(path,label_dir+"/20-30/"+img)
        elif age < 40:
            copyfile(path,label_dir+"/30-40/"+img)
        elif age < 50:
            copyfile(path,label_dir+"/40-50/"+img)
        elif age < 60:
            copyfile(path,label_dir+"/50-60/"+img)
        elif age < 70:
            copyfile(path,label_dir+"/60-70/"+img)
        elif age < 80:
            copyfile(path,label_dir+"/70-80/"+img)
        elif age < 90:
            copyfile(path,label_dir+"/80-90/"+img)
        else:
            copyfile(path,label_dir+"/90+/"+img)
