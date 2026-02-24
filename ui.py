from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from database import Database


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.is_loading = False
        self.pending_toggles = {}

        self.flush_timer = QTimer(self)
        self.flush_timer.setSingleShot(True)
        self.flush_timer.setInterval(120)
        self.flush_timer.timeout.connect(self.flush_pending_toggles)

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
        self.list_widget.itemChanged.connect(self.toggle_task)

        self.load_tasks()

    def load_tasks(self):
        self.is_loading = True
        self.list_widget.clear()
        for task_id, title, done in self.db.get_tasks():
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, task_id)
            if done:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)
        self.is_loading = False

    def add_task(self):
        title = self.input.text()
        if title:
            self.db.add_task(title)
            self.input.clear()
            self.load_tasks()

    def toggle_task(self, item):
        if self.is_loading:
            return
        task_id = item.data(Qt.UserRole)
        done = 1 if item.checkState() == Qt.Checked else 0
        self.pending_toggles[task_id] = done
        self.flush_timer.start()

    def flush_pending_toggles(self):
        if not self.pending_toggles:
            return
        updates = list(self.pending_toggles.items())
        self.pending_toggles.clear()
        self.db.toggle_tasks_batch(updates)

    def delete_task(self):
        item = self.list_widget.currentItem()
        if item is None:
            return
        task_id = item.data(Qt.UserRole)
        self.pending_toggles.pop(task_id, None)
        self.db.delete_task(task_id)
        self.load_tasks()

    def closeEvent(self, event):
        self.flush_pending_toggles()
        super().closeEvent(event)
