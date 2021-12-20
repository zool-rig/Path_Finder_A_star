import sys
import core.ui as path_finder_ui
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication([])
    ui = path_finder_ui.PathFinderUI()
    ui.show()
    sys.exit(app.exec_())
