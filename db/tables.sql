
CREATE TABLE IF NOT EXISTS pracownicy (
    id_pracownika SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    haslo VARCHAR(255) NOT NULL,  
    rola_admin VARCHAR(50)        
);

CREATE TABLE IF NOT EXISTS klienci (
    id_klienta SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    nr_prawa_jazdy VARCHAR(20) UNIQUE NOT NULL,
    telefon VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS wyposazenie (
    id_wyposazenia SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS samochody (
    id_samochodu SERIAL PRIMARY KEY,
    marka VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    nr_rejestracyjny VARCHAR(20) UNIQUE NOT NULL,
    status_techniczny VARCHAR(50) NOT NULL  
);

CREATE TABLE IF NOT EXISTS samochod_wyposazenie (
    id_samochodu INTEGER NOT NULL,
    id_wyposazenia INTEGER NOT NULL,
    PRIMARY KEY (id_samochodu, id_wyposazenia),
    FOREIGN KEY (id_samochodu) REFERENCES samochody(id_samochodu) ON DELETE CASCADE,
    FOREIGN KEY (id_wyposazenia) REFERENCES wyposazenie(id_wyposazenia) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wypozyczenia (
    id_wypozyczenia SERIAL PRIMARY KEY,
    id_klienta INTEGER NOT NULL,
    id_samochodu INTEGER NOT NULL,
    data_wypozyczenia DATE NOT NULL,
    data_zwrotu DATE NOT NULL,
    koszt_calkowity NUMERIC(10, 2) NOT NULL,
    status_wypozyczenia VARCHAR(50) NOT NULL, 
    data_rejestracji TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta),
    FOREIGN KEY (id_samochodu) REFERENCES samochody(id_samochodu),
    CHECK (data_zwrotu >= data_wypozyczenia)
);

CREATE TABLE IF NOT EXISTS protokoly_stanu (
    id_protokolu SERIAL PRIMARY KEY,
    id_wypozyczenia INTEGER NOT NULL,
    przebieg_start INTEGER NOT NULL,
    przebieg_koniec INTEGER,
    uwagi_o_szkodach TEXT,
    FOREIGN KEY (id_wypozyczenia) REFERENCES wypozyczenia(id_wypozyczenia)
);
