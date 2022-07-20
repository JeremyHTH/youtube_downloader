from pytube import YouTube
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
import sys
import os


class DownloaderGUI(QMainWindow):

    def __init__(self):
        super(DownloaderGUI, self).__init__()
        self.setGeometry(400,400,400,200)
        self.setWindowTitle('Youtube downloader')
        self.environment_setup()
        self.downloadType = 'Video' 
        self.resolution = 'Highest'
        Mainwidget = QWidget()
        Mainwidget.setLayout(self.WindowLayout)
        self.setCentralWidget(Mainwidget)
        self.status = QStatusBar()
        self.status.showMessage('status: idle')
        self.setStatusBar(self.status)

    def environment_setup(self):

        self.WindowLayout = QVBoxLayout()
        self.url_textbox = QLineEdit()

        formLayout = QFormLayout()
        formLayout.addRow('URL', self.url_textbox)

        choose = QComboBox()
        data = ['Video', 'Audio']
        choose.addItems(data)
        choose.setItemIcon(0,QIcon('image/video.jpeg'))
        choose.setItemIcon(1,QIcon('image/audio.png'))

        formLayout.addRow('Type',choose)
        choose.activated[str].connect(self._boxcallback)


        checkboxLayout = QHBoxLayout()
        checkbox1 = QRadioButton('Highest')
        checkbox1.setChecked(True)
        checkbox1.toggled.connect(self._checkboxCallback)

        checkbox2 = QRadioButton('720p')
        checkbox2.toggled.connect(self._checkboxCallback)

        checkbox3 = QRadioButton('480p')
        checkbox3.toggled.connect(self._checkboxCallback)
        
        checkboxLayout.addWidget(checkbox1)
        checkboxLayout.addWidget(checkbox2)
        checkboxLayout.addWidget(checkbox3)

        checkboxWidgit = QWidget()
        checkboxWidgit.setLayout(checkboxLayout)
        formLayout.addRow('Resolution',checkboxWidgit)
        # self.WindowLayout.addLayout(checkboxLayout)

        self.WindowLayout.addLayout(formLayout)
        
        # This is a example for BoxLayout

        # boxLayout = QHBoxLayout()
        # choose = QComboBox()
        # data = ['Video', 'Audio']
        # choose.addItems(data)
        # boxLayout.addWidget(choose)
        # self.WindowLayout.addLayout(boxLayout)


        buttonLayout = QHBoxLayout()

        download_button = QPushButton()
        download_button.setText('Download')
        download_button.clicked.connect(self._downloader)
        buttonLayout.addWidget(download_button)

        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self._clear)
        buttonLayout.addWidget(clear_button)

        self.WindowLayout.addLayout(buttonLayout)

    def keyPressEvent(self, event):
        
        if event.key() == 16777220 or event.key() == Qt.Key_Enter:
            self._downloader()
        

    def _downloader(self):
        url = self.url_textbox.text()
        try:
            youtube = YouTube(url)
            if self.downloadType == 'Video':
                if self.resolution == 'Highest':
                    video = youtube.streams.get_highest_resolution()
                else:
                    video = youtube.streams.get_by_resolution(self.resolution)

                if not os.path.exists('video'):
                    os.mkdir('video')

                self.status.showMessage('downloading video Resolution : {}'.format(self.resolution))
                video.download('video')
                self.status.showMessage('done. Idle')

            elif self.downloadType == 'Audio':
                audio = youtube.streams.filter(only_audio=True)

                if not os.path.exists('audio'):
                    os.mkdir('audio')

                self.status.showMessage('downloading Audio')
                audio[0].download('audio')
                self.status.showMessage('done. Idle')
        except Exception as e:
            print(e)
            QMessageBox.question(self,'Error',str(e))


    def _clear(self):
        self.url_textbox.setText('')

    def _boxcallback(self,text):
        self.downloadType = text

    def _checkboxCallback(self,value):
        
        Target = self.sender()

        if Target.isChecked() == True:
            self.resolution = Target.text()


def main():
    app = QApplication(sys.argv)
    win = DownloaderGUI()
    win.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()