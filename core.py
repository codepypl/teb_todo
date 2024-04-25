import sys

from PySide6.QtWidgets import QApplication

from ui.main import TaskManagerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())
