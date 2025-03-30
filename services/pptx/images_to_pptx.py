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


def create_pptx_from_images(image_folder, pptx_filename="output.pptx", images_per_slide=2):
    """
    Create a PowerPoint presentation from images.
    
    Args:
        image_folder (str): Path to folder containing images
        pptx_filename (str): Output PowerPoint filename
        images_per_slide (int): Number of images per slide (1 or 2)
    """
    if images_per_slide not in [1, 2]:
        raise ValueError("images_per_slide must be 1 or 2")
        
    prs = Presentation()
    prs.slide_width = Inches(10)  # Standard Google Slides width
    prs.slide_height = Inches(4.41)  # Standard Google Slides height

    # Get and sort images (e.g., page_1.png, page_2.png)
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.endswith('.png')],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )

    # Calculate total number of slides
    total_slides = (len(image_files) + images_per_slide - 1) // images_per_slide
    
    # Adjust compression settings based on number of slides
    if total_slides > 50:
        compression_quality = 70  # Stronger compression for large presentations
        max_size = (1200, 675)   # Smaller maximum size for large presentations
        print(f"Large presentation detected ({total_slides} slides). Using stronger compression.")
    else:
        compression_quality = 85  # Normal compression
        max_size = (1600, 900)   # Standard maximum size
        print(f"Normal presentation ({total_slides} slides). Using standard compression.")

    for i in range(0, len(image_files), images_per_slide):
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide layout

        # Define positions based on number of images per slide
        if images_per_slide == 1:
            positions = [(0, 0)]  # Center position
        else:
            # Calculate positions for two images without spacing
            slide_center = prs.slide_width / 2
            positions = [
                (slide_center, 0),  # First image (right edge at center)
                (slide_center, 0)   # Second image (left edge at center)
            ]

        for j, pos in enumerate(positions):
            if i + j < len(image_files):
                original_img_path = os.path.join(image_folder, image_files[i + j])
                compressed_img_path = compress_image(original_img_path, quality=compression_quality, max_size=max_size)  # Compress image

                # Open image to get size
                with Image.open(compressed_img_path) as img:
                    img_width, img_height = img.size

                # Calculate scaling factor
                max_width = prs.slide_width / 2  # Use half of slide width for each image
                max_height = prs.slide_height
                width_ratio = max_width / img_width
                height_ratio = max_height / img_height
                scale = min(width_ratio, height_ratio)

                # Apply scaling
                new_width = img_width * scale
                new_height = img_height * scale

                # Position image
                if images_per_slide == 1:
                    # Center single image
                    x = (prs.slide_width - new_width) / 2
                else:
                    # For two images, position them without spacing
                    if j == 0:
                        # First image: align right edge to center
                        x = pos[0] - new_width
                    else:
                        # Second image: align left edge to center
                        x = pos[0]
                
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
