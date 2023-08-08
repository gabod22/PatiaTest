# -*- coding: latin-1 -*-
from ctypes import Array, c_char
from PIL import Image, ImageQt
from modules.iconExtractor import extract_icon, IconSize

def win32_icon_to_image(icon_bits: Array[c_char], size: IconSize) -> Image:
    """
    Convert a Windows GDI bitmap to a PIL `Image` instance.
    """
    w, h = IconSize.to_wh(size)
    img = Image.frombytes("RGBA", (w, h), icon_bits, "raw", "BGRA")
    return ImageQt.ImageQt(img)