def route(image, mode="auto"):
    if mode == "garment":
        return "garment"
    elif mode == "person":
        return "person"

    # MVP：先手動指定
    return "garment"