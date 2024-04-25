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

        self.edit_button = QPushButton("Edytuj priorytet")
        self.edit_button.clicked.connect(self.edit_priority)
        layout.addWidget(self.edit_button)

        self.remove_button = QPushButton("Usuń priorytet")
        self.remove_button.clicked.connect(self.remove_priority)
        layout.addWidget(self.remove_button)


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

    def edit_priority(self):
        selected_item = self.priority_list.currentItem()
        if selected_item:
            priority_name = selected_item.text()
            new_priority_name, ok = QInputDialog.getText(self, 'Edytuj priorytet', 'Wpisz nową nazwę priorytetu:',
                                                         QLineEdit.Normal, priority_name)
            if ok and new_priority_name:
                priority = session.query(Priority).filter_by(name=priority_name).first()
                if priority:
                    priority.name = new_priority_name
                    session.commit()
                    self.load_priorities()

    def remove_priority(self):
        selected_item = self.priority_list.currentItem()
        if selected_item:
            priority_name = selected_item.text()
            priority = session.query(Priority).filter_by(name=priority_name).first()
            if priority:
                session.delete(priority)
                session.commit()
                self.load_priorities()