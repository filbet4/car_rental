
INSERT INTO pracownicy (imie, nazwisko, login, haslo, rola_admin)
VALUES
  ('Adam', 'Administrator', 'admin',
   '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
   'ADMIN')

ON CONFLICT (login) DO NOTHING;

INSERT INTO klienci (imie, nazwisko, nr_prawa_jazdy, telefon)
VALUES
  ('Piotr', 'Nowak', 'PL1234567890', '504-123-456'),
  ('Anna',  'Kowalski', 'PL0987654321', '505-234-567'),
  ('Jan',   'Lewandowski', 'PL1122334455', '506-345-678'),
  ('Magdalena', 'Szymańska', 'PL5566778899', '507-456-789')
ON CONFLICT (nr_prawa_jazdy) DO NOTHING;

INSERT INTO samochody (marka, model, nr_rejestracyjny, status_techniczny)
VALUES
  ('Toyota', 'Corolla', 'KR12345', 'Sprawny'),
  ('BMW', 'X5', 'WA54321', 'Sprawny'),
  ('Audi', 'A4', 'GD98765', 'W serwisie'),
  ('Skoda', 'Octavia', 'PO11223', 'Sprawny'),
  ('Ford', 'Focus', 'LU77889', 'Sprawny')
ON CONFLICT (nr_rejestracyjny) DO NOTHING;

INSERT INTO wyposazenie (nazwa)
VALUES
  ('GPS'),
  ('Klimatyzacja'),
  ('Bagażnik dachowy'),
  ('Ładowarka USB'),
  ('Ubezpieczenie premium')
ON CONFLICT DO NOTHING;

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 1, 1
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 1 AND id_wyposazenia = 1);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 1, 4
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 1 AND id_wyposazenia = 4);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 2, 1
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 2 AND id_wyposazenia = 1);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 2, 5
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 2 AND id_wyposazenia = 5);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 3, 2
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 3 AND id_wyposazenia = 2);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 4, 3
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 4 AND id_wyposazenia = 3);

INSERT INTO samochod_wyposazenie (id_samochodu, id_wyposazenia)
SELECT 5, 4
WHERE NOT EXISTS (SELECT 1 FROM samochod_wyposazenie WHERE id_samochodu = 5 AND id_wyposazenia = 4);


INSERT INTO wypozyczenia (id_klienta, id_samochodu, data_wypozyczenia, data_zwrotu, koszt_calkowity, status_wypozyczenia)
SELECT
  (SELECT id_klienta FROM klienci WHERE nr_prawa_jazdy='PL1234567890'),
  1,
  '2024-01-10',
  '2024-01-17',
  350.00,
  'Zakończone'
WHERE NOT EXISTS (
  SELECT 1 FROM wypozyczenia
  WHERE id_samochodu=1 AND data_wypozyczenia='2024-01-10'
);

INSERT INTO wypozyczenia (id_klienta, id_samochodu, data_wypozyczenia, data_zwrotu, koszt_calkowity, status_wypozyczenia)
SELECT
  (SELECT id_klienta FROM klienci WHERE nr_prawa_jazdy='PL0987654321'),
  2,
  '2024-01-12',
  '2024-01-19',
  280.00,
  'Zakończone'
WHERE NOT EXISTS (
  SELECT 1 FROM wypozyczenia
  WHERE id_samochodu=2 AND data_wypozyczenia='2024-01-12'
);

INSERT INTO wypozyczenia (id_klienta, id_samochodu, data_wypozyczenia, data_zwrotu, koszt_calkowity, status_wypozyczenia)
SELECT
  (SELECT id_klienta FROM klienci WHERE nr_prawa_jazdy='PL1122334455'),
  3,
  '2024-01-05',
  '2024-01-08',
  200.00,
  'Zakończone'
WHERE NOT EXISTS (
  SELECT 1 FROM wypozyczenia
  WHERE id_samochodu=3 AND data_wypozyczenia='2024-01-05'
);

INSERT INTO wypozyczenia (id_klienta, id_samochodu, data_wypozyczenia, data_zwrotu, koszt_calkowity, status_wypozyczenia)
SELECT
  (SELECT id_klienta FROM klienci WHERE nr_prawa_jazdy='PL5566778899'),
  4,
  '2024-01-14',
  '2024-01-21',
  420.00,
  'Zakończone'
WHERE NOT EXISTS (
  SELECT 1 FROM wypozyczenia
  WHERE id_samochodu=4 AND data_wypozyczenia='2024-01-14'
);

INSERT INTO wypozyczenia (id_klienta, id_samochodu, data_wypozyczenia, data_zwrotu, koszt_calkowity, status_wypozyczenia)
SELECT
  (SELECT id_klienta FROM klienci WHERE nr_prawa_jazdy='PL1234567890'),
  5,
  '2023-12-20',
  '2023-12-27',
  450.00,
  'Zakończone'
WHERE NOT EXISTS (
  SELECT 1 FROM wypozyczenia
  WHERE id_samochodu=5 AND data_wypozyczenia='2023-12-20'
);


INSERT INTO protokoly_stanu (id_wypozyczenia, przebieg_start, przebieg_koniec, uwagi_o_szkodach)
SELECT w.id_wypozyczenia, 120000, 120450, 'Brak szkód'
FROM wypozyczenia w
WHERE NOT EXISTS (
  SELECT 1 FROM protokoly_stanu p WHERE p.id_wypozyczenia = w.id_wypozyczenia
)
ORDER BY w.id_wypozyczenia
LIMIT 1;

SELECT 'Dane testowe załadowane' as status;

