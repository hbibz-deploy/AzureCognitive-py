import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json, sys, json
import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw

def is_male(attr):
    if attr == 'Male':
        return True


def paraMade(key, url):
    subscription_key = key
    uri_base = 'https://eastus.api.cognitive.microsoft.com'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    body = {'url': url}

    try:
        response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)
        parsed = json.loads(response.text)
        print("\tIn this picture : %s\nWe found that:\n" % url)
        print (json.dumps(parsed, sort_keys=True, indent=2))
        print("\tThere are %i people" % parsed.__len__())
        for person in parsed:
            print("\t> Person %i:\n\tThis is a %i-year old %s" %(parsed.index(person)+1, person["faceAttributes"]["age"],person["faceAttributes"]["gender"]))
            if person["faceAttributes"]["hair"]["bald"] == 0.0:
                if is_male(person["faceAttributes"]["gender"]):
                    print("\tHis face, has the id %s" % (person['faceId']))
                else:
                    print("\tHer face, has the id %s"% (person['faceId']))
    except Exception as e:
        print('Error:')
        print(e)

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

paraMade(sys.argv[1], sys.argv[2])
recogn(sys.argv[1], sys.argv[2])
