from PIL import Image
import pyautogui
from PIL import Image
import lifemanapy.constants.constants as const
import lifemanapy.configs.config as config
import numpy as np

def get_bar_dimensions(location_life):
    if location_life != None:
        inicio_x = location_life.left + 14
        inicio_y = location_life.top + 5
        final_x = inicio_x + 92
        final_y = location_life.height + location_life.top - 5
        return (inicio_x, inicio_y, final_x, final_y), (inicio_x, inicio_y+const.RANGE_MANA_POSITION, final_x, final_y+const.RANGE_MANA_POSITION)
    else:
        return None

def set_dimensions(img:Image):
    ar = Image.fromarray(np.uint8(np.asarray(const.HEART_IMAGE)))
    config.dimensions = get_bar_dimensions(location_life=pyautogui.locate(ar, img, confidence=.8))
