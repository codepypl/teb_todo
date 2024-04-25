from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QLineEdit

from db import session, Category


class CategoryManagerApp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zarządzanie Kategoriami")
        self.setGeometry(300, 200, 500, 200)

        layout = QVBoxLayout()

        self.category_list = QListWidget()
        layout.addWidget(self.category_list)

        self.load_categories()

        self.add_button = QPushButton("Dodaj kategorię")
        self.add_button.clicked.connect(self.add_category)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edytuj kategorię")
        self.edit_button.clicked.connect(self.edit_category)
        layout.addWidget(self.edit_button)

        self.remove_button = QPushButton("Usuń kategorię")
        self.remove_button.clicked.connect(self.remove_category)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def load_categories(self):
        self.category_list.clear()
        categories = session.query(Category).all()
        for category in categories:
            self.category_list.addItem(str(category.name))

    def add_category(self):
        category, ok = QInputDialog.getText(self, 'Dodaj kategorię', 'Wpisz nazwę kategorii:')
        if ok and category:
            new_category = Category(name=category)
            session.add(new_category)
            session.commit()
            self.load_categories()

    def edit_category(self):
        selected_item = self.category_list.currentItem()
        if selected_item:
            category_name = selected_item.text()
            new_category_name, ok = QInputDialog.getText(self, 'Edytuj kategorię', 'Wpisz nową nazwę kategorii:',
                                                         QLineEdit.Normal, category_name)
            if ok and new_category_name:
                category = session.query(Category).filter_by(name=category_name).first()
                if category:
                    category.name = new_category_name
                    session.commit()
                    self.load_categories()

    def remove_category(self):
        selected_item = self.category_list.currentItem()
        if selected_item:
            category_name = selected_item.text()
            category = session.query(Category).filter_by(name=category_name).first()
            if category:
                session.delete(category)
                session.commit()
                self.load_categories()