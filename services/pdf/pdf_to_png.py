#!/usr/bin/env python3
import os
import sys
from services.utils.logger import logger

# Mac users will have to install poppler. You can do this with brew:
# brew install poppler
from pdf2image import convert_from_path


def convert_pdf_to_png(pdf_path: str, output_folder: str, dpi=300):
    file_name = os.path.basename(pdf_path)
    logger.info(f"Converting {file_name} to PNG images")
    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    for i, image in enumerate(images, start=1):
        output_path = os.path.join(output_folder, f"page_{i}.png")
        image.save(output_path, "PNG")
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pdf_to_png <pdf_path> <output_folder> [dpi]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    convert_pdf_to_png(pdf_path, output_folder, dpi)
