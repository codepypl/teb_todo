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

        self.category_label = QLabel("Kategoria:")
        self.category_input = QComboBox()
        categories = session.query(Category).all()
        for category in categories:
            self.category_input.addItem(str(category.name))
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        self.category_input.setCurrentText(project.category.name)

        self.deadline_label = QLabel("Data zakończenia:")
        self.deadline_input = QDateEdit(project.deadline)
        self.deadline_input.setCalendarPopup(True)
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        self.task_widget = QWidget()
        self.task_layout = QVBoxLayout()
        self.tasks_label = QLabel("Lista zadań:")
        self.task_widget.setLayout(self.task_layout)
        layout.addWidget(self.tasks_label)
        layout.addWidget(self.task_widget)

        self.add_task_button = QPushButton("Dodaj zadanie")
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.load_tasks()

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

        if not name:
            QMessageBox.warning(self, "Błąd", "Nazwa projektu nie może być pusta.")
            return
        if not description:
            QMessageBox.warning(self, "Błąd", "Opis projektu nie może być pusty.")
            return
        if deadline < QDate.currentDate().toPython():
            QMessageBox.warning(self, "Błąd", "Data zakończenia projektu nie może być wcześniejsza niż obecna data.")
            return

        priority_id = session.query(Priority).filter_by(name=priority).first().id
        category_id = session.query(Category).filter_by(name=category).first().id

        self.project.name = name
        self.project.description = description
        self.project.priority_id = priority_id
        self.project.category_id = category_id
        self.project.deadline = deadline
        session.commit()
        self.accept()

    def add_task(self):
        task, ok = QInputDialog.getText(self, 'Dodaj zadanie', 'Opisz zadanie:')
        if ok and task:
            existing_tasks = [checkbox.text() for checkbox in self.task_layout.findChildren(QCheckBox)]
            if task in existing_tasks:
                QMessageBox.warning(self, "Błąd", "To zadanie już istnieje w projekcie.")
                return
            new_task = Task(name=task, project_id=self.project.id)
            session.add(new_task)
            session.commit()
            self.load_tasks()

    def load_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            self.task_layout.itemAt(i).widget().setParent(None)

        tasks = session.query(Task).filter_by(project_id=self.project.id)
        for task in tasks:
            checkbox = QCheckBox(str(task.name))
            checkbox.setChecked(task.completed)
            checkbox.stateChanged.connect(lambda state, t=task: self.update_task_status(state, t))
            self.task_layout.addWidget(checkbox)

    def update_task_status(self, state, task):
        completed = bool(state)
        task.completed = completed
        session.commit()
