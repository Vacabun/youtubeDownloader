import sys,os
from PyQt5.QtWidgets import (QDesktopWidget,QWidget, QPushButton, QApplication,QHBoxLayout, QVBoxLayout, QLabel, QInputDialog,QFileDialog,QMessageBox,QProgressDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    downloadURL = ''
    saveAddress = ''
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        self.setWindowTitle('YouTube Downloader made by @Vacabun')
        self.setMinimumSize(520,400)
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # step1
        self.step1TextLable1 = QLabel("step1:", self)
        self.step1Button = QPushButton('设置代理', self)
        self.step1TextLable2 = QLabel("代理(不设置默认无代理):", self)
        self.step1VBox = QVBoxLayout()
        self.step1VBox.addWidget(self.step1TextLable1)
        self.step1VBox.addWidget(self.step1Button)
        self.step1VBox.addWidget(self.step1TextLable2)

        # step2

        self.step2TextLable1 = QLabel("step2:", self)
        self.step2Button = QPushButton('输入下载链接', self)
        self.step2TextLable2 = QLabel("下载链接:", self)
        self.step2VBox = QVBoxLayout()
        self.step2VBox.addWidget(self.step2TextLable1)
        self.step2VBox.addWidget(self.step2Button)
        self.step2VBox.addWidget(self.step2TextLable2)

        # step3
        self.step3TextLable1 = QLabel("step3:", self)
        self.step3Button = QPushButton('选择下载格式', self)
        self.step3TextLable2 = QLabel("下载格式:", self)
        self.step3VBox = QVBoxLayout()
        self.step3VBox.addWidget(self.step3TextLable1)
        self.step3VBox.addWidget(self.step3Button)
        self.step3VBox.addWidget(self.step3TextLable2)

        # step4
        self.step4TextLable1 = QLabel("step4:", self)
        self.step4Button = QPushButton('选择保存位置', self)
        self.step4TextLable2 = QLabel("保存位置:", self)
        self.step4VBox = QVBoxLayout()
        self.step4VBox.addWidget(self.step4TextLable1)
        self.step4VBox.addWidget(self.step4Button)
        self.step4VBox.addWidget(self.step4TextLable2)

        # step5
        self.step5TextLable1 = QLabel("step5:", self)
        self.step5Button = QPushButton('开始下载', self)
        self.step5TextLable2 = QLabel("", self)
        self.step5VBox = QVBoxLayout()
        self.step5VBox.addWidget(self.step5TextLable1)
        self.step5VBox.addWidget(self.step5Button)
        self.step5VBox.addWidget(self.step5TextLable2)

        self.mainVBox = QVBoxLayout()
        self.mainVBox.addLayout(self.step1VBox)
        self.mainVBox.addLayout(self.step2VBox)
        self.mainVBox.addLayout(self.step3VBox)
        self.mainVBox.addLayout(self.step4VBox)
        self.mainVBox.addLayout(self.step5VBox)

        #
        self.step1Button.clicked.connect(self.showDialog)
        self.step2Button.clicked.connect(self.showDialog)
        self.step3Button.clicked.connect(self.showDialog)
        self.step4Button.clicked.connect(self.showDialog)
        self.step5Button.clicked.connect(self.showDialog)

        self.setLayout(self.mainVBox)

        self.setWindowIcon(QIcon('download_128px.png'))

        self.show()
    def download(self):
        cmd = f'you-get -o {self.saveAddress} {self.downloadURL}'
        print(cmd)

    def showDialog(self):
        sender = self.sender()
        videoType = ['1080p','720p','480p']
        if sender == self.step1Button:
            text, ok = QInputDialog.getText(self, '设置代理', '请输入代理信息(如127.0.0.1:1080)：')
            if ok:
                if(text == ""):
                    self.step1TextLable2.setText("无代理" + text)
                else:
                    self.step1TextLable2.setText("设置代理:"+text)
        elif sender == self.step2Button:
            self.downloadURL, ok = QInputDialog.getText(self, '输入下载链接', '下载链接:')
            if ok:
                self.step2TextLable2.setText("下载链接:"+self.downloadURL)
        elif sender == self.step3Button:
            if len(videoType):
                text, ok = QInputDialog.getItem(self, '选择下载格式', '下载格式:',videoType)
                if ok:
                    self.step3TextLable2.setText("下载格式:" + str(text))
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('错误')
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("请输入下载地址")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
        elif sender == self.step4Button:
            self.saveAddress = QFileDialog.getExistingDirectory(self,"选择保存位置","C:/")
            self.step4TextLable2.setText("保存位置:" + str(self.saveAddress))
        elif sender == self.step5Button:
            self.download()
            num = 1000000
            progress = QProgressDialog(self)
            progress.setWindowTitle("请稍等")
            progress.setLabelText("正在下载...")
            progress.setCancelButtonText("取消")
            progress.setMinimumDuration(5)
            progress.setWindowModality(Qt.WindowModal)
            progress.setRange(0, num)
            for i in range(num):
                progress.setValue(i)
                if progress.wasCanceled():
                    QMessageBox.warning(self,"提示","操作失败")
                    break
            else:
                progress.setValue(num)
                QMessageBox.information(self,"提示","操作成功")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exit(app.exec_())
