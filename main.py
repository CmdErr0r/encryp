from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QFileDialog,QMenu,QAction
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import sys
import os
from data  import dataEncrypt, dataFind

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loc")
        self.setGeometry(100,100,400,300)
        self.setAcceptDrops(True)

        # Create the menu bar
        self.menu_bar = self.menuBar()

        # Create the File menu
        file_menu = self.menu_bar.addMenu("Encrypte Data")
        file_menu = self.menu_bar.addMenu("Find Dublicated Data")

        # Create actions for the File menu
        dataEncrypt = QAction("encrypte Data", self)
        dataEncrypt.triggered.connect(self.show_dataEncrypt)
        file_menu.addAction(dataEncrypt)

        dataFind = QAction("encrypte Data", self)
        dataFind.triggered.connect(self.show_dataFind)
        file_menu.addAction(dataFind)
        # dataFind = QAction("Find Dublicated Files", self)
        # dataFind.triggered.connect(self.show_crypt_section)

    def show_dataEncrypt(self):
        self.crypt_window = dataEncrypt()
        self.crypt_window.show()

    def show_dataFind(self):
        self.crypt_window = dataFind()
        self.crypt_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
