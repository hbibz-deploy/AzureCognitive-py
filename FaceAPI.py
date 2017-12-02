import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import sys


def recogn(KEY, img_url):
    CF.Key.set(KEY)
    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/'
    CF.BaseUrl.set(BASE_URL)
    detected = CF.face.detect(img_url)
    print(detected)
    def getRectangle(faceDictionary):
        rect = faceDictionary['faceRectangle']
        left = rect['left']
        top = rect['top']
        bottom = left + rect['height']
        right = top + rect['width']
        return ((left, top), (bottom, right))

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(img)
    for face in detected:
        draw.rectangle(getRectangle(face), outline='blue')

    img.show()
recogn(sys.argv[1], sys.argv[2])
