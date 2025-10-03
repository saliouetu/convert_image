from PIL import Image
def convert_png_to_svg(img) : 
    """

    """
    image = Image.open(img)
    
    width, height = img.size
    color_per_hexagon = []
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            color_hexagon = []
            for i in range(10):
                color_hexagon.append()






if __name__ == "__main__":
    convert_png_to_svg("../images/hexagon.jpg")  





