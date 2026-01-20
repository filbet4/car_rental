import psycopg

DB_NAME = "car_rental"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432


def get_conn():
    return psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )





def login_user(login, password):
    """Logowanie pracownika."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_pracownika, imie, nazwisko, rola_admin
                FROM pracownicy
                WHERE login=%s AND haslo=%s
            """, (login, password))

            r = cur.fetchone()
            if not r:
                return None

            return {
                "id": r[0],
                "imie": r[1],
                "nazwisko": r[2],
                "rola": r[3]
            }



def get_all_klienci():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_klienta, imie, nazwisko, nr_prawa_jazdy, telefon
                FROM klienci
                ORDER BY id_klienta
            """)
            return cur.fetchall()


def add_klient(imie, nazwisko, nr_prawa_jazdy, telefon):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO klienci (imie, nazwisko, nr_prawa_jazdy, telefon)
                    VALUES (%s, %s, %s, %s)
                """, (imie, nazwisko, nr_prawa_jazdy, telefon))
        return True
    except Exception as e:
        print("Add klient error:", e)
        return False


def update_klient(idk, imie, nazwisko, prawo, tel):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE klienci
                    SET imie=%s,
                        nazwisko=%s,
                        nr_prawa_jazdy=%s,
                        telefon=%s
                    WHERE id_klienta=%s
                """, (imie, nazwisko, prawo, tel, idk))
        return True
    except Exception as e:
        print("Update klient error:", e)
        return False


def delete_klient(idk):
    """Usunięcie klienta — nie powiedzie się jeśli są powiązane wypożyczenia."""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM klienci WHERE id_klienta=%s", (idk,))
        return True
    except Exception as e:
        print("Delete klient error:", e)
        return False



def get_all_samochody():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_samochodu, marka, model, nr_rejestracyjny, status_techniczny
                FROM samochody
                ORDER BY id_samochodu
            """)
            return cur.fetchall()


def add_samochod(marka, model, nr_rej, status):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO samochody (marka, model, nr_rejestracyjny, status_techniczny)
                    VALUES (%s, %s, %s, %s)
                """, (marka, model, nr_rej, status))
        return True
    except Exception as e:
        print("Add samochod error:", e)
        return False


def update_samochod(ids, marka, model, nr_rej, status):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE samochody
                    SET marka=%s,
                        model=%s,
                        nr_rejestracyjny=%s,
                        status_techniczny=%s
                    WHERE id_samochodu=%s
                """, (marka, model, nr_rej, status, ids))
        return True
    except Exception as e:
        print("Update samochod error:", e)
        return False


def delete_samochod(ids):
    """Usunie tylko jeśli samochód NIE ma powiązanych wypożyczeń."""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM samochody WHERE id_samochodu=%s", (ids,))
        return True
    except Exception as e:
        print("Delete samochod error:", e)
        return False



def get_all_wypozyczenia():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT w.id_wypozyczenia, k.imie, k.nazwisko,
                       s.marka, s.model,
                       w.data_wypozyczenia, w.data_zwrotu,
                       w.koszt_calkowity, w.status_wypozyczenia
                FROM wypozyczenia w
                JOIN klienci k ON w.id_klienta = k.id_klienta
                JOIN samochody s ON w.id_samochodu = s.id_samochodu
                ORDER BY w.id_wypozyczenia DESC
            """)
            return cur.fetchall()


def add_wypozyczenie(id_klienta, id_samochodu, data_w, data_z, koszt, status):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO wypozyczenia
                    (id_klienta, id_samochodu, data_wypozyczenia,
                     data_zwrotu, koszt_calkowity, status_wypozyczenia)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_klienta, id_samochodu, data_w, data_z, koszt, status))
        return True
    except Exception as e:
        print("Add wypozyczenie error:", e)
        return False


def return_wypozyczenie(id_wyp):
    """Zwrot wypożyczenia – ustawia status 'Zakończone'."""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE wypozyczenia
                    SET status_wypozyczenia='Zakończone'
                    WHERE id_wypozyczenia=%s
                """, (id_wyp,))
        return True
    except Exception as e:
        print("Return wypozyczenie error:", e)
        return False



def get_aktywni_klienci():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Aktywni_Klienci")
            return cur.fetchall()
