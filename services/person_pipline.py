from color_parsing.models.schp_parser import parse_clothes
from color_parsing.services.color_analyzer import analyze_colors


def process_person(image):
    top_mask, bottom_mask = parse_clothes(image)

    top_colors = analyze_colors(image, top_mask)
    bottom_colors = analyze_colors(image, bottom_mask)

    return {
        "top": top_colors,
        "bottom": bottom_colors
    }
