import os
import sys
import logging
import shutil
from pathlib import Path
from typing import List
from services.pdf.pdf_to_png import convert_pdf_to_png
from services.pptx.images_to_pptx import create_pptx_from_images
from services.ggl.upload_to_drive import upload_to_google_drive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'input_dir': Path("inputs/pdf"),
    'output_dir': Path("outputs/images"),
    'output_pptx_dir': Path("outputs"),
    'processed_dir': Path("outputs/processed"),
    'supported_formats': ['.pdf']
}

def setup_directories() -> None:
    """Create necessary directories if they don't exist."""
    for directory in [CONFIG['input_dir'], CONFIG['output_dir'], CONFIG['output_pptx_dir'], CONFIG['processed_dir']]:
        directory.mkdir(parents=True, exist_ok=True)

def get_pdf_files() -> List[Path]:
    """Get list of PDF files from input directory."""
    try:
        return [f for f in CONFIG['input_dir'].glob("*.pdf")]
    except Exception as e:
        logger.error(f"Error reading input directory: {e}")
        raise

def clean_output_directory() -> None:
    """Clean the output directory of previous conversion files."""
    try:
        for f in CONFIG['output_dir'].glob("*"):
            f.unlink()
    except Exception as e:
        logger.error(f"Error cleaning output directory: {e}")
        raise

def process_pdf_file(pdf_path: Path) -> None:
    """Process a single PDF file through the conversion pipeline."""
    try:
        file_name = pdf_path.stem
        pptx_file = CONFIG['output_pptx_dir'] / f"{file_name}.pptx"
        
        logger.info(f"Processing {pdf_path.name}")
        
        # Step 1: Convert PDF to images
        logger.info("Converting PDF to images...")
        convert_pdf_to_png(pdf_path, CONFIG['output_dir'])
        
        # Step 2: Convert images to PowerPoint
        logger.info("Creating PowerPoint presentation...")
        create_pptx_from_images(CONFIG['output_dir'], pptx_file)
        
        # Step 3: Upload to Google Drive
        logger.info("Uploading to Google Drive...")
        upload_to_google_drive(pptx_file)
        
        # Step 4: Move processed PDF to processed directory
        processed_path = CONFIG['processed_dir'] / pdf_path.name
        shutil.move(str(pdf_path), str(processed_path))
        logger.info(f"Moved {pdf_path.name} to processed directory")
        
        logger.info(f"Successfully processed {pdf_path.name}")
        
    except Exception as e:
        logger.error(f"Error processing {pdf_path.name}: {e}")
        raise

def main():
    """Main function to orchestrate the PDF to PowerPoint conversion process."""
    try:
        setup_directories()
        pdf_files = get_pdf_files()
        
        if not pdf_files:
            logger.warning("No PDF files found in input directory")
            return
            
        for pdf_file in pdf_files:
            clean_output_directory()
            process_pdf_file(pdf_file)
            
        logger.info("✅ Process complete!")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

