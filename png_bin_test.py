from PIL import Image, ImageFilter

def img_binarize(img: Image.Image, black_extpand: bool, threshold: int) -> Image.Image:
    img_bin = Image.eval(img.convert("L"), lambda p: 0 if p < threshold else 255)
    if black_extpand:
        return img_bin.filter(ImageFilter.MinFilter(size=3)) # 黑色周围3*3扩充均变为黑色
    else:
        return img_bin

png_path = "png_bin_test.png"

png = Image.open(png_path).convert("RGB")
png_bin = img_binarize(png, False, 195)
png_bin.show()