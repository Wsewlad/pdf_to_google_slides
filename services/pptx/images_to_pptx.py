from pptx import Presentation
from pptx.util import Inches
import os
from PIL import Image


def compress_image(image_path, quality=85, max_size=(1600, 900)):
    """Compresses an image to reduce file size while maintaining quality."""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)  # Resize while maintaining aspect ratio
        compressed_path = image_path.replace(".png", "_compressed.png")
        img.save(compressed_path, "PNG", optimize=True, quality=quality)
    return compressed_path


def create_pptx_from_images(image_folder, pptx_filename="output.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(10)  # Standard Google Slides width
    prs.slide_height = Inches(4.41)  # Standard Google Slides height

    # Get and sort images (e.g., page_1.png, page_2.png)
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.endswith('.png')],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )

    for i in range(0, len(image_files), 2):  # Two images per slide
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide layout

        positions = [(0, 0), (prs.slide_width / 2, 0)]  # Left and right side

        for j, pos in enumerate(positions):
            if i + j < len(image_files):
                original_img_path = os.path.join(image_folder, image_files[i + j])
                compressed_img_path = compress_image(original_img_path)  # Compress image

                # Open image to get size
                with Image.open(compressed_img_path) as img:
                    img_width, img_height = img.size

                # Calculate scaling factor
                max_width = prs.slide_width / 2
                max_height = prs.slide_height
                width_ratio = max_width / img_width
                height_ratio = max_height / img_height
                scale = min(width_ratio, height_ratio)

                # Apply scaling
                new_width = img_width * scale
                new_height = img_height * scale

                # Center image
                x = pos[0] + (max_width - new_width) / 2
                y = (prs.slide_height - new_height) / 2

                slide.shapes.add_picture(compressed_img_path, x, y, width=new_width, height=new_height)

                # Delete compressed file after inserting
                os.remove(compressed_img_path)

    prs.save(pptx_filename)
    print(f"✅ Compressed PowerPoint saved as: {pptx_filename}")


if __name__ == "__main__":
    image_folder = "images"
    pptx_filename = "output.pptx"
    create_pptx_from_images(image_folder, pptx_filename)
