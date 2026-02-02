from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame
)
from database.db import get_connection
from ui.faculty_form import COMMON_FORM_STYLE


class SubjectForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        card = QFrame()
        card.setObjectName("card")
        cl = QVBoxLayout()

        title = QLabel("Add Subject")
        title.setObjectName("title")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Subject Name")

        self.hours = QLineEdit()
        self.hours.setPlaceholderText("Weekly Hours")

        self.faculty = QComboBox()
        self.load_faculty()

        btn = QPushButton("Save Subject")
        btn.clicked.connect(self.save)

        for w in [title, self.name, self.hours, self.faculty, btn]:
            cl.addWidget(w)

        card.setLayout(cl)
        layout.addWidget(card)
        self.setLayout(layout)
        self.setStyleSheet(COMMON_FORM_STYLE)

    def load_faculty(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM faculty")
        for i, n in cur.fetchall():
            self.faculty.addItem(n, i)
        conn.close()

    def save(self):
        if not self.name.text() or not self.hours.text():
            QMessageBox.warning(self, "Error", "All fields required")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO subject (name, faculty_id, weekly_hours) VALUES (?, ?, ?)",
            (self.name.text(), self.faculty.currentData(), int(self.hours.text()))
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Subject added")
        self.name.clear()
        self.hours.clear()
