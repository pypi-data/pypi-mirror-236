import numpy as np
import cv2
from PIL import Image
import configs.config as cfg
import constants.constants as const
from converter.conversor import convert_to_HSV
from lifemanapy.dimensions.dimensions import set_dimensions as sdimensions

def get_bars(image:Image):
    img_t = image
    if(cfg.dimensions != None):
        life = img_t.crop(cfg.dimensions[0])
        mana = img_t.crop(cfg.dimensions[1])
        return convert_to_HSV(life), convert_to_HSV(mana)
    else:
        return (np.array([]), np.array([]))

def main(image:Image):
    life, mana = get_bars(image=image)

    if((life.size != 0) and (mana.size != 0)):
        life_mask = cv2.inRange(life, const.HSV_LIFE_MINIMA, const.HSV_LIFE_MAXIMA)
        mana_mask = cv2.inRange(mana, const.HSV_MANA_MINIMA, const.HSV_MANA_MAXIMA)

        life = int((np.count_nonzero(life_mask)/92)*100)
        mana = int((np.count_nonzero(mana_mask)/92)*100)

        return life, mana
    else:
        return None

def set_dimensions(image:Image):
    sdimensions(img=image)
