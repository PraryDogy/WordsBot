from PIL import Image
import os
import cv2
import numpy as np

def create_avatar(image: Image):
    image = image.convert('RGBA')
    candle = Image.open('additional/candle.png')
    new_avatar = Image.new('RGBA', image.size)
    new_avatar = Image.alpha_composite(new_avatar, image)
    new_avatar = Image.alpha_composite(new_avatar, candle)
    new_avatar.save('/Users/Morkowik/Desktop/Evgeny/WordsBot/candled.png')
