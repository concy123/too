import sys
from PyQt5.QtWidgets import QApplication
from uio import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())