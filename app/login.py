from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
import app.db as db


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.user = None

        self.setWindowTitle("Logowanie")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Hasło")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Zaloguj")
        btn_login.clicked.connect(self.try_login)

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Hasło"))
        layout.addWidget(self.pass_input)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def try_login(self):
        login = self.login_input.text().strip()
        password = self.pass_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Błąd", "Wprowadź login i hasło.")
            return

        user = db.login_user(login, password)
        if not user:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowy login lub hasło.")
            return

        self.user = user
        self.accept()  

    def get_user(self):
        return self.user
