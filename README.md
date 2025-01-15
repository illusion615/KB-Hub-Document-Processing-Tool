# Document Processing Application

This project is a document processing application that allows users to upload PDF, Word, and PowerPoint documents. Each page of the uploaded documents is converted into images for user review. The application also includes a setup panel for user login to the Microsoft Power Platform Dataverse environment, enabling data entry for knowledge topics and the uploading of images to a specified table.

## Features

- Upload documents in PDF, Word, and PPT formats.
- Convert each page of the documents into images.
- User authentication for Microsoft Dataverse.
- Data entry for knowledge topics.
- Upload images to a specified Dataverse table.

## Project Structure

```
document-processing-app
├── src
│   ├── app.py
│   ├── document_processing
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   ├── word_processor.py
│   │   └── ppt_processor.py
│   ├── image_conversion
│   │   ├── __init__.py
│   │   └── converter.py
│   ├── user_auth
│   │   ├── __init__.py
│   │   └── login.py
│   ├── dataverse_integration
│   │   ├── __init__.py
│   │   └── dataverse_client.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd document-processing-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Access the application in your web browser at `http://localhost:5000`.

3. Follow the on-screen instructions to upload documents and manage your data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.