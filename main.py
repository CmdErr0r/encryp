from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QFileDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import sys
import os
from encrypte import Lock

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loc")
        self.setGeometry(100,100,400,300)
        self.setAcceptDrops(True)
        self.lock = Lock()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # self.keyBlockContainer = QWidget()
        # self.keyBlockLayout = QHBoxLayout(self.keyBlockContainer)
        self.messages = lambda a,stat:f"<div style='text-align: center;'><font color=\'{'green' if stat else 'red'}\'>{a}</font></div>"
        self.keyAcc = QLabel("Key isnt activated")
        self.layout.addWidget(self.keyAcc)

        self.search = QPushButton("Add Key", self)
        self.search.clicked.connect(self.onDialogKey)
        self.layout.addWidget(self.search)

        # self.layout.addWidget(self.keyBlockLayout)

        # self.label.setAlignment(Qt.AlignCenter) 
        # self.layout.addWidget(self.label)

        self.btn_encrypt = QPushButton("Lock File", self)
        self.btn_encrypt.clicked.connect(self.on_lock)
        self.layout.addWidget(self.btn_encrypt)

        self.Kreset = QPushButton("Reset Key", self)
        self.Kreset.clicked.connect(self.on_KReset)

    def updateLL(self):
        self.btn_encrypt.setText("Unlock File" if self.lock.key else "Lock File")
        if self.lock.key:
            self.layout.addWidget(self.Kreset)
        else:
            self.layout.removeWidget(self.Kreset)
        self.keyAcc.setText(f"<div style='text-align: center;'>{'Key Avaiable' if self.lock.key else 'No Key Found'}</div>")

    def on_KReset(self, e):
        self.lock.key=None
        self.updateLL()

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
                    self.keyAcc.setText(self.messages("file has decrypted succsessfully", True))
                else:
                    self.keyAcc.setText(self.messages("key didnt match", False))
            else:
                """ Encryption of File and updating the File with a key """
                key = self.lock.generateKey()
                self.lock.reKey()
                self.lock.lockKey()

                open(os.path.join(os.path.dirname(filePath), os.path.splitext(os.path.basename(filePath))[0] +".key"), 'w').write("".join(["".join(i) for i in self.lock.key ]))
                open(filePath, 'w').write("".join(self.lock.msg))
                self.keyAcc.setText(self.messages("encrypted the file", True))
            
            self.updateLL()

    def onDialogKey(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filePath, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*)", options=options)
        if filePath:            
            
            # activate Key
            key = open(filePath).read()
            self.lock.key = key
            trutly = self.lock.reKey()

            self.keyAcc.setText(self.messages(f"{'Succsessfully Activated' if trutly else 'No Key Found'}", trutly))
            self.updateLL()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
