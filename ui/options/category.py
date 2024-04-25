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