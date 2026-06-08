import cv2
import os
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
TARGET_SIZE = 4000

def resize_and_pad(image, target_size=4000):
    h, w = image.shape[:2]

    # 等比例縮放
    scale = target_size / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)
    # resize
    if scale > 1:
        interp = cv2.INTER_CUBIC   # 放大
    else:
        interp = cv2.INTER_AREA    # 縮小
    resized = cv2.resize(image, (new_w, new_h), interpolation=interp)

    if resized.shape[2] == 4: #若有透明度(H, W, 4)
    # 拆 RGBA
        rgb = resized[:, :, :3]
        alpha = resized[:, :, 3] / 255.0

    # 建立白底畫布
    white_bg = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255
    resized = (
        rgb * alpha[..., None] + 
        white_bg * (1 - alpha[..., None])
    ).astype(np.uint8)

    canvas = np.ones((target_size, target_size, 3), dtype=np.uint8) * 255
    
    # 計算置中位置
    x_offset = (target_size - new_w) // 2
    y_offset = (target_size - new_h) // 2

    # 貼照片到畫布
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized

    return canvas

def save_image(image, filename, output_dir=OUTPUT_DIR):
    # output_dir 可由後端指定；未指定時使用 color_parsing 自己的 outputs 資料夾。
    if output_dir is None:
        output_dir = OUTPUT_DIR

    image = resize_and_pad(image, TARGET_SIZE)

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)

    # OpenCV 寫檔使用 BGR，這裡把 RGB 圖片轉成 BGR 後再儲存。
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # cv2.imwrite 在 Windows 中文路徑可能失敗，改用 imencode + tofile。
    ext = os.path.splitext(filename)[1] or ".png"
    success, encoded_image = cv2.imencode(ext, image_bgr)
    if not success:
        raise ValueError(f"Failed to encode image: {filename}")
    encoded_image.tofile(path)

    return path
