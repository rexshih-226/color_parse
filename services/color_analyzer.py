import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from color_parsing.services.color_mapper_lab import map_color_lab

def get_best_k(pixels):
    pixel_std = np.std(pixels)
    if pixel_std > 50: return 5  # 顏色豐富（漸層/拼色）
    if pixel_std > 20: return 3  # 普通
    return 2                     # 純色

def analyze_colors(image, mask, k=3, min_ratio=0.05):

    ### 避免去背邊緣的半透明/殘留背景污染顏色
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # 1. 套 mask
    pixels = image[mask > 200]

    if len(pixels) < 5:
        return [{"color": None, "percent": None}] *3

    # 2. 動態調整k
    sample_size = min(len(pixels), 100000)
    pixels_sampled = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
    dynamic_k = get_best_k(pixels_sampled)

    ### debug 用圖片
    if len(pixels_sampled) >= 10000:
        debug_img = pixels_sampled[:10000].reshape(100, 100, 3).astype(np.uint8)

        cv2.imwrite(
            "debug_kmeans_input.jpg",
            cv2.cvtColor(debug_img, cv2.COLOR_RGB2BGR)
        )

    ### 在LAB做KMeans
    pixels_lab = cv2.cvtColor(
        pixels.reshape(-1, 1, 3).astype(np.uint8),
        cv2.COLOR_RGB2LAB
    ).reshape(-1, 3)

    # 3. KMeans
    kmeans = MiniBatchKMeans(n_clusters=dynamic_k, n_init="auto", random_state=42)
    kmeans.fit(pixels_lab)

    centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    # 4. 統計比例
    counts = np.bincount(labels)
    total = len(labels)

    results = []
    for i in range(len(centers)):
        ratio = counts[i] / total
        if ratio >= 0.05:
            color_name = map_color_lab(centers[i])
            results.append((color_name, ratio))

    merged_same_color = {}
    for name, ratio in results:
        merged_same_color[name] = merged_same_color.get(name, 0) + ratio

    # 5. 排序
    results = sorted(merged_same_color.items(), key=lambda x: x[1], reverse=True)

    # 6. 補 NULL
    final = []
    for i in range(3):
        if i < len(results):
            final.append({
                "color": results[i][0],
                "percent": round(results[i][1] * 100, 1)
            })
        else:
            final.append({
                "color": None,
                "percent": None
            })

    return final
