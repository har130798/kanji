from words_to_pdf import *
from make_query import get_most_relevant
import sys
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, \
    QLineEdit, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, Qt

class Kanji(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Open File'
        self.left = 100
        self.top = 100
        self.initUI()

    def initUI(self):
        self.text = 'ただいまー '
        openAct = QAction(QIcon('exit.png'), '&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open a new file')
        openAct.triggered.connect(self.openFileNameDialog)

        self.statusBar()

        self.searchBar = QLineEdit(self)
        self.searchBar.move(20, 40)
        self.searchBar.resize(180, 20)
        self.searchBar.returnPressed.connect(self.on_click)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)

        self.result = QLabel(self.text, self)
        self.result.move(20, 110)
        self.result.setFont(QFont("Sans Serif", 25))

        self.result.resize(1560, 790)
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.searchButton = QPushButton('Search', self)
        self.searchButton.move(20, 70)

        self.searchButton.clicked.connect(self.on_click)
        self.searchButton.setAutoDefault(True)


        self.setGeometry(300, 300, 1600, 900)
        self.setWindowTitle('検索-Search and Record')
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.searchBar.text()
        self.text = get_most_relevant(textboxValue)
        self.result.setText(self.text)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            read_file(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kanji()
    sys.exit(app.exec_())