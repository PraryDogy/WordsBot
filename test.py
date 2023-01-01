from PIL import Image
import os
import cv2
from matplotlib import pyplot as plt
import numpy as np

def create_avatar(image: Image):
    image = image.convert('RGBA')
    candle = Image.open('additional/candle.png')
    new_avatar = Image.new('RGBA', image.size)
    new_avatar = Image.alpha_composite(new_avatar, image)
    new_avatar = Image.alpha_composite(new_avatar, candle)
    new_avatar.save('/Users/Morkowik/Desktop/Evgeny/WordsBot/candled.png')


def compare(input):

    candle120 = '/Users/Morkowik/Desktop/Evgeny/WordsBot/candles/120.jpg'
    candle100 = '/Users/Morkowik/Desktop/Evgeny/WordsBot/candles/100.jpg'
    candle80 = '/Users/Morkowik/Desktop/Evgeny/WordsBot/candles/80.jpg'
    candle60 = '/Users/Morkowik/Desktop/Evgeny/WordsBot/candles/60.jpg'

    img = cv2.imread(input,0)
    templates = tuple(cv2.imread(im,0) for im in (candle120, candle100, candle80, candle60))

    for im, tmp in zip((candle120, candle100, candle80, candle60) ,templates):
        res = cv2.matchTemplate(img, tmp, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        print(im.split('/')[-1])

        if loc[::-1][1].size > 0:
            print('true')
            return True

    return False

compare('./off2.png')