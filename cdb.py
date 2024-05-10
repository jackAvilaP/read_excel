import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image

def generate_barcode(num):

    barcode_format = barcode.get_barcode_class("code128")
    my_barcode = barcode_format(num, writer=ImageWriter())

    folder_path = "barcodes"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, num)
    my_barcode.save(file_path)



