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

        self.description_label = QLabel("Opis projektu:")
        self.description_input = QTextEdit(project.description)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        self.priority_label = QLabel("Priorytet:")
        self.priority_input = QComboBox()
        priorities = session.query(Priority).all()
        for priority in priorities:
            self.priority_input.addItem(str(priority.name))
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)
        self.priority_input.setCurrentText(project.priority.name)
