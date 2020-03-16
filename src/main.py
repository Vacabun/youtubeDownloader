import sys, os, subprocess, threading, re
from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel,
                             QInputDialog, QFileDialog, QMessageBox, QProgressDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

formatlist = []
containerlist = []
qualitylist = []
sizelist = []
downloadOptions = []


class MainWindow(QWidget):
    systemRun = True
    ProxyInfo = ''
    downloadURL = ''
    downloadindex = -1
    saveAddress = 'c:\\'

    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        self.setWindowTitle('YouTube Downloader made by @Vacabun')
        self.setMinimumSize(520, 400)
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # step1
        self.step1TextLable1 = QLabel("step1:", self)
        self.step1Button = QPushButton('设置代理', self)
        self.step1TextLable2 = QLabel("代理:" + self.ProxyInfo, self)
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
        self.step5TextLable2.setText('正在下载中，请稍后。')
        cmd = f'you-get --format={formatlist[self.downloadindex]} -o {self.saveAddress} {self.downloadURL}'
        # print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()
        output = output.decode('UTF-8')
        self.step5TextLable2.setText('下载已完成。')

    def getDoloadInfo(self):
        self.step5TextLable2.setText('解析下载地址中，请稍后。')
        cmd = f'you-get -i {self.downloadURL}'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()
        output = output.decode('UTF-8')
        pattern = re.compile(r'(- format[^#]*#{1})', re.M)  # 查找数字
        result = pattern.findall(output)
        formatlist.clear()
        containerlist.clear()
        qualitylist.clear()
        sizelist.clear()
        for match in result:
            # 解析format
            format = re.compile(r'(format.*\r\n)', re.M).findall(match)[0]
            format = re.sub(r'(\r\n)', r'', format)
            format = re.sub(r'format:( )*', r'', str(format))
            formatlist.append(format)
            # 解析container
            container = re.compile(r'(container.*\r\n)', re.M).findall(match)[0]
            container = re.sub(r'(\r\n)', r'', container)
            container = re.sub(r'container:( )*', r'', container)
            containerlist.append(container)
            # 解析quality
            quality = re.compile(r'(quality.*\r\n)', re.M).findall(match)[0]
            quality = re.sub(r'(\r\n)', r'', quality)
            quality = re.sub(r'quality:( )*', r'', quality)
            qualitylist.append(quality)
            # 解析size byte
            size = re.compile(r'\(.*\)', re.M).findall(match)[0]
            size = re.sub(r'[^0123456789]', '', size)
            sizelist.append(size)
        self.step5TextLable2.setText('解析下载地址完成。')

    def showDialog(self):
        sender = self.sender()
        if sender == self.step1Button:
            text, ok = QInputDialog.getText(self, '设置代理', '请输入代理信息(如127.0.0.1:1080)：')
            if ok:
                if (text.replace(' ', '') == ""):
                    self.step1TextLable2.setText("无代理" + text)
                else:
                    self.step1TextLable2.setText("设置代理:" + text)
        elif sender == self.step2Button:
            self.downloadURL, ok = QInputDialog.getText(self, '输入下载链接', '下载链接:')
            if ok:
                self.step2TextLable2.setText("下载链接:" + self.downloadURL)
                thread = threading.Thread(target=self.getDoloadInfo)
                thread.setDaemon(True)
                thread.start()

        elif sender == self.step3Button:
            if (len(formatlist)):
                downloadOptions.clear()
                for i in range(len(formatlist)):
                    downloadOptions.append(qualitylist[i] + ' ' + containerlist[i] + ' ' + sizelist[i] + 'bytes')
                if len(downloadOptions):
                    text, ok = QInputDialog.getItem(self, '选择下载格式', '下载格式:', downloadOptions)
                    if ok:
                        self.step3TextLable2.setText("下载格式:" + text)
                        self.downloadindex = downloadOptions.index(text)
                        # print(self.downloadindex)
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('错误')
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("请输入下载地址或等待下载地址解析完成.")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
        elif sender == self.step4Button:
            self.saveAddress = QFileDialog.getExistingDirectory(self, "选择保存位置", "C:/")
            self.step4TextLable2.setText("保存位置:" + self.saveAddress)
        elif sender == self.step5Button:

            thread = threading.Thread(target=self.download)
            thread.setDaemon(True)
            thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exit(app.exec_())
