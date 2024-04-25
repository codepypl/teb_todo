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

        self.category_label = QLabel("Kategoria:")
        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)

        self.deadline_label = QLabel("Data zakończenia:")
        self.deadline_input = QDateEdit()
        self.deadline_input.setDate(QDate.currentDate())
        self.deadline_input.setCalendarPopup(True)
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_project)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_project(self):
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        priority = self.priority_input.currentText()
        category = self.category_input.currentText()
        deadline = self.deadline_input.date().toPython()

        priority_id = session.query(Priority).filter_by(name=priority).first().id
        category_id = session.query(Category).filter_by(name=category).first().id

        new_project = Project(name=name, description=description, priority_id=priority_id,
                              category_id=category_id, deadline=deadline)
        session.add(new_project)
        session.commit()
        self.accept()

