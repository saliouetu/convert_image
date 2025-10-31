from PIL import Image
from math import sqrt, pi, cos, sin
from collections import defaultdict


def axial_round(q, r):
    """
    Round fractional axial hex coordinates (q, r) to the nearest hex cell.

    Args:
        q (float): Axial q-coordinate of the hex.
        r (float): Axial r-coordinate of the hex.

    Returns:
        tuple[int, int]: The rounded integer axial coordinates (q, r).
    """
    x, z = q, r
    y = -x - z
    rx, ry, rz = round(x), round(y), round(z)
    dx, dy, dz = abs(rx - x), abs(ry - y), abs(rz - z)
    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return (rx, rz)


def pixel_to_pointy_hex(x, y, size):
    """
    Convert pixel coordinates (x, y) to axial hex coordinates (q, r)
    for a pointy-topped hex grid.

    Args:
        x (float): Pixel x-coordinate.
        y (float): Pixel y-coordinate.
        size (float): Hexagon radius (distance from center to corner).

    Returns:
        tuple[int, int]: The axial hex coordinates (q, r).
    """
    x /= size
    y /= size
    q = (2 / 3) * x
    r = (sqrt(3) / 3) * y - (1 / 3) * x
    return axial_round(q, r)


def hex_to_pixel(q, r, size):
    """
    Convert axial hex coordinates (q, r) to pixel center coordinates (x, y).

    Args:
        q (int): Axial q-coordinate of the hex.
        r (int): Axial r-coordinate of the hex.
        size (float): Hexagon radius (distance from center to corner).

    Returns:
        tuple[float, float]: Pixel coordinates (x, y) of the hex center.
    """
    x = size * (3/2) * q
    y = size * sqrt(3) * (q/2 + r)
    return x, y


def hex_corner(cx, cy, size, i):
    """
    Compute the coordinates of the i-th corner of a pointy-topped hexagon.

    Args:
        cx (float): X-coordinate of the hexagon center.
        cy (float): Y-coordinate of the hexagon center.
        size (float): Hexagon radius.
        i (int): Corner index (0–5).

    Returns:
        tuple[float, float]: Pixel coordinates (x, y) of the corner.
    """
    angle_deg = 60 * i
    angle_rad = pi / 180 * angle_deg
    return (cx + size * cos(angle_rad), cy + size * sin(angle_rad))


def hexagon_points(q, r, size):
    """
    Compute the six corner points of a hexagon in SVG format.

    Args:
        q (int): Axial q-coordinate of the hex.
        r (int): Axial r-coordinate of the hex.
        size (float): Hexagon radius.

    Returns:
        str: Space-separated string of 'x,y' points for an SVG <polygon>.
    """
    cx, cy = hex_to_pixel(q, r, size)
    points = [hex_corner(cx, cy, size, i) for i in range(6)]
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points)


def convert_png_to_svg(img_path, output_path="output.svg"):
    """
    Convert a PNG image to an SVG made of colored hexagons.

    Each hexagon's color is the average of the pixels that fall within
    its corresponding region in the input image.

    Args:
        img_path (str): Path to the input PNG file.
        output_path (str, optional): Output SVG file name. Defaults to "output.svg".
    """
    image = Image.open(img_path).convert("RGB")
    width, height = image.size
    size =  height / (10 * sqrt(3))
    color_per_hexagon = defaultdict(list)

    for x in range(0, width, int(size / 2)):
        for y in range(0, height, int(size / 2)):
            pixel = image.getpixel((x, y))
            h = pixel_to_pointy_hex(x, y, size)
            color_per_hexagon[h].append(pixel)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'] 

    for (q, r), pixels in color_per_hexagon.items():
        n = len(pixels)
        r_avg = sum(p[0] for p in pixels) // n
        g_avg = sum(p[1] for p in pixels) // n
        b_avg = sum(p[2] for p in pixels) // n
        color_hex = f"#{r_avg:02x}{g_avg:02x}{b_avg:02x}"
        points = hexagon_points(q, r, size)
        svg.append(f'<polygon points="{points}" fill="{color_hex}" stroke="none" />')

    svg.append("</svg>")

    with open(output_path, "w") as f:
        f.write("\n".join(svg))

if __name__ == "__main__":
    convert_png_to_svg("./images/hexagon.jpg", "output.svg")
 





