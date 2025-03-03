import os
import sys
from services.pdf.pdf_to_png import convert_pdf_to_png
from services.pptx.images_to_pptx import create_pptx_from_images
from services.ggl.upload_to_drive import upload_to_google_drive


# for all pdf files in inputs/pdf folder
files = [f for f in os.listdir("inputs/pdf") if f.endswith(".pdf")]
for file in files:
    file_name = file.split(".pdf")[0]
    pdf_path = os.path.join("inputs/pdf", file)
    output_folder = "outputs/images"
    pptx_file = f"outputs/{file_name}.pptx"

    # clean images folder
    for f in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, f))

    # Step 1: Convert PDF to images
    convert_pdf_to_png(pdf_path, output_folder)

    # Step 2: Convert images to PowerPoint
    create_pptx_from_images(output_folder, pptx_file)

    # Step 3: Upload to Google Drive
    upload_to_google_drive(pptx_file)

print("✅ Process complete!")

