from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel, QStackedWidget, QVBoxLayout, QWidget ,QAction
import sys
from file import dataEncrypt, dataFind

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loc")
        self.setGeometry(100,100,400,300)
        self.setAcceptDrops(True)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Add the initial welcome label to the stack
        self.welcome_label = QLabel("Welcome! Select an action from the menu.")
        self.stack.addWidget(self.welcome_label)
        
        self.encrypt_widget = dataEncrypt()
        self.stack.addWidget(self.encrypt_widget)

        self.find_widget = dataFind()
        self.stack.addWidget(self.find_widget)
        self.show_data_find()

        self.menu_bar = self.menuBar()
        menu_data = self.menu_bar.addMenu("Data")
        
        data_encrypt = QAction("Encrypt Data", self)
        data_encrypt.triggered.connect(self.show_data_encrypt)
        menu_data.addAction(data_encrypt)
        
        data_find = QAction("Find Duplicated Data", self)
        data_find.triggered.connect(self.show_data_find)
        menu_data.addAction(data_find)

    def show_data_encrypt(self):
        self.stack.setCurrentWidget(self.encrypt_widget)
    
    def show_data_find(self):
        self.stack.setCurrentWidget(self.find_widget)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
