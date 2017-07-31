import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar
from PyQt5.QtCore import QCoreApplication
import urllib.request,json
import requests,os,time,urllib3
from multiprocessing import Queue


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data=""
        self.downloadURL=""
        self.title=""
        self.length=""
        self.hasConverted=0
        self.logo=QLabel(self)
        self.videoNameLabel=QLabel(self)
        self.videoLenLabel=QLabel(self)
        self.progressbar=QProgressBar(self)


        self.btnDownload=QPushButton('Convert',self)
        self.btnClear=QPushButton('Clear',self)
        self.msg = QMessageBox()
        self.urlLabel=QLabel(self)
        self.urlTextBox=QTextEdit(self)
        subMenuQuit = QAction(QtGui.QIcon(''), "&Quit", self)
        subMenuQuit.setShortcut("Ctrl+Q")
        subMenuQuit.setStatusTip("Quit")
        subMenuQuit.triggered.connect(self.quit)

        subMenuAbout = QAction(QtGui.QIcon(''), "&About", self)
        subMenuAbout.setShortcut("Ctrl+I")
        subMenuAbout.setStatusTip("About the Application")
        subMenuAbout.triggered.connect(self.about)


        self.statusBar()

        mainMenu=self.menuBar()
        fileMenu=mainMenu.addMenu("&File")
        fileMenu.addAction(subMenuQuit)

        aboutMenu=mainMenu.addMenu("&About")
        aboutMenu.addAction(subMenuAbout)


        self.initUI()

    def initUI(self):

        self.logo.setGeometry(100,40,300,60)
        self.logo.setStyleSheet("padding: 5px;")
        self.logo.setPixmap(QtGui.QPixmap(os.getcwd()+"/logo.png"))

        self.videoNameLabel.move(10,210)
        self.videoNameLabel.setFixedWidth(400)
        self.videoNameLabel.setText("Name: <b>None</b>")
        self.videoLenLabel.move(10, 230)
        self.videoLenLabel.setText("Length: <b>0s</b>")




        self.btnClear.move(240,160)
        self.btnClear.resize(100,40)
        btnClearText=self.btnClear.font()
        btnClearText.setPointSize(15)
        self.btnClear.setFont(btnClearText)
        self.btnClear.setIcon(QtGui.QIcon('clear.png'))
        self.btnClear.clicked.connect(self.clear)


        self.btnDownload.move(350, 160)
        self.btnDownload.resize(130, 40)
        btnDownloadText = self.btnDownload.font()
        btnDownloadText.setPointSize(15)
        self.btnDownload.setFont(btnDownloadText)
        self.btnDownload.clicked.connect(self.convertanddownload)
        self.btnDownload.setIcon(QtGui.QIcon('convert.png'))

        self.urlLabel.move(10,120)
        self.urlLabel.setText("URL: ")
        labelFont=self.urlLabel.font()
        labelFont.setPointSize(17)
        self.urlLabel.setFont(labelFont)
        self.urlTextBox.move(70,123)
        self.urlTextBox.resize(410,25)

        self.progressbar.move(10,280)
        self.progressbar.resize(460,20)


        self.resize(500,310)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setWindowTitle('Tube To Mp3')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.show()


    def clear(self):
        self.urlTextBox.setText("")
    def convertanddownload(self):
        if self.hasConverted==1:
            self.btnDownload.setEnabled(False)
            self.btnClear.setEnabled(False)
            self.downloadMP3(self.downloadURL,self.title.replace('/','//'))
        else:
            if self.urlTextBox.toPlainText().__contains__("youtube.com/watch?v="):
                self.urlTextBox.setEnabled(False)
                with urllib.request.urlopen("http://www.youtubeinmp3.com/fetch/?format=JSON&video="+self.urlTextBox.toPlainText()) as url:
                    self.data = json.loads(url.read().decode())
                self.downloadURL=self.data['link']
                self.title=self.data['title']
                self.length=self.data['length']
                self.btnDownload.setText("Download")
                self.btnDownload.setIcon(QtGui.QIcon('download.png'))
                self.videoNameLabel.setText("Name: <b>"+self.title+"</b>")
                self.videoLenLabel.setText("Length: <b>" + self.length + "s</b>")
                self.hasConverted=1
                self.btnClear.setEnabled(False)
            else:
                self.urlTextBox.setText("<p style='color:red;'>Please enter a valid youtube video url</p>")

    def downloadMP3(self,link,title):
        file_path ="./music/"+str(int(time.time()))+".mp3"
        if not os.path.exists(os.path.dirname(file_path)):
            os.mkdir(os.path.dirname(file_path))
        with open(file_path, "wb+") as f:
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    self.progressbar.setValue(done)
                self.downloadCompleteMsgBox()
            f.flush()
        self.btnClear.setEnabled(True)
        self.btnDownload.setEnabled(True)
        self.hasConverted=0
        self.urlTextBox.setEnabled(True)
        self.btnDownload.setText("Convert")
        self.btnDownload.setIcon(QtGui.QIcon('convert.png'))
        self.progressbar.setValue(0)

    def downloadCompleteMsgBox(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Downloaded "+self.title+".mp3 in /music folder in the installation directory successfully.")
        self.msg.setWindowTitle("Tube To Mp3")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msgbtn)
        self.msg.show()


    def about(self):

        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Tube To Mp3 developed by Anuran Barman\nAPI provided by www.youtubeinmp3.com")
        self.msg.setInformativeText("Email: anuranbarman@gmail.com")
        self.msg.setWindowTitle("Tube To Mp3")
        self.msg.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msgbtn)
        self.msg.show()

    def msgbtn(self):
        self.msg.hide()


    def quit(self):
        choice=QMessageBox.question(self,"Tube To Mp3","Are you sure you want to quit?",QMessageBox.Yes | QMessageBox.No)
        if choice==QMessageBox.Yes:
            sys.exit()
        else:
            pass


def internet_on():
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=10)
        return True
    except Exception:
        return False




def checkInternetMsg():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Tube To Mp3 requires internet connection to work.Connect to internet and try again.")
        msg.setWindowTitle("Tube To Mp3")
        msg.setWindowIcon(QtGui.QIcon('icon.ico'))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(QCoreApplication.instance().quit)
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not internet_on():
        checkInternetMsg()
    else:
        ex = Window()
        sys.exit(app.exec_())