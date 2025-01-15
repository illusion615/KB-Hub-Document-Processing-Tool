def save_uploaded_file(file, upload_folder):
    import os
    from werkzeug.utils import secure_filename

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_message(message):
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info(message)