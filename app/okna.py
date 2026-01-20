from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QDialog, QLineEdit, QFormLayout,
    QLabel, QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
import app.db as db


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(
            f"Wypożyczalnia – {user['imie']} {user['nazwisko']} ({user['rola']})"
        )
        self.resize(1200, 750)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_klienci = QWidget()
        self.tab_samochody = QWidget()
        self.tab_wypozyczenia = QWidget()

        self.tabs.addTab(self.tab_klienci, "Klienci")
        self.tabs.addTab(self.tab_samochody, "Samochody")
        self.tabs.addTab(self.tab_wypozyczenia, "Wypożyczenia")

        self.init_klienci_tab()
        self.init_samochody_tab()
        self.init_wypozyczenia_tab()

        self.load_klienci()
        self.load_samochody()
        self.load_wypozyczenia()

        btn_logout = QPushButton("Wyloguj")
        btn_logout.clicked.connect(self.close)
        self.statusBar().addPermanentWidget(btn_logout)


    def init_klienci_tab(self):
        layout = QVBoxLayout()
        self.table_kl = QTableWidget()
        self.table_kl.setColumnCount(5)
        self.table_kl.setHorizontalHeaderLabels(
            ["ID", "Imię", "Nazwisko", "Prawo jazdy", "Telefon"]
        )
        layout.addWidget(self.table_kl)

        btns = QHBoxLayout()
        b_add = QPushButton("Dodaj")
        b_edit = QPushButton("Edytuj")
        b_del = QPushButton("Usuń")

        b_add.clicked.connect(self.add_klient_dialog)
        b_edit.clicked.connect(self.edit_klient_dialog)
        b_del.clicked.connect(self.delete_klient)

        btns.addWidget(b_add)
        btns.addWidget(b_edit)
        btns.addWidget(b_del)

        layout.addLayout(btns)
        self.tab_klienci.setLayout(layout)

    def load_klienci(self):
        rows = db.get_all_klienci()
        self.table_kl.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                item = QTableWidgetItem("" if v is None else str(v))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_kl.setItem(r, c, item)

    def add_klient_dialog(self):
        dlg = QDialog(self)
        form = QFormLayout()

        im = QLineEdit()
        na = QLineEdit()
        pj = QLineEdit()
        tel = QLineEdit()

        form.addRow("Imię:", im)
        form.addRow("Nazwisko:", na)
        form.addRow("Nr prawa jazdy:", pj)
        form.addRow("Telefon:", tel)

        btn = QPushButton("Zapisz")
        btn.clicked.connect(lambda: self.save_add_klient(dlg, im, na, pj, tel))
        form.addWidget(btn)

        dlg.setLayout(form)
        dlg.exec()

    def save_add_klient(self, dlg, im, na, pj, tel):
        if db.add_klient(im.text(), na.text(), pj.text(), tel.text()):
            dlg.accept()
            self.load_klienci()
        else:
            QMessageBox.warning(self, "Błąd", "Nie udało się dodać klienta.")

    def edit_klient_dialog(self):
        r = self.table_kl.currentRow()
        if r < 0:
            return
        
        idk = int(self.table_kl.item(r, 0).text())
        im0 = self.table_kl.item(r, 1).text()
        na0 = self.table_kl.item(r, 2).text()
        pj0 = self.table_kl.item(r, 3).text()
        tel0 = self.table_kl.item(r, 4).text()

        dlg = QDialog(self)
        form = QFormLayout()

        im = QLineEdit(im0)
        na = QLineEdit(na0)
        pj = QLineEdit(pj0)
        tel = QLineEdit(tel0)

        form.addRow("Imię:", im)
        form.addRow("Nazwisko:", na)
        form.add.addRow("Prawo jazdy:", pj)
        form.addRow("Telefon:", tel)

        btn = QPushButton("Zapisz zmiany")
        btn.clicked.connect(lambda: self.save_edit_klient(
            dlg, idk, im, na, pj, tel
        ))
        form.addWidget(btn)

        dlg.setLayout(form)
        dlg.exec()

    def save_edit_klient(self, dlg, idk, im, na, pj, tel):
        if db.update_klient(idk, im.text(), na.text(), pj.text(), tel.text()):
            dlg.accept()
            self.load_klienci()
        else:
            QMessageBox.warning(self, "Błąd", "Nie udało się edytować klienta.")

    def delete_klient(self):
        r = self.table_kl.currentRow()
        if r < 0:
            return
        
        idk = int(self.table_kl.item(r, 0).text())

        if not db.delete_klient(idk):
            QMessageBox.warning(self, "Błąd",
                                "Nie można usunąć klienta – posiada wypożyczenia.")
            return
        
        self.load_klienci()


    def init_samochody_tab(self):
        layout = QVBoxLayout()
        self.table_sam = QTableWidget()
        self.table_sam.setColumnCount(5)
        self.table_sam.setHorizontalHeaderLabels(
            ["ID", "Marka", "Model", "Nr rej.", "Status"]
        )
        layout.addWidget(self.table_sam)

        btns = QHBoxLayout()
        b_add = QPushButton("Dodaj")
        b_edit = QPushButton("Edytuj")
        b_del = QPushButton("Usuń")

        b_add.clicked.connect(self.add_samochod_dialog)
        b_edit.clicked.connect(self.edit_samochod_dialog)
        b_del.clicked.connect(self.delete_samochod)

        btns.addWidget(b_add)
        btns.addWidget(b_edit)
        btns.addWidget(b_del)

        layout.addLayout(btns)
        self.tab_samochody.setLayout(layout)

    def load_samochody(self):
        rows = db.get_all_samochody()
        self.table_sam.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                item = QTableWidgetItem("" if v is None else str(v))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_sam.setItem(r, c, item)

    def add_samochod_dialog(self):
        dlg = QDialog(self)
        form = QFormLayout()

        marka = QLineEdit()
        model = QLineEdit()
        nr = QLineEdit()
        status = QComboBox()
        status.addItems(["Sprawny", "W serwisie", "Niedostępny"])

        form.addRow("Marka:", marka)
        form.addRow("Model:", model)
        form.addRow("Nr rejestracyjny:", nr)
        form.addRow("Status:", status)

        btn = QPushButton("Zapisz")
        btn.clicked.connect(
            lambda: self.save_add_samochod(dlg, marka, model, nr, status)
        )
        form.addWidget(btn)

        dlg.setLayout(form)
        dlg.exec()

    def save_add_samochod(self, dlg, marka, model, nr, status):
        if db.add_samochod(
            marka.text(), model.text(), nr.text(), status.currentText()
        ):
            dlg.accept()
            self.load_samochody()
        else:
            QMessageBox.warning(self, "Błąd", "Nie udało się dodać samochodu.")

    def edit_samochod_dialog(self):
        r = self.table_sam.currentRow()
        if r < 0:
            return

        ids = int(self.table_sam.item(r, 0).text())
        m0 = self.table_sam.item(r, 1).text()
        mo0 = self.table_sam.item(r, 2).text()
        nr0 = self.table_sam.item(r, 3).text()
        st0 = self.table_sam.item(r, 4).text()

        dlg = QDialog(self)
        form = QFormLayout()

        marka = QLineEdit(m0)
        model = QLineEdit(mo0)
        nr = QLineEdit(nr0)
        status = QComboBox()
        status.addItems(["Sprawny", "W serwisie", "Niedostępny"])
        status.setCurrentText(st0)

        form.addRow("Marka:", marka)
        form.addRow("Model:", model)
        form.addRow("Nr rej:", nr)
        form.addRow("Status:", status)

        btn = QPushButton("Zapisz zmiany")
        btn.clicked.connect(lambda: self.save_edit_samochod(
            dlg, ids, marka, model, nr, status
        ))
        form.addWidget(btn)

        dlg.setLayout(form)
        dlg.exec()

    def save_edit_samochod(self, dlg, ids, marka, model, nr, status):
        if db.update_samochod(
            ids, marka.text(), model.text(), nr.text(), status.currentText()
        ):
            dlg.accept()
            self.load_samochody()
        else:
            QMessageBox.warning(self, "Błąd", "Nie udało się edytować samochodu.")

    def delete_samochod(self):
        r = self.table_sam.currentRow()
        if r < 0:
            return
        
        ids = int(self.table_sam.item(r, 0).text())

        if not db.delete_samochod(ids):
            QMessageBox.warning(self, "Błąd",
                                "Nie można usunąć samochodu – posiada wypożyczenia.")
            return
        
        self.load_samochody()


    def init_wypozyczenia_tab(self):
        layout = QVBoxLayout()

        self.table_w = QTableWidget()
        self.table_w.setColumnCount(9)
        self.table_w.setHorizontalHeaderLabels([
            "ID", "Imię klienta", "Nazwisko klienta",
            "Marka", "Model",
            "Data wyp.", "Data zwrotu", "Koszt", "Status"
        ])
        layout.addWidget(self.table_w)

        btns = QHBoxLayout()

        b_add = QPushButton("Nowe wypożyczenie")
        b_return = QPushButton("Zakończ (zwrot)")
        b_add.clicked.connect(self.add_wypozyczenie_dialog)
        b_return.clicked.connect(self.return_wypozyczenie)

        btns.addWidget(b_add)
        btns.addWidget(b_return)

        layout.addLayout(btns)
        self.tab_wypozyczenia.setLayout(layout)

    def load_wypozyczenia(self):
        rows = db.get_all_wypozyczenia()
        self.table_w.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                item = QTableWidgetItem("" if v is None else str(v))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_w.setItem(r, c, item)

    def add_wypozyczenie_dialog(self):
        dlg = QDialog(self)
        form = QFormLayout()

        # LISTA KLIENTÓW
        kl = db.get_all_klienci()
        cb_kl = QComboBox()
        for k in kl:
            cb_kl.addItem(f"{k[1]} {k[2]} ({k[3]})", k[0])

        # LISTA SAMOCHODÓW
        sam = db.get_all_samochody()
        cb_sam = QComboBox()
        for s in sam:
            cb_sam.addItem(f"{s[1]} {s[2]} – {s[3]}", s[0])

        d_w = QDateEdit()
        d_w.setDate(QDate.currentDate())
        d_w.setCalendarPopup(True)

        d_z = QDateEdit()
        d_z.setDate(QDate.currentDate().addDays(1))
        d_z.setCalendarPopup(True)

        koszt = QLineEdit()

        status = QComboBox()
        status.addItems(["W toku", "Zakończone", "Anulowane"])

        form.addRow("Klient:", cb_kl)
        form.addRow("Samochód:", cb_sam)
        form.addRow("Data wyp.:", d_w)
        form.addRow("Data zwrotu:", d_z)
        form.addRow("Koszt:", koszt)
        form.addRow("Status:", status)

        btn = QPushButton("Dodaj wypożyczenie")
        btn.clicked.connect(lambda: self.save_add_wypozyczenie(
            dlg, cb_kl, cb_sam, d_w, d_z, koszt, status
        ))
        form.addWidget(btn)

        dlg.setLayout(form)
        dlg.exec()

    def save_add_wypozyczenie(self, dlg, cb_kl, cb_sam, d_w, d_z, koszt, status):
        idk = cb_kl.currentData()
        ids = cb_sam.currentData()

        if not db.add_wypozyczenie(
            idk,
            ids,
            d_w.date().toString("yyyy-MM-dd"),
            d_z.date().toString("yyyy-MM-dd"),
            koszt.text(),
            status.currentText()
        ):
            QMessageBox.warning(self, "Błąd", "Nie udało się dodać wypożyczenia.")
            return

        dlg.accept()
        self.load_wypozyczenia()

    def return_wypozyczenie(self):
        r = self.table_w.currentRow()
        if r < 0:
            return

        idw = int(self.table_w.item(r, 0).text())

        if not db.return_wypozyczenie(idw):
            QMessageBox.warning(self, "Błąd", "Nie udało się zakończyć wypożyczenia.")
            return

        QMessageBox.information(self, "OK", "Wypożyczenie zakończone.")
        self.load_wypozyczenia()
