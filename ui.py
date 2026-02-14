from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from database import Database


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Task Manager")

        self.layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("New task...")

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")
        self.list_widget = QListWidget()
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_btn)
        self.buttons_layout.addWidget(self.delete_btn)

        self.layout.addWidget(self.input)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

        self.add_btn.clicked.connect(self.add_task)
        self.delete_btn.clicked.connect(self.delete_task)
        self.list_widget.itemDoubleClicked.connect(self.toggle_task)

        self.load_tasks()

    def load_tasks(self):
        self.list_widget.clear()
        for task_id, title, done in self.db.get_tasks():
            item = QListWidgetItem(title)
            item.setData(1, task_id)
            if done:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)

    def add_task(self):
        title = self.input.text()
        if title:
            self.db.add_task(title)
            self.input.clear()
            self.load_tasks()

    def toggle_task(self, item):
        task_id = item.data(1)
        done = 1 if item.checkState() == Qt.Unchecked else 0
        self.db.toggle_task(task_id, done)
        self.load_tasks()

    def delete_task(self):
        item = self.list_widget.currentItem()
        if item is None:
            return
        task_id = item.data(1)
        self.db.delete_task(task_id)
        self.load_tasks()
