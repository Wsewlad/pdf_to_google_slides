# PDF to Google Slides Converter

A Python tool that automatically converts PDF files to PowerPoint presentations and uploads them to Google Drive.

## Features

- Converts PDF files to PowerPoint presentations
- Automatically uploads presentations to Google Drive
- Handles multiple PDF files in batch
- Provides detailed logging of the conversion process
- Error handling and recovery
- Automatically moves processed PDFs to a separate directory

## Prerequisites

- Python 3.7 or higher
- Google Drive API credentials
- Poppler (for PDF processing)

### Installing Poppler

#### macOS
```bash
brew install poppler
```

#### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

#### Windows
Download and install poppler from: http://blog.alivate.com.au/poppler-windows/

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf_to_google_slides
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Drive API:
   - Go to the Google Cloud Console
   - Create a new project
   - Enable the Google Drive API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials and save as `credentials.json` in the project root

## Usage

1. Place your PDF files in the `inputs/pdf` directory
2. Run the script:
```bash
python main.py
```

The script will:
1. Convert each PDF to a PowerPoint presentation
2. Upload the presentations to Google Drive
3. Move processed PDFs to the `outputs/processed` directory
4. Log the process in `conversion.log`

## Project Structure

```
pdf_to_google_slides/
├── inputs/
│   └── pdf/           # Place PDF files here
├── outputs/
│   ├── images/        # Temporary storage for converted images
│   └── processed/     # Processed PDF files are moved here
├── services/
│   ├── pdf/          # PDF processing services
│   ├── pptx/         # PowerPoint creation services
│   └── ggl/          # Google Drive services
├── main.py           # Main script
├── requirements.txt  # Python dependencies
└── credentials.json  # Google Drive API credentials
```

## Error Handling

The script includes comprehensive error handling and logging:
- All operations are logged to both console and `conversion.log`
- Errors are caught and logged with detailed information
- The script will exit with status code 1 if a fatal error occurs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.