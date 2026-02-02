from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from database.db import get_connection
from ui.faculty_form import COMMON_FORM_STYLE


class RoomForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        card = QFrame()
        card.setObjectName("card")
        cl = QVBoxLayout()

        title = QLabel("Add Room")
        title.setObjectName("title")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Room Name")

        self.type = QLineEdit()
        self.type.setPlaceholderText("Type (Classroom / Lab)")

        self.cap = QLineEdit()
        self.cap.setPlaceholderText("Capacity")

        btn = QPushButton("Save Room")
        btn.clicked.connect(self.save)

        for w in [title, self.name, self.type, self.cap, btn]:
            cl.addWidget(w)

        card.setLayout(cl)
        layout.addWidget(card)
        self.setLayout(layout)
        self.setStyleSheet(COMMON_FORM_STYLE)

    def save(self):
        if not self.name.text() or not self.type.text() or not self.cap.text():
            QMessageBox.warning(self, "Error", "All fields required")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO room (name, type, capacity) VALUES (?, ?, ?)",
            (self.name.text(), self.type.text(), int(self.cap.text()))
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Room added")
        self.name.clear()
        self.type.clear()
        self.cap.clear()
