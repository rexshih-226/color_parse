from color_parsing.models.bg_remover import remove_background
from color_parsing.services.color_analyzer import analyze_colors
from color_parsing.services.image_saver import save_image


def process_garment(image, filename, output_dir=None):
    # remove_background 回傳衣服遮罩 mask，以及去背後的 cutout 圖片。
    mask, cutout = remove_background(image)

    # 顏色分析只看 mask 範圍，避免背景顏色干擾辨識結果。
    colors = analyze_colors(image, mask)

    # 把去背後圖片存到後端指定的 output 資料夾。
    save_path = save_image(cutout, filename, output_dir=output_dir)

    return {
        "image_path": save_path,
        "colors": colors
    }
