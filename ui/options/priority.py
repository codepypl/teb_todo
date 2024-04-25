from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QLineEdit

from db import session, Priority


class PriorityManagerApp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zarządzanie Priorytetami")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.priority_list = QListWidget()
        layout.addWidget(self.priority_list)

        self.load_priorities()

        self.add_button = QPushButton("Dodaj priorytet")
        self.add_button.clicked.connect(self.add_priority)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
    def load_priorities(self):
        self.priority_list.clear()
        priorities = session.query(Priority).all()
        for priority in priorities:
            self.priority_list.addItem(str(priority.name))

    def add_priority(self):
        priority, ok = QInputDialog.getText(self, 'Dodaj priorytet', 'Wpisz nazwę priorytetu:')
        if ok and priority:
            new_priority = Priority(name=priority)
            session.add(new_priority)
            session.commit()
            self.load_priorities()