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