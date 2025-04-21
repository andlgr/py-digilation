"""
MIT License
Created on: 2025-04-21
Author: André Reis <andre.lgr@gmail.com>
"""

import os
import sys

import cv2
from halation_engine import HalationEngine

class Converter():
    def __init__(self):
        self.halation_engine = HalationEngine()

    def load_jpeg_image(self, path):
        """Load JPEG image (8-bit sRGB) and convert to linear RGB."""
        return cv2.imread(path)

    def convert(self, in_path, out_path = "converted.jpeg"):
        original_image = self.load_jpeg_image(in_path)
        halated_image, _, _, _ = self.halation_engine.apply_advanced_halation(original_image)
        cv2.imwrite(out_path, halated_image)

if __name__ == "__main__":
    converter = Converter()

    if len(sys.argv) != 2:
        print("Usage: python main.py base_directory <scans all files and create a *_converted.png>")
        sys.exit(1)

    folder_in = sys.argv[1]

    in_files = []

    for _,_, files in os.walk(folder_in):
        for file_name in files:
            if 'jpeg' in file_name:
                in_files.append(file_name)

    for file_name in in_files:
        in_path = folder_in + '/' + file_name
        out_path = in_path + '_converted.png'
        print(in_path)
        print(out_path)
        converter.convert(in_path, out_path)
        print("")

