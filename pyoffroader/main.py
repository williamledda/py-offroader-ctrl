import sys
from PySide2.QtWidgets import QApplication

import pyoffroader.controlapp.pyxtremew as ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ui.PyXtremeW()
    widget.show()

    exitStatus = app.exec_()

    sys.exit(exitStatus)
