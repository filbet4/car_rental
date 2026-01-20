
CREATE OR REPLACE VIEW Aktywni_Klienci AS
SELECT
    k.id_klienta,
    k.imie,
    k.nazwisko,
    k.nr_prawa_jazdy,
    k.telefon,
    COUNT(w.id_wypozyczenia) AS liczba_wypozyczen
FROM
    klienci k
JOIN
    wypozyczenia w ON k.id_klienta = w.id_klienta
GROUP BY
    k.id_klienta, k.imie, k.nazwisko, k.nr_prawa_jazdy, k.telefon
HAVING
    COUNT(w.id_wypozyczenia) >= 5;
