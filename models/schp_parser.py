from rembg import remove
import numpy as np
import cv2


def remove_background(image):
    result = remove(image)

    # 轉 numpy
    img = np.array(result)

    # 取 alpha channel 當 mask
    if img.shape[2] == 4:
        mask = img[:, :, 3]
    else:
        mask = np.ones(img.shape[:2]) * 255

    return mask, img

def parse_clothes(image):
    # Placeholder implementation - replace with actual cloth parsing logic
    pass