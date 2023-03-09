Opettajia
-id, nimi

#CREATE TABLE Opettajat(id INTEGER PRIMARY KEY, nimi TEXT)

Kursseja
-id, nimi, op

 ->Opetustehtavat
   id, kurssi_id, opettaja_id

#CREATE TABLE Kurssit(id INTEGER PRIMARY KEY, nimi TEXT, credits INTEGER, opettaja_id INTEGER REFRENCES Opettajat)

Opiskelijoita
-id, nimi

#CREATE TABLE Opiskelijat(id INTEGER PRIMARY KEY, nimi TEXT)

Suorituksia
id, opiskelija_id, kurssi_id, date, arvosana

#CREATE TABLE Suoritukset(id INTEGER PRIMARY KEY, opiskelija_id INTEGER REFERENCES Opiskelijat, kurssi_id INTEGER REFERENCES Kurssit, date DATETIME, arvosana INTEGER)

Ryhmiä
id, nimi

#CREATE TABLE Ryhmat(id INTEGER PRIMARY KEY, nimi TEXT)

 -> Lisätään Jäsenet -taulu
    id, ryhmä_id, opiskelija_id/opettaja_id
    #CREATE TABLE Jasenyydet(id INTEGER PRIMARY KEY, ryhma_id INTEGER REFERENCES Ryhmat, opiskelija_id INTEGER REFERENCES Opiskelijat, opettaja_id INTEGER REFERENCES Opettajat)

Courses_by_teacher
SELECT
 Kurssit.nimi
FROM
 Opetustehtavat LEFT JOIN Kurssit ON Opetustehtavat.kurssi_id = Kurssit.id
                LEFT JOIN Opettajat ON Opetustehtavat.opettaja_id = Opettajat.id
WHERE 
 Opettajat.nimi = ?
ORDER BY
 Kurssit.nimi




credits_by_teacher
SELECT
 SUM(Kurssit.credits)
FROM
 Opettajat, Opetustehtavat, Kurssit, Suoritukset
WHERE
 Opetustehtavat.opettaja_id = Opettajat.id AND
 Kurssit.id = Opetustehtavat.kurssi_id AND
 Suoritukset.kurssi_id = Kurssit.id AND
 Opettaja.nimi = ?




courses_by_student
SELECT
 Kurssit.nimi
FROM
 Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id
             LEFT JOIN Opiskelijat ON Suoritukset.opiskelija_id = Opiskelijat.id
WHERE
 Opiskelijat.nimi = ?
ORDER BY
 Kurssit.nimi




credits_by_year
SELECT
 SUM(Kurssit.credits)
FROM
 Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id
WHERE
 SUBSTR(Suoritukset.date, 1, 4) = ?



grade_distribution 
SELECT 
 COUNT(Suoritukset.arvosana)
FROM 
 Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id
WHERE
 Kurssit.nimi = ? 
GROUP BY
 Suoritukset.arvosana



course_list
SELECT
 Kurssit.nimi, COUNT(Opetustehtävät.id)
FROM
 Kurssit LEFT JOIN Opetustehtävät ON Opetustehtävät.kurssi_id = Kurssit.id
GROUP BY
 Kurssit.nimi 
ORDER BY
 Kurssit.nimi

SELECT
 Kurssit.nimi, COUNT(Suoritukset.id)
FROM
 Kurssit LEFT JOIN Suoritukset ON Suoritukset.kurssi_id = Kurssit.id
GROUP BY
 Kurssit.nimi 
ORDER BY
 Kurssit.nimi



group_people(group_name)
SELECT
 Opiskelijat.nimi, Opettajat.nimi
FROM 
 Jasenet LEFT JOIN Ryhmat ON Jasenet.ryhma_id = Ryhmat.id 
         LEFT JOIN Opiskelijat ON Jasenet.opiskelija_id = Opiskelijat.id
         LEFT JOIN Opettajat ON Jasenet.opettaja_id = Opettajat.id
WHERE
 Ryhma.nimi = ?
ORDER BY
 Opiskelija.nimi



credits_in_groups
SELECT
 Ryhmat.nimi, SUM(Kurssit.credits)
FROM
 Ryhmat LEFT JOIN Jasenyydet ON Ryhmat.id = Jasenyydet.ryhma_id
        LEFT JOIN Opiskelijat ON Jasenyydet.opiskelija_id = Opiskelijat.id
	LEFT JOIN Suoritukset ON Suoritukset.opiskelija_id = Opiskelijat.id
	LEFT JOIN Kurssit ON Suoritukset.kurssti_id = Kurssit.id
GROUP BY
 Ryhmat.nimi



common_groups(teacher_name, student_name)
SELECT
 Jasenyydet.id
FROM
 Opiskelijat, Opettajat, Jasenyydet, Ryhmat
WHERE
 Opettaja.nimi = ? AND Opiskelija.nimi = ? AND
 Opiskelijat.id = Jasenyydet.opsikelija_id 





OR Opettajat.id = Jasenyydet.opettaja_id


SELECT
 Ryhmat.nimi
FROM
 Opiskelijat, Opettajat, Ryhmat,
 (SELECT * FROM Jasenyydet WHERE Opiskelija_id IS NOT NULL) AS Opiskelijajasenyydet,
 (SELECT * FROM Jasenyydet WHERE Opettaja_id IS NOT NULL) AS Opettajajasenyydet
WHERE
 Opettajat.nimi = ? AND Opiskelijat.nimi = ? AND Opiskelijajasenyydet.ryhma_id = Opettajajasenyydet.ryhma_id AND
 Opiskelijat.id = Opiskelijajasenyydet.opiskelija_id AND Opettajat.id = Opettajajasenyydet.opettaja_id AND 
 Opiskelijajasenyydet.ryhma_id = Kurssit.id AND Opettajajasenyydet.kurssi_id = Kurssit.id




SELECT
 Ryhmat.nimi
FROM
 (SELECT * FROM Jasenyydet WHERE Opiskelija_id IS NOT NULL) AS Opiskelijajasenyydet,
 (SELECT * FROM Jasenyydet WHERE Opettaja_id IS NOT NULL) AS Opettajajasenyydet LEFT JOIN Ryhmat ON 
WHERE
 Opettajat.nimi = ? AND Opiskelijat.nimi = ? AND Opiskelijajasenyydet.ryhma_id = Opettajajasenyydet.ryhma_id AND
 Opiskelijat.id = Opiskelijajasenyydet.opiskelija_id AND Opettajat.id = Opettajajasenyydet.opettaja_id


