from custom_websocket import CustomWebSocketServer
import threading
import sys
from logger import log
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox
)
from PyQt6.QtCore import QObject, pyqtSignal

from UsersDatabase import create_users_tables, add_user
from MarksDataBase import create_marks_tables, reset_markers
from events.LoginNetworkEvent import LoginNetworkEvent
from events.MapMarksEvent import MapMarksEvent


class BridgeSignals(QObject):
    clients_changed = pyqtSignal()

bridge = BridgeSignals()

connected_clients = set()  # tuples: (websocket, client_id, room_id)

network_events = [
    LoginNetworkEvent,
    MapMarksEvent,
]



def handle_message(client, message: str):
    if message == "user_go_login":
        for ws, cid, rid in list(connected_clients):
            if ws == client:
                connected_clients.remove((ws, cid, rid))
                connected_clients.add((ws, None, None))
                bridge.clients_changed.emit()
        return

    for event in network_events:
        if event.detect(message):
            event.handle(client, message, connected_clients)
            bridge.clients_changed.emit()
            return

    client.send("Unknown command")


def handle_client(websocket):

    client = str(websocket.raw_socket.getpeername())
    log("SYSTEM", client, "CONNECTED")

    connected_clients.add((websocket, None, None))
    bridge.clients_changed.emit()

    try:
        while True:
            message = websocket.receive()
            if message is None:
                break
            handle_message(websocket, message)
    except Exception as e:
        pass
    finally:
        log("SYSTEM", client, "DISCONNECTED")

        for ws, cid, rid in list(connected_clients):
            if ws == websocket:
                connected_clients.remove((ws, cid, rid))
                bridge.clients_changed.emit()


def run_server():

    log("SYSTEM", "SERVER", "STARTED")

    create_users_tables()
    create_marks_tables()
    reset_markers()
    CustomWebSocketServer("0.0.0.0", 3000, handle_client).start_websocket()

    log("SYSTEM", "SERVER", "STOPPED")

class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server")
        self.setMinimumSize(400, 500)
        self._build_ui()
        bridge.clients_changed.connect(self.refresh_clients)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # --- Add User section ---
        user_group = QGroupBox("Add User")
        user_layout = QVBoxLayout(user_group)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        user_layout.addWidget(QLabel("Username:"))
        user_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        user_layout.addWidget(QLabel("Password:"))
        user_layout.addWidget(self.password_input)

        self.feedback_label = QLabel("")
        user_layout.addWidget(self.feedback_label)

        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.handle_add_user)
        user_layout.addWidget(add_btn)

        layout.addWidget(user_group)

        # --- Connected clients section ---
        clients_group = QGroupBox("Connected Clients")
        clients_layout = QVBoxLayout(clients_group)

        self.clients_text = QTextEdit()
        self.clients_text.setReadOnly(True)
        clients_layout.addWidget(self.clients_text)

        layout.addWidget(clients_group)

    def handle_add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.feedback_label.setText("Please fill in both fields.")
            return

        add_user(username, password)
        self.feedback_label.setText(f"User '{username}' added.")
        self.username_input.clear()
        self.password_input.clear()

    def refresh_clients(self):
        rooms = {}
        pending = 0

        for ws, cid, rid in connected_clients:
            if rid is None:
                pending += 1
            else:
                rooms.setdefault(rid, []).append(cid)

        lines = []

        if pending > 0:
            lines.append(f"Not logged in: {pending} client(s)")

        for rid in sorted(rooms.keys()):
            ids = rooms[rid]
            lines.append(f"\nRoom {rid} ({len(ids)} connected):")
            for cid in ids:
                lines.append(f"  - user id: {cid}")

        if not lines:
            lines.append("No clients connected.")

        self.clients_text.setText("\n".join(lines))


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec())