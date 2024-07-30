from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os

class DropArea(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Your Key And File Here \n\n")
        self.setStyleSheet("""
            QLabel {
                border: 4px dashed #aaa;
                padding: 20px;
                background-color: #f0f0f0;
            }
        """)

        self.setAcceptDrops(True)  # Enable drag-and-drop

    def dragEnterEvent(self, event: QDragEnterEvent):
        print("Drag Enter Event Triggered")  # Debugging output
        
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        print("Drop Event Triggered")  # Debugging output

        file_urls = event.mimeData().urls()
        if not file_urls:
            print("No files found")
        for file_url in file_urls:
            file_path = file_url.toLocalFile()
            if os.path.isfile(file_path):
                print(f"File dropped: {file_path}")
            else:
                print(f"Not a file: {file_path}")

