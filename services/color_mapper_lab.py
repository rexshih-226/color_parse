import cv2
import numpy as np

def map_color_lab(lab_pixel):
    min_dist = float('inf')
    best_name = "未知"

    L,a,b = lab_pixel

    ### 白 / 灰 / 黑 低彩度色先判
    chroma = np.sqrt(a * a + b * b)

    ### 白色
    if L > 80 and chroma < 10:
        return "白色"

    ### 黑色
    if L < 20:
        return "黑色"

    ### 灰色
    if chroma < 8:
        return "灰色"

    # 3. 調整權重 (加強對色調 a, b 的敏感度)
    # 人眼對顏色的「種類」比「明暗」敏感，所以我們把 a, b 的權重調高
    weight = np.array([1.0, 1.8, 1.8]) # L 權重 1, a 權重 1.8, b 權重 1.8

    for name, lab_val in COLOR_LIBRARY_LAB.items():
        # 計算歐幾里德距離 (Delta E)
        dist = np.linalg.norm((lab_pixel - np.array(lab_val)) * weight)
        if dist < min_dist:
            min_dist = dist
            best_name = name
            
    return best_name

COLOR_LIBRARY_RGB = {
    "白色": [255, 255, 255],
    "灰色": [128, 128, 128],
    "黑色": [0, 0, 0],

    "紅色": [220, 20, 60],
    "粉紅色": [255, 182, 193],
    "橘色": [255, 165, 0],
    "黃色": [255, 215, 0],

    "米色": [245, 245, 220],
    "卡其色": [195, 176, 145],
    "棕色": [139, 69, 19],

    "綠色": [34, 139, 34],
    "藍綠色": [0, 128, 128],
    "藍色": [30, 144, 255],
    "紫色": [138, 43, 226],
}

COLOR_LIBRARY_LAB = {}

for name, rgb in COLOR_LIBRARY_RGB.items():

    rgb_np = np.uint8([[rgb]])

    ### OpenCV 的 LAB 轉換統一使用 RGB
    lab = cv2.cvtColor(
        rgb_np,
        cv2.COLOR_RGB2LAB
    )[0][0]

    COLOR_LIBRARY_LAB[name] = lab