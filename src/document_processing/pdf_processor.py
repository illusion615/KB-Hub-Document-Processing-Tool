import logging
from pdf2image import convert_from_path
from logging_config import setup_logging

# Ensure logging is set up
setup_logging()

class PdfProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info(f"Initialized PdfProcessor with file: {file_path}")

    def convert_to_images(self):
        logging.info("Converting PDF to images")
        images = convert_from_path(self.file_path)
        logging.info(f"Converted PDF to {len(images)} images")
        return images