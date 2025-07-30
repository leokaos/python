import PIL.Image
import pilgram

img = PIL.Image.open("GOPR0271.JPG")

pilgram.lofi(img).save("churros.jpg")

import base64

with open("GOPR0271.JPG", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print(encoded_string)