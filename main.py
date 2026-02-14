import sys
from PySide6.QtWidgets import QApplication
from ui import TaskManager

app = QApplication(sys.argv)
window = TaskManager()
window.show()
sys.exit(app.exec())
