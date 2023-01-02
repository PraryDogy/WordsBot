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


def den_light(input):
    """
    True = no light
    """
    candle_piece = cv2.imread('./candles/candle_piece_640.png', 0)
    img = cv2.imread(input, 0)

    res = cv2.matchTemplate(img, candle_piece, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)

    if loc[::-1][1].size > 0:
        print('true')
        return True

    return False


den_light('./test img/off.png')