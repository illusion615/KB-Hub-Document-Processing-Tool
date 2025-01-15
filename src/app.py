import sys
import logging
import os
import base64
import requests
import markdown2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QProgressBar, QListWidget, QGraphicsView, QGraphicsScene, QFormLayout, QLineEdit, QGroupBox, QListWidgetItem, QGraphicsPixmapItem, QComboBox, QCheckBox, QTextBrowser, QTextEdit, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize, QBuffer, QIODevice

from document_processing.pdf_processor import PdfProcessor
from document_processing.word_processor import WordProcessor
from document_processing.ppt_processor import PptProcessor
from logging_config import setup_logging

class DocumentProcessingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Knowledge Hub Document Processing Tool')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)  # Reduce spacing between panels

        # Gallery Panel
        gallery_layout = QVBoxLayout()
        gallery_layout.setSpacing(5)  # Reduce spacing within the gallery panel

        # Command Bar for Gallery Panel
        gallery_command_bar = QHBoxLayout()
        gallery_command_bar.setSpacing(5)  # Reduce spacing within the command bar
        self.upload_button = QPushButton('Upload Document')
        self.upload_button.setIcon(QIcon(self.get_icon_path('open_pdf.png')))
        self.upload_button.setToolTip('Upload Document')
        self.upload_button.clicked.connect(self.upload_document)
        gallery_command_bar.addWidget(self.upload_button)
        gallery_layout.addLayout(gallery_command_bar)

        # List widget to display thumbnails
        self.gallery_panel = QListWidget()
        self.gallery_panel.itemClicked.connect(self.display_selected_image)
        gallery_layout.addWidget(self.gallery_panel)

        # Wrap gallery layout in a widget
        gallery_widget = QWidget()
        gallery_widget.setLayout(gallery_layout)
        gallery_widget.setMinimumWidth(250)
        gallery_widget.setMaximumWidth(250)
        gallery_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        content_layout.addWidget(gallery_widget)

        # Content Display Area
        display_layout = QVBoxLayout()
        display_layout.setSpacing(5)  # Reduce spacing within the content display area

        # Command Bar for Content Display Area
        command_bar = QHBoxLayout()
        command_bar.setSpacing(5)  # Reduce spacing within the command bar
        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_in_button.setIcon(QIcon(self.get_icon_path('zoom_in.png')))
        self.zoom_in_button.setToolTip('Zoom In')
        self.zoom_in_button.clicked.connect(self.zoom_in)
        command_bar.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton('Zoom Out')
        self.zoom_out_button.setIcon(QIcon(self.get_icon_path('zoom_out.png')))
        self.zoom_out_button.setToolTip('Zoom Out')
        self.zoom_out_button.clicked.connect(self.zoom_out)
        command_bar.addWidget(self.zoom_out_button)

        self.fit_width_button = QPushButton('Fit Width')
        self.fit_width_button.setIcon(QIcon(self.get_icon_path('fit_width.png')))
        self.fit_width_button.setToolTip('Fit Width')
        self.fit_width_button.clicked.connect(self.fit_width)
        command_bar.addWidget(self.fit_width_button)

        self.fit_height_button = QPushButton('Fit Height')
        self.fit_height_button.setIcon(QIcon(self.get_icon_path('fit_height.png')))
        self.fit_height_button.setToolTip('Fit Height')
        self.fit_height_button.clicked.connect(self.fit_height)
        command_bar.addWidget(self.fit_height_button)

        display_layout.addLayout(command_bar)

        # Graphics view to display the selected image
        self.content_display = QGraphicsView()
        self.scene = QGraphicsScene()
        self.content_display.setScene(self.scene)
        display_layout.addWidget(self.content_display)

        # Wrap content display layout in a widget
        content_display_widget = QWidget()
        content_display_widget.setLayout(display_layout)
        content_display_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(content_display_widget)

        # Markdown Preview Panel
        markdown_preview_layout = QVBoxLayout()
        markdown_preview_layout.setSpacing(5)  # Reduce spacing within the markdown preview panel
        self.response_display = QTextBrowser()
        markdown_preview_layout.addWidget(self.response_display)

        # Wrap markdown preview layout in a widget
        markdown_preview_widget = QWidget()
        markdown_preview_widget.setLayout(markdown_preview_layout)
        markdown_preview_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(markdown_preview_widget)

        # Knowledge Hub Configuration Area
        knowledge_hub_layout = QVBoxLayout()
        knowledge_hub_layout.setSpacing(5)  # Reduce spacing within the knowledge hub configuration area

        # Command Bar for Knowledge Hub Configuration Area
        knowledge_command_bar = QHBoxLayout()
        knowledge_command_bar.setSpacing(5)  # Reduce spacing within the command bar
        self.save_setting_button = QPushButton("Save Setting")
        self.save_setting_button.setIcon(QIcon(self.get_icon_path('save.png')))
        self.save_setting_button.setToolTip('Save Setting')
        self.save_setting_button.clicked.connect(self.save_setting)
        knowledge_command_bar.addWidget(self.save_setting_button)

        self.upload_knowledge_button = QPushButton("Upload Knowledge")
        self.upload_knowledge_button.setIcon(QIcon(self.get_icon_path('upload_knowledge.png')))
        self.upload_knowledge_button.setToolTip('Upload Knowledge')
        self.upload_knowledge_button.clicked.connect(self.upload_knowledge)
        knowledge_command_bar.addWidget(self.upload_knowledge_button)

        knowledge_hub_layout.addLayout(knowledge_command_bar)

        # Dataverse Settings
        dataverse_group = QGroupBox("Dataverse Settings")
        dataverse_layout = QFormLayout()
        self.dataverse_url = QLineEdit()
        dataverse_layout.addRow("Dataverse URL:", self.dataverse_url)
        dataverse_group.setLayout(dataverse_layout)
        knowledge_hub_layout.addWidget(dataverse_group)

        # Knowledge Topic
        topic_group = QGroupBox("Knowledge Topic")
        topic_layout = QFormLayout()
        self.knowledge_topic = QLineEdit()
        topic_layout.addRow("Title:", self.knowledge_topic)
        self.group_name = QLineEdit()
        topic_layout.addRow("Group Name:", self.group_name)
        self.extraction_engine = QComboBox()
        self.extraction_engine.addItems(["AI Builder OCR", "GPT4o Multimodal", "Extract Text and Images"])
        topic_layout.addRow("Extraction Engine:", self.extraction_engine)
        self.generate_article_immediately = QCheckBox("Generate Article Immediately")
        topic_layout.addRow(self.generate_article_immediately)
        topic_group.setLayout(topic_layout)
        knowledge_hub_layout.addWidget(topic_group)

        # New Section for Web API
        webapi_group = QGroupBox("Web API Settings")
        webapi_layout = QFormLayout()
        self.prompt_input = QTextEdit()
        webapi_layout.addRow("Prompt:", self.prompt_input)
        self.gpt_version = QComboBox()
        self.gpt_version.addItems(["GPT4o", "GPT4o Multimodal", "GPT4o-mini"])
        webapi_layout.addRow("GPT Version:", self.gpt_version)
        self.send_request_button = QPushButton("Send Request")
        self.send_request_button.clicked.connect(self.send_request_to_webapi)
        webapi_layout.addRow(self.send_request_button)
        webapi_group.setLayout(webapi_layout)
        knowledge_hub_layout.addWidget(webapi_group)

        # Wrap knowledge hub layout in a widget
        knowledge_hub_widget = QWidget()
        knowledge_hub_widget.setLayout(knowledge_hub_layout)
        knowledge_hub_widget.setMinimumWidth(400)
        knowledge_hub_widget.setMaximumWidth(400)
        content_layout.addWidget(knowledge_hub_widget)

        # Add content layout to the main layout
        main_layout.addLayout(content_layout)

        # Status Bar
        status_bar = QHBoxLayout()
        status_bar.setSpacing(5)  # Reduce spacing within the status bar
        self.status_label = QLabel("Status: Ready")
        self.progress_bar = QProgressBar()
        status_bar.addWidget(self.status_label)
        status_bar.addWidget(self.progress_bar)
        main_layout.addLayout(status_bar)

        # Add main layout to the widget
        self.setLayout(main_layout)

        # Set up logging to update the status bar
        setup_logging(self.status_label)

        self.current_pixmap_item = None
        self.current_image = None

    def get_icon_path(self, icon_name):
        # Helper function to get the full path of an icon
        return os.path.join(os.path.dirname(__file__), 'icons', icon_name)

    def upload_document(self):
        # Function to handle document upload
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Document", "", "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;PPT Files (*.pptx)", options=options)
        if not file_path:
            QMessageBox.critical(self, 'Error', 'No file selected')
            logging.error("No file selected")
            return

        try:
            logging.info(f"Selected file: {file_path}")
            if file_path.endswith('.pdf'):
                processor = PdfProcessor(file_path)
                images = processor.convert_to_images()
            elif file_path.endswith('.docx'):
                processor = WordProcessor(file_path)
                text_content = processor.process_word()
                images = []  # Assuming no images for Word documents
            elif file_path.endswith('.pptx'):
                processor = PptProcessor(file_path)
                text_content = processor.process_ppt()
                images = []  # Assuming no images for PPT documents
            else:
                QMessageBox.critical(self, 'Error', 'Unsupported file type')
                logging.error("Unsupported file type")
                return

            logging.info(f"Processed {len(images)} pages")
            self.display_images(images)
            self.update_status(file_path, len(images))
            QMessageBox.information(self, 'Success', f'Processed {len(images)} pages')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to process document: {str(e)}')
            logging.error(f"Failed to process document: {str(e)}")

    def display_images(self, images):
        # Function to display thumbnails in the gallery panel
        self.images = images
        self.gallery_panel.clear()
        for i, image in enumerate(images):
            item_widget = QWidget()
            item_layout = QVBoxLayout()
            item_layout.setAlignment(Qt.AlignCenter)  # Align the layout to the center

            image = image.convert("RGBA")
            data = image.tobytes("raw", "RGBA")
            qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(self.gallery_panel.width() - 20, self.gallery_panel.width() - 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            icon_label = QLabel()
            icon_label.setPixmap(scaled_pixmap)
            item_layout.addWidget(icon_label, alignment=Qt.AlignCenter)  # Align the icon label to the center

            page_label = QLabel(f"Page {i + 1}")
            page_label.setAlignment(Qt.AlignCenter)
            item_layout.addWidget(page_label, alignment=Qt.AlignCenter)  # Align the page label to the center

            item_widget.setLayout(item_layout)
            item = QListWidgetItem(self.gallery_panel)
            item.setSizeHint(QSize(200, int(200 * image.height / image.width) + 20))
            self.gallery_panel.addItem(item)
            self.gallery_panel.setItemWidget(item, item_widget)

    def resizeEvent(self, event):
        # Override resizeEvent to resize thumbnails when the gallery panel is resized
        super().resizeEvent(event)
        self.update_thumbnails()

    def update_thumbnails(self):
        # Function to update the size of thumbnails to fit the width of the gallery panel
        for i in range(self.gallery_panel.count()):
            item = self.gallery_panel.item(i)
            widget = self.gallery_panel.itemWidget(item)
            if widget:
                icon_label = widget.findChild(QLabel)
                if icon_label:
                    pixmap = icon_label.pixmap()
                    if pixmap:
                        scaled_pixmap = pixmap.scaled(self.gallery_panel.width() - 20, self.gallery_panel.width() - 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        icon_label.setPixmap(scaled_pixmap)

    def display_selected_image(self, item):
        # Function to display the selected image in the content display area
        index = self.gallery_panel.row(item)
        image = self.images[index]
        self.current_image = image  # Store the current image
        image = image.convert("RGBA")
        data = image.tobytes("raw", "RGBA")
        qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)

        if self.current_pixmap_item:
            self.scene.removeItem(self.current_pixmap_item)

        self.current_pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.current_pixmap_item)
        self.content_display.fitInView(self.current_pixmap_item, Qt.KeepAspectRatio)

    def send_request_to_webapi(self):
        if not self.current_image:
            QMessageBox.critical(self, 'Error', 'No image selected')
            return

        try:
            # Convert the current image to base64
            buffered = QBuffer()
            buffered.open(QIODevice.WriteOnly)
            self.current_image.save(buffered, "PNG")
            img_str = base64.b64encode(buffered.data()).decode()

            # Prepare the request payload
            payload = {
                "Prompt": self.prompt_input.toPlainText(),
                "GPTVersion": self.gpt_version.currentText(),
                "File": img_str
            }

            # Send the request to the web API
            response = requests.post("https://prod-09.westus.logic.azure.com:443/workflows/a400f8e5c18a4b538e3964ad7d804a34/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=e3VkB-o7ZL_mTVQRdlTuy05cRspGZa4Dx1gh-EhNVGw", json=payload)
            response.raise_for_status()

            # Parse the JSON response
            response_json = response.json()
            output_markdown = response_json.get("output", "")

            # Convert Markdown to HTML
            output_html = markdown2.markdown(output_markdown)

            # Display the response
            self.response_display.setHtml(output_html)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to send request: {str(e)}')
            logging.error(f"Failed to send request: {str(e)}")

    def zoom_in(self):
        # Function to zoom in the content display area
        self.content_display.scale(1.2, 1.2)

    def zoom_out(self):
        # Function to zoom out the content display area
        self.content_display.scale(0.8, 0.8)

    def fit_width(self):
        # Function to fit the image to the width of the content display area
        if self.current_pixmap_item:
            self.content_display.fitInView(self.current_pixmap_item, Qt.KeepAspectRatioByExpanding)

    def fit_height(self):
        # Function to fit the image to the height of the content display area
        if self.current_pixmap_item:
            self.content_display.fitInView(self.current_pixmap_item, Qt.KeepAspectRatio)

    def update_status(self, file_path, total_pages):
        # Function to update the status bar
        self.status_label.setText(f"File: {file_path} | Pages: {total_pages} | Poppler Path: /opt/homebrew/bin")

    def save_setting(self):
        # Placeholder function to save settings
        logging.info("Settings saved")

    def upload_knowledge(self):
        # Placeholder function to upload knowledge
        logging.info("Knowledge uploaded")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DocumentProcessingApp()
    ex.show()
    sys.exit(app.exec_())