from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QStackedWidget,
    QTableWidget, QTableWidgetItem, QComboBox
)
from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ui.faculty_form import FacultyForm
from ui.subject_form import SubjectForm
from ui.class_form import ClassForm
from ui.room_form import RoomForm
from datetime import datetime
from database.db import get_connection
from engine.generator import generate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DAV University – Timetable Automation System")
        self.setGeometry(80, 60, 1200, 750)
        self.run_selector = QComboBox()
        self.load_runs()


        # ================= ROOT =================
        central = QWidget()
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ================= HEADER =================
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 12, 20, 12)

        logo = QLabel()
        pix = QPixmap("assets/dav_logo.png")
        logo.setPixmap(pix.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        title = QLabel("DAV University – Timetable Automation System")
        title.setObjectName("headerTitle")

        header_layout.addWidget(logo)
        header_layout.addSpacing(12)
        header_layout.addWidget(title)
        header_layout.addStretch()

        header.setLayout(header_layout)
        root_layout.addWidget(header)

        # ================= TABS =================
        tabs = QTabWidget()

        # ======================================================
        # DATA MANAGEMENT TAB (DASHBOARD STYLE)
        # ======================================================
        data_tab = QWidget()
        data_layout = QHBoxLayout()
        data_layout.setContentsMargins(15, 15, 15, 15)

        # ---------- SIDEBAR ----------
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        btn_faculty = QPushButton("Faculty")
        btn_subject = QPushButton("Subject")
        btn_class = QPushButton("Class")
        btn_room = QPushButton("Room")

        side_buttons = [btn_faculty, btn_subject, btn_class, btn_room]

        for btn in side_buttons:
            btn.setMinimumHeight(44)
            btn.setObjectName("sideButton")
            sidebar.addWidget(btn)

        sidebar.addStretch()

        # ---------- FORM STACK ----------
        self.form_stack = QStackedWidget()

        self.faculty_form = FacultyForm()
        self.subject_form = SubjectForm()
        self.class_form = ClassForm()
        self.room_form = RoomForm()

        self.form_stack.addWidget(self.faculty_form)
        self.form_stack.addWidget(self.subject_form)
        self.form_stack.addWidget(self.class_form)
        self.form_stack.addWidget(self.room_form)

        btn_faculty.clicked.connect(lambda: self.form_stack.setCurrentWidget(self.faculty_form))
        btn_subject.clicked.connect(lambda: self.form_stack.setCurrentWidget(self.subject_form))
        btn_class.clicked.connect(lambda: self.form_stack.setCurrentWidget(self.class_form))
        btn_room.clicked.connect(lambda: self.form_stack.setCurrentWidget(self.room_form))

        # ---------- CENTERED FORM CONTAINER ----------
        form_container = QWidget()
        form_container_layout = QHBoxLayout()
        form_container_layout.setAlignment(Qt.AlignCenter)

        self.form_stack.setMaximumWidth(520)   # KEY FIX FOR FULLSCREEN ISSUE
        form_container_layout.addWidget(self.form_stack)

        form_container.setLayout(form_container_layout)

        data_layout.addLayout(sidebar, 1)
        data_layout.addWidget(form_container, 3)

        data_tab.setLayout(data_layout)

       # ================= TIMETABLE TAB =================
        timetable_tab = QWidget()
        tt_layout = QVBoxLayout()
        tt_layout.setContentsMargins(20, 20, 20, 20)

        # 1️⃣ Generate button
        btn_generate = QPushButton("Generate Timetable")
        btn_generate.setObjectName("generateButton")
        btn_generate.setMinimumHeight(46)
        btn_generate.clicked.connect(self.generate_timetable)

        # 2️⃣ Timetable version selector
        self.run_selector = QComboBox()
        self.load_runs()

        # 3️⃣ View selector
        self.view_selector = QComboBox()
        self.view_selector.addItems(["Class View", "Faculty View", "Room View"])
        self.view_selector.currentIndexChanged.connect(self.load_filter_options)

        # 4️⃣ Filter selector
        self.filter_box = QComboBox()
        self.filter_box.currentIndexChanged.connect(self.load_filtered_timetable)

        # 5️⃣ Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 6️⃣ ADD widgets to layout (AFTER creation)
        tt_layout.addWidget(btn_generate)
        tt_layout.addSpacing(10)

        tt_layout.addWidget(QLabel("Timetable Version"))
        tt_layout.addWidget(self.run_selector)

        tt_layout.addSpacing(10)
        tt_layout.addWidget(QLabel("View By"))
        tt_layout.addWidget(self.view_selector)

        tt_layout.addWidget(self.filter_box)
        tt_layout.addWidget(self.table)

        timetable_tab.setLayout(tt_layout)

        # ================= ADD TABS =================
        tabs.addTab(data_tab, "Data Management")
        tabs.addTab(timetable_tab, "Timetable")

        root_layout.addWidget(tabs)
        central.setLayout(root_layout)
        self.setCentralWidget(central)

        # ================= STYLES =================
        self.setStyleSheet("""
        QWidget {
            background-color: #f4f6fb;
            font-family: Segoe UI;
            color: #1f2937;
        }

        QWidget#header {
            background-color: #ffffff;
            border-bottom: 2px solid #e5e7eb;
        }

        QLabel#headerTitle {
            font-size: 22px;
            font-weight: bold;
            color: #1f4fd8;
        }

        QPushButton#sideButton {
            background-color: #1f4fd8;
            color: white;
            border-radius: 6px;
            font-size: 14px;
        }

        QPushButton#sideButton:hover {
            background-color: #163fa3;
        }

        QFrame#card {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
        }

        QLineEdit, QComboBox {
            height: 38px;
            padding: 6px;
            border-radius: 6px;
            border: 1px solid #d1d5db;
            background: white;
        }

        QPushButton {
            background-color: #1f4fd8;
            color: white;
            border-radius: 6px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #163fa3;
        }

        QPushButton#generateButton {
            background-color: #f4c430;
            color: #1f2937;
            font-size: 15px;
        }

        QPushButton#generateButton:hover {
            background-color: #e0b422;
        }

        QTabBar::tab {
            padding: 10px 20px;
            background: #e5e7eb;
        }

        QTabBar::tab:selected {
            background: white;
            font-weight: bold;
        }
        """)

    # ======================================================
    # TIMETABLE LOGIC (UNCHANGED)
    # ======================================================
    def generate_timetable(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, student_count FROM class")
        classes = [{"id": c[0], "student_count": c[1]} for c in cur.fetchall()]

        cur.execute("SELECT id, faculty_id, weekly_hours FROM subject")
        subjects = [{"id": s[0], "faculty_id": s[1], "weekly_hours": s[2]} for s in cur.fetchall()]

        cur.execute("SELECT id, capacity FROM room")
        rooms = [{"id": r[0], "capacity": r[1]} for r in cur.fetchall()]

        conn.close()

        timetable = generate(classes, subjects, rooms)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM timetable")

        for e in timetable:
            cur.execute("""
                INSERT INTO timetable
                (class_id, subject_id, faculty_id, room_id, day, time_slot)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (e["class_id"], e["subject_id"], e["faculty_id"], e["room_id"], e["day"], e["slot"]))

        conn.commit()
        conn.close()

    def load_filter_options(self):
        self.filter_box.clear()
        conn = get_connection()
        cur = conn.cursor()

        view = self.view_selector.currentText()
        if view == "Class View":
            cur.execute("SELECT id, name FROM class")
        elif view == "Faculty View":
            cur.execute("SELECT id, name FROM faculty")
        else:
            cur.execute("SELECT id, name FROM room")

        for i, n in cur.fetchall():
            self.filter_box.addItem(n, i)

        conn.close()

    def load_filtered_timetable(self):
        run_id = self.run_selector.currentData()
        if run_id is None:
            return
        sel = self.filter_box.currentData()
        if sel is None:
            return

        conn = get_connection()
        cur = conn.cursor()

        view = self.view_selector.currentText()
        base = """
            SELECT c.name, f.name, r.name, t.day, t.time_slot
            FROM timetable t
            JOIN class c ON t.class_id = c.id
            JOIN faculty f ON t.faculty_id = f.id
            JOIN room r ON t.room_id = r.id
        """

        if view == "Class View":
            base += " WHERE c.id = ?"
        elif view == "Faculty View":
            base += " WHERE f.id = ?"
        else:
            base += " WHERE r.id = ?"

        cur.execute(base, (sel,))
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Class", "Faculty", "Room", "Day", "Time Slot"]
        )

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))
        
        def generate_timetable(self):
            conn = get_connection()
            cur = conn.cursor()

            # Create new timetable run
            cur.execute(
                "INSERT INTO timetable_run (created_at) VALUES (?)",
                (datetime.now().strftime("%d-%m-%Y %H:%M"),)
            )
            run_id = cur.lastrowid
        def load_runs(self):
            self.run_selector.clear()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, created_at FROM timetable_run ORDER BY id DESC")

            for rid, time in cur.fetchall():
                self.run_selector.addItem(f"Run {rid} – {time}", rid)

            conn.close()
        def load_runs(self):
            self.run_selector.clear()

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT id, created_at
                FROM timetable_run
                ORDER BY id DESC
            """)

            for run_id, created_at in cur.fetchall():
                self.run_selector.addItem(
                    f"Run {run_id} – {created_at}",
                    run_id
                )

            conn.close()
