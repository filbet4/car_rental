
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






\item
    \textbf{Chest X-ray Analyzer (group project)} \\
    Python project designed to analyze given Chest X-rays in order to provide information about possible diseases using Django, PyTorch and Kaggle. 
\item
    \textbf{Car Rental} \\
    Application written in Python using PostgreSQL, allowing admin to manage clients, vehicles and rentals.