import cv2
from PIL import Image
from gtts import gTTS
import os
path=f"{__file__}".replace("\\resources\\processing.py", "").replace("/resources/processing.py", "")

def gay(image):
    im = Image.open(image)
    im.seek(0)
    im.save(image)
    im.close()

    background = cv2.imread(image)
    overlay = cv2.imread(f'{path}/data/processing/gay.png'.replace("\\", "/"))

    background = cv2.resize(background, (720,720))
    overlay = cv2.resize(overlay, (720, 720))

    added_image = cv2.addWeighted(background,0.6,overlay,0.4,0)
    cv2.imwrite(f'{path}\\data\\temp\\result.png'.replace("\\", "/"), added_image)
    return(f'{path}\\data\\temp\\result.png'.replace("\\", "/"))

def resize(image, y, x):
    background = cv2.imread(image)
    background = cv2.resize(background, (y,x))

    cv2.imwrite(f'{path}\\data\\temp\\result.png'.replace("\\", "/"), background)
    return(f'{path}\\data\\temp\\result.png'.replace("\\", "/"))

def war(image):
    im = Image.open(image)
    im.seek(0)
    im.save(image)
    im.close()

    background = cv2.imread(image)
    overlay = cv2.imread(f'{path}/data/processing/helicopters.png'.replace("\\", "/"))

    background = cv2.resize(background, (1670,1108))
    overlay = cv2.resize(overlay, (1670,1108))

    added_image = cv2.addWeighted(background,0.6,overlay,0.4,0)
    cv2.imwrite(f'{path}\\data\\temp\\result.png'.replace("\\", "/"), added_image)
    return(f'{path}\\data\\temp\\result.png'.replace("\\", "/"))

def cum(image):
    im = Image.open(image)
    im.seek(0)
    im.save(image)
    im.close()

    background = cv2.imread(image)
    overlay = cv2.imread(f'{path}/data/processing/cum.png'.replace("\\", "/"))

    background = cv2.resize(background, (720,720))
    overlay = cv2.resize(overlay, (720,720))

    added_image = cv2.addWeighted(background,.7,overlay,.1,0)
    cv2.imwrite(f'{path}\\data\\temp\\result.png'.replace("\\", "/"), added_image)
    return(f'{path}\\data\\temp\\result.png'.replace("\\", "/"))

def tts(txt, languag):
    speech = gTTS(text = u'{}'.format(txt), lang = languag, slow = False)
    speech.save(f"{path}/data/temp/tts.mp3")
    return(f"{path}/data/temp/tts.mp3")