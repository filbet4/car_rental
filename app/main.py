import sys
from PyQt6.QtWidgets import QApplication, QDialog
from app.login import LoginWindow
from app.okna import MainWindow


def main():
    app = QApplication(sys.argv)

    while True:
        login_win = LoginWindow()
        result = login_win.exec()

        if result != QDialog.DialogCode.Accepted:
            break

        user = login_win.get_user()

        main_win = MainWindow(user)
        main_win.show()

        app.exec()


    sys.exit(0)


if __name__ == "__main__":
    main()
