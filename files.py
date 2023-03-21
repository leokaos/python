# import OS
import os
from PIL import Image
 
for x in os.listdir():
    if x.endswith(".webp"):
        full_name = os.path.basename(x)
        file_name = os.path.splitext(full_name)
        print(file_name[0])
        im = Image.open(x).convert("RGB")
        im.save(str(file_name[0]) + ".png", "png")
