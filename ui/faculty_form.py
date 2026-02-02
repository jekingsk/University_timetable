from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from database.db import get_connection

COMMON_FORM_STYLE = """
QWidget {
    background-color: #f7f9fc;
    font-family: Segoe UI;
}

QFrame#card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
}

QLabel#title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

QLineEdit, QComboBox {
    height: 36px;
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #cfd6e4;
}

QPushButton {
    margin-top: 12px;
    height: 38px;
    background-color: #2d89ef;
    color: white;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1b5fbf;
}
"""

class FacultyForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()

        title = QLabel("Add Faculty")
        title.setObjectName("title")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Faculty Name")

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText("Max Weekly Hours")

        btn = QPushButton("Save Faculty")
        btn.clicked.connect(self.save_faculty)

        for w in [title, self.name_input, self.hours_input, btn]:
            card_layout.addWidget(w)

        card.setLayout(card_layout)
        layout.addWidget(card)
        self.setLayout(layout)

        self.setStyleSheet(self.style())

    def save_faculty(self):
        if not self.name_input.text() or not self.hours_input.text():
            QMessageBox.warning(self, "Error", "All fields required")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO faculty (name, max_hours) VALUES (?, ?)",
            (self.name_input.text(), int(self.hours_input.text()))
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Saved", "Faculty added")
        self.name_input.clear()
        self.hours_input.clear()

    def style(self):
        return COMMON_FORM_STYLE
