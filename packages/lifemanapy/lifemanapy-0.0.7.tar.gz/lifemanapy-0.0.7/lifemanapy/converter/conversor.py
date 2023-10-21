import cv2
from PIL import Image
import numpy as np

def convert_to_HSV(img:Image):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV_FULL)