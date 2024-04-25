from PySide6.QtCore import QDate
from PySide6.QtWidgets import QVBoxLayout, QDialog, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QWidget, \
    QPushButton, QInputDialog, QMessageBox, QCheckBox

from db import session, Priority, Category, Task


class EditProjectDialog(QDialog):
    def __init__(self, project):
        super().__init__()

        self.project = project

        layout = QVBoxLayout()

        self.name_label = QLabel("Nazwa projektu:")
        self.name_input = QLineEdit(project.name)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
