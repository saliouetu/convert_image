import pytest
from convert_png_to_svg import *
from math import *

def test_axial_round():
    axial_round(-1.01924,54) == (-1,54)


def test_pixel_to_pointy_hex():
    pixel_to_pointy_hex(135,243,3) == (30, 32)


def test_hex_to_pixel():
    hex_to_pixel(30,32,3) == (135.0, 244.2191638672117) 


def test_hex_corner():
    hex_corner(12,15,3,2) == (10.5, 17.598076211353316)


def test_hexagon_points():
    hexagon_points(30,32,3) == "138.00,244.22 136.50,246.82 133.50,246.82 132.00,244.22 133.50,241.62 136.50,241.62"
