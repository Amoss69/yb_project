import asyncio
import websockets
import threading
import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QFont

from UsersDatabase import create_users_tables, add_user
from MarksDataBase import create_marks_tables, reset_markers
from events.LoginNetworkEvent import LoginNetworkEvent
from events.MapMarksEvent import MapMarksEvent


# ─────────────────────────────────────────────
#  Signal bridge: asyncio thread → Qt GUI
# ─────────────────────────────────────────────
class BridgeSignals(QObject):
    clients_changed = pyqtSignal()

bridge = BridgeSignals()


# ─────────────────────────────────────────────
#  WebSocket server logic
# ─────────────────────────────────────────────
connected_clients = set()  # tuples: (websocket, client_id, room_id)

network_events = [
    LoginNetworkEvent,
    MapMarksEvent,
]


async def handle_message(client, message: str):
    if message == "user_go_login":
        for ws, cid, rid in list(connected_clients):
            if ws == client:
                connected_clients.remove((ws, cid, rid))
                connected_clients.add((ws, None, None))
                bridge.clients_changed.emit()
        return

    for event in network_events:
        if event.detect(message):
            await event.handle(client, message, connected_clients)
            bridge.clients_changed.emit()
            return

    await client.send("Unknown command")


async def handle_client(websocket):
    connected_clients.add((websocket, None, None))
    bridge.clients_changed.emit()

    try:
        async for message in websocket:
            await handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        for ws, cid, rid in list(connected_clients):
            if ws == websocket:
                connected_clients.remove((ws, cid, rid))
                bridge.clients_changed.emit()


async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 3000)
    await server.wait_closed()


def run_server():
    create_users_tables()
    create_marks_tables()
    reset_markers()
    asyncio.run(start_server())


# ─────────────────────────────────────────────
#  Styles
# ─────────────────────────────────────────────
DARK_BG   = "#0d0d0d"
PANEL_BG  = "#141414"
BORDER    = "#2a2a2a"
ACCENT    = "#00e5a0"
TEXT      = "#e8e8e8"
TEXT_DIM  = "#555555"
ERROR     = "#ff4f4f"

STYLE = f"""
QWidget {{
    background-color: {DARK_BG};
    color: {TEXT};
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}}
QFrame#panel {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}
QLabel#section_title {{
    color: {ACCENT};
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: bold;
}}
QLineEdit {{
    background-color: {DARK_BG};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 8px 12px;
    color: {TEXT};
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}}
QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
QPushButton#add_btn {{
    background-color: {ACCENT};
    color: #000000;
    border: none;
    border-radius: 5px;
    padding: 9px 0px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}}
QPushButton#add_btn:hover {{ background-color: #00ffb3; }}
QPushButton#add_btn:pressed {{ background-color: #00a86b; }}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {DARK_BG};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: #333;
    border-radius: 3px;
}}
"""


# ─────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────
class ServerDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Dashboard")
        self.setMinimumSize(500, 640)
        self.setStyleSheet(STYLE)
        self._build_ui()
        bridge.clients_changed.connect(self.refresh_clients)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # Header
        title = QLabel("SERVER DASHBOARD")
        title.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT}; letter-spacing: 4px;")
        root.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        root.addWidget(sep)

        # ── Add User panel ──
        user_panel = QFrame()
        user_panel.setObjectName("panel")
        ul = QVBoxLayout(user_panel)
        ul.setContentsMargins(18, 16, 18, 18)
        ul.setSpacing(10)

        ul.addWidget(self._section_label("ADD USER"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("username")
        ul.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        ul.addWidget(self.password_input)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet(f"font-size: 11px; color: {ACCENT};")
        ul.addWidget(self.feedback_label)

        add_btn = QPushButton("+ CREATE USER")
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.handle_add_user)
        ul.addWidget(add_btn)

        root.addWidget(user_panel)

        # ── Clients panel ──
        clients_panel = QFrame()
        clients_panel.setObjectName("panel")
        clients_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cl = QVBoxLayout(clients_panel)
        cl.setContentsMargins(18, 16, 18, 18)
        cl.setSpacing(10)

        cl.addWidget(self._section_label("CONNECTED CLIENTS"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.clients_container = QWidget()
        self.clients_container.setStyleSheet("background: transparent;")
        self.clients_layout = QVBoxLayout(self.clients_container)
        self.clients_layout.setContentsMargins(0, 0, 0, 0)
        self.clients_layout.setSpacing(12)
        self.clients_layout.addStretch()
        scroll.setWidget(self.clients_container)
        cl.addWidget(scroll)

        root.addWidget(clients_panel)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("section_title")
        return lbl

    def handle_add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            self.feedback_label.setStyleSheet(f"font-size: 11px; color: {ERROR};")
            self.feedback_label.setText("✗  Both fields are required.")
            return
        add_user(username, password)
        self.feedback_label.setStyleSheet(f"font-size: 11px; color: {ACCENT};")
        self.feedback_label.setText(f"✓  User '{username}' created.")
        self.username_input.clear()
        self.password_input.clear()

    def refresh_clients(self):
        # Clear all widgets except trailing stretch
        while self.clients_layout.count() > 1:
            item = self.clients_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Group active clients by room
        rooms = {}
        pending_count = 0
        for ws, cid, rid in connected_clients:
            if rid is None:
                pending_count += 1
            else:
                rooms.setdefault(rid, []).append(cid)

        # Pending block
        idx = 0
        if pending_count:
            self.clients_layout.insertWidget(idx, self._room_block("Pending", ["unknown"] * pending_count))
            idx += 1

        # Room blocks
        for rid in sorted(rooms.keys()):
            self.clients_layout.insertWidget(idx, self._room_block(f"Room {rid}", rooms[rid]))
            idx += 1

        # Empty state
        if not pending_count and not rooms:
            empty = QLabel("No clients connected.")
            empty.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px;")
            self.clients_layout.insertWidget(0, empty)

    def _room_block(self, title, client_ids):
        block = QFrame()
        block.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_BG};
                border: 1px solid {BORDER};
                border-radius: 6px;
            }}
        """)
        bl = QVBoxLayout(block)
        bl.setContentsMargins(12, 10, 12, 10)
        bl.setSpacing(6)

        room_lbl = QLabel(title)
        room_lbl.setStyleSheet(f"color: {ACCENT}; font-size: 12px; font-weight: bold;")
        bl.addWidget(room_lbl)

        for cid in client_ids:
            row = QHBoxLayout()
            dot = QLabel("●")
            dot.setFixedWidth(16)
            dot.setStyleSheet(f"color: {ACCENT}; font-size: 10px;")
            name = QLabel(f"id: {cid}" if cid != "unknown" else "unknown")
            row.addWidget(dot)
            row.addWidget(name)
            row.addStretch()
            bl.addLayout(row)

        return block


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    app = QApplication(sys.argv)
    window = ServerDashboard()
    window.show()
    sys.exit(app.exec())