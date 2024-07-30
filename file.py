from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QFileDialog,QMenu,QAction
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os
from data import Lock, Find

class dataEncrypt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lock = Lock()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.messages = lambda a,stat:f"<div style='text-align: center;'><font color=\'{'green' if stat else 'red'}\'>{a}</font></div>"
        self.keyAcc = QLabel("")
        self.layout.addWidget(self.keyAcc)

        self.search = QPushButton("", self)
        self.search.clicked.connect(self.onDialogKey)
        self.layout.addWidget(self.search)

        self.btn_encrypt = QPushButton("No Key Found", self)
        self.btn_encrypt.clicked.connect(self.on_lock)
        self.layout.addWidget(self.btn_encrypt)

        self.updateLL()

    def updateLL(self):
        self.btn_encrypt.setText("Unlock File" if self.lock.key else "Lock File")
        self.search.setText("Remove Key" if self.lock.key else "Add Key" )

    def on_lock(self, e):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filePath, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*)", options=options)
        if filePath:
            msg = list(open(filePath).read())
            self.lock.msg = msg

            # unlock and write to a file
            if(self.lock.key):
                if self.lock.lockKey(unlock=True):
                    """ Decryption of File and updating the File """
                    open(filePath, 'w').write("".join(self.lock.msg))
                    self.keyAcc.setText(self.messages("File has Decrypted succsessfully", True))
                else:
                    self.keyAcc.setText(self.messages("key didnt match", False))
            else:
                """ Encryption of File and updating the File with a key """
                key = self.lock.generateKey()
                self.lock.reKey()
                self.lock.lockKey()

                open(os.path.join(os.path.dirname(filePath), os.path.basename(filePath) + ".key"), 'a').write("".join(["".join(i) for i in self.lock.key ]))
                open(filePath, 'w').write("".join(self.lock.msg))
                self.keyAcc.setText(self.messages("encrypted the file", True))
            
            self.updateLL()

    def onDialogKey(self):
        if(self.lock.key):
            self.lock.key=None
            self.updateLL()
            self.keyAcc.setText(f"<div style='text-align: center;'>{'Key Avaiable' if self.lock.key else 'No Key Found'}</div>")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filePath, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*)", options=options)
        if filePath:            
            key = open(filePath).read()
            self.lock.key = key
            trutly = self.lock.reKey()
            if not trutly: self.lock.key = None 
            print("BROKEN AND REMOVED KEY")

            self.keyAcc.setText(self.messages(f"{'Succsessfully Activated' if trutly else 'No Key Found'}", trutly))
            self.updateLL()

class dataFind(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("<div style='text-align: center;'>Nothing to Do</div>")
        self.layout.addWidget(self.label)

        self.btn = QPushButton("Select the files")
        self.btn.clicked.connect(self.is_same)
        self.layout.addWidget(self.btn)

    def is_same(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        files, _ = QFileDialog.getOpenFileNames(self, "Select a file", "", "All Files (*)", options=options)
        if files:
            f = Find()
            f.files = files
            f.give_id()

            # self.label.setText(f"<div style='text-align: center;'>{msgs}</div>")

            


