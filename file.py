from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QFileDialog,QMenu,QAction,QSizePolicy
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os
from data import Lock, getInfo, find

class subdata:
    def __init__(self):
        self.messages = lambda a,stat:f"<div style='text-align: center;'><font color=\'{'green' if stat==1 else ('black' if  stat==2 else 'red')}\'>{a}</font></div>"
        self.texture()

    def texture(self):
        self.lock = Lock()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0,0,0,0)

        self.header = QWidget()
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.header_layout = QVBoxLayout(self.header)
        self.header_layout.setContentsMargins(0,0,0,0)
        
        self.footer = QWidget()
        self.footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.footer_layout = QVBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.footer)

    def explorer(self, single=True):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        return [QFileDialog.getOpenFileNames, QFileDialog.getOpenFileName][single](self, "Select a file", "", "All Files (*)", options=options)

class dataEncrypt(QMainWindow, subdata):
    def __init__(self):
        super().__init__()

        self.keyAcc = QLabel(self.messages("Nothing to Do", 2))
        self.header_layout.addWidget(self.keyAcc)

        self.search = QPushButton("", self)
        self.search.clicked.connect(self.onDialogKey)
        self.footer_layout.addWidget(self.search)

        self.btn_encrypt = QPushButton("No Key Found", self)
        self.btn_encrypt.clicked.connect(self.on_lock)
        self.footer_layout.addWidget(self.btn_encrypt)

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
                    self.keyAcc.setText(self.messages("File has Decrypted succsessfully", 1))
                else:
                    self.keyAcc.setText(self.messages("key didnt match", 0))
            else:
                """ Encryption of File and updating the File with a key """
                key = self.lock.generateKey()
                self.lock.reKey()
                self.lock.lockKey()

                open(os.path.join(os.path.dirname(filePath), os.path.basename(filePath) + ".key"), 'a').write("".join(["".join(i) for i in self.lock.key ]))
                open(filePath, 'w').write("".join(self.lock.msg))
                self.keyAcc.setText(self.messages("encrypted the file", 1))
            
            self.updateLL()

    def onDialogKey(self):
        if(self.lock.key):
            self.lock.key=None
            self.updateLL()
            self.keyAcc.setText(f"<div style='text-align: center;'>{'Key Avaiable' if self.lock.key else 'No Key Found'}</div>")
            return

        filePath, _ = self.explorer()
        if filePath:            
            key = open(filePath).read()
            self.lock.key = key
            trutly = self.lock.reKey()
            if not trutly:
                self.lock.key = None 
                print("BROKEN AND REMOVED KEY")

            self.keyAcc.setText(self.messages(f"{'Succsessfully Activated' if trutly else 'No Key Found'}", int(trutly)))
            self.updateLL()

class dataFind(QMainWindow,subdata):
    def __init__(self):
        super().__init__()
        
        self.label = QLabel(self.messages("Nothing to Do",2))
        self.header_layout.addWidget(self.label)

        self.btn = QPushButton("Select the files")
        self.btn.clicked.connect(self.is_same)
        self.footer_layout.addWidget(self.btn) 

    def is_same(self):
        paths, _ = self.explorer(False)
        texts = lambda info:  f"""<div>
                <div>File Path: {info[0]}</div>
                <div>File Size: {info[1]} bytes</div>"""
                # <div>Last Access Time: {info[2]}</div>
                # <div>Last Modification Time: {info[3]}</div>
                # <div>Creation Time: {info[4]}</div>
                # </div>
        msgs = []
        
        if paths:
            files = find(paths)
            for file in files:
                if len(file) > 1:
                    msgs.append("".join(list(map(texts, getInfo(file)))))
        
        t= ""
        for msg in msgs:
            t += "<div>"+"".join(msg)+"</div>"
        
        self.label.setText(t)

class dataInfo(QMainWindow,subdata):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self.messages("hi",2))
        self.header_layout.addWidget(self.label)

        self.btn = QPushButton("Select the File")
        self.btn.clicked.connect(self.is_info)
        self.footer_layout.addWidget(self.btn)
        
    def is_info(self):
        path, _ = self.explorer()
        self.label.setText(self.messages(f"path finded {path}",2))