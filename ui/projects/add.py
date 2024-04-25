from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QDateEdit, \
    QMessageBox

from db import Priority, Category, session, Project

class AddProjectDialog(QDialog):
    def __init__(self, categories, priorities):
        super().__init__()
        layout = QVBoxLayout()

        self.name_label = QLabel("Nazwa projektu:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.description_label = QLabel("Opis projektu:")
        self.description_input = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        self.priority_label = QLabel("Priorytet:")
        self.priority_input = QComboBox()
        self.priority_input.addItems(priorities)
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)