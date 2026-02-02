from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from database.db import get_connection
from ui.faculty_form import COMMON_FORM_STYLE


class ClassForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        card = QFrame()
        card.setObjectName("card")
        cl = QVBoxLayout()

        title = QLabel("Add Class")
        title.setObjectName("title")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Class Name (e.g. TY-CS-A)")

        self.count = QLineEdit()
        self.count.setPlaceholderText("Student Count")

        self.sem = QLineEdit()
        self.sem.setPlaceholderText("Semester")

        btn = QPushButton("Save Class")
        btn.clicked.connect(self.save)

        for w in [title, self.name, self.count, self.sem, btn]:
            cl.addWidget(w)

        card.setLayout(cl)
        layout.addWidget(card)
        self.setLayout(layout)
        self.setStyleSheet(COMMON_FORM_STYLE)

    def save(self):
        if not self.name.text() or not self.count.text() or not self.sem.text():
            QMessageBox.warning(self, "Error", "All fields required")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO class (name, student_count, semester) VALUES (?, ?, ?)",
            (self.name.text(), int(self.count.text()), self.sem.text())
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Class added")
        self.name.clear()
        self.count.clear()
        self.sem.clear()
