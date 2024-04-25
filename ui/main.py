from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox,
                               QProgressBar, QHBoxLayout, QListWidgetItem)

from ui.options.category import CategoryManagerApp
from ui.options.priority import PriorityManagerApp
from ui.projects.add import AddProjectDialog
from ui.projects.edit import EditProjectDialog
import pandas as pd
from db import session, Task, Category, Priority, Project


class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.report_button = None
        self.priority_button = None
        self.category_button = None
        self.project_list = None
        self.central_widget = None
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.project_list = QListWidget()
        layout.addWidget(self.project_list)

        add_button = QPushButton("Dodaj projekt")
        add_button.clicked.connect(self.add_project)
        layout.addWidget(add_button)

        self.category_button = QPushButton("Zarządzaj kategoriami")
        self.category_button.clicked.connect(self.manage_categories)
        layout.addWidget(self.category_button)

        self.priority_button = QPushButton("Zarządzaj priorytetami")
        self.priority_button.clicked.connect(self.manage_priorities)
        layout.addWidget(self.priority_button)
        self.load_projects()

    def load_projects(self):
        self.project_list.clear()
        projects = session.query(Project).all()
        for project in projects:
            project_widget = self.create_project_widget(project)
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setSizeHint(project_widget.sizeHint())
            self.project_list.addItem(listWidgetItem)
            self.project_list.setItemWidget(listWidgetItem, project_widget)