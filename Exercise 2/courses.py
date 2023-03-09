import os
import sqlite3

# poistaa tietokannan alussa (kätevä moduulin testailussa)
os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut
def create_tables():
    db.execute("CREATE TABLE Opettajat(id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Kurssit(id INTEGER PRIMARY KEY, nimi TEXT, credits INTEGER)")
    db.execute("CREATE TABLE Opetustehtavat(id INTEGER PRIMARY KEY, kurssi_id INTEGER REFERENCES Kurssit, opettaja_id INTEGER REFERENCES Opettajat)")
    db.execute("CREATE TABLE Opiskelijat(id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Suoritukset(id INTEGER PRIMARY KEY, opiskelija_id INTEGER REFERENCES Opiskelijat, kurssi_id INTEGER REFERENCES Kurssit, date DATETIME, arvosana INTEGER)")
    db.execute("CREATE TABLE Ryhmat(id INTEGER PRIMARY KEY, nimi TEXT)")
    db.execute("CREATE TABLE Jasenyydet(id INTEGER PRIMARY KEY, ryhma_id INTEGER REFERENCES Ryhmat, opiskelija_id INTEGER REFERENCES Opiskelijat, opettaja_id INTEGER REFERENCES Opettajat)")

# lisää opettajan tietokantaan
def create_teacher(name):
    tulos = db.execute("INSERT INTO Opettajat(nimi) VALUES (?)", [name])
    return tulos.lastrowid

# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    tulos = db.execute("INSERT INTO Kurssit(nimi, credits) VALUES (?, ?)", [name, credits])
    kurssi_id = tulos.lastrowid
    for id in teacher_ids:
        db.execute("INSERT INTO Opetustehtavat(kurssi_id, opettaja_id) VALUES (?, ?)", [kurssi_id, id])
    return kurssi_id

# lisää opiskelijan tietokantaan
def create_student(name):
    tulos = db.execute("INSERT INTO Opiskelijat(nimi) VALUES (?)", [name])
    return tulos.lastrowid

# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    tulos = db.execute("INSERT INTO Suoritukset(opiskelija_id, kurssi_id, date, arvosana) VALUES (?,?,?,?)", [student_id, course_id, date, grade])
    return tulos.lastrowid

# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    tulos = db.execute("INSERT INTO Ryhmat(nimi) VALUES (?)", [name])
    ryhma_id = tulos.lastrowid
    for id in teacher_ids:
        db.execute("INSERT INTO Jasenyydet(ryhma_id, opettaja_id) VALUES (?,?)", [ryhma_id, id])
    for id in student_ids:
        db.execute("INSERT INTO Jasenyydet(ryhma_id, opiskelija_id) VALUES (?,?)", [ryhma_id, id])
    return ryhma_id

# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    tulokset = db.execute("SELECT Kurssit.nimi FROM Opetustehtavat LEFT JOIN Kurssit ON Opetustehtavat.kurssi_id = Kurssit.id LEFT JOIN Opettajat ON Opetustehtavat.opettaja_id = Opettajat.id WHERE Opettajat.nimi = ? ORDER BY Kurssit.nimi", [teacher_name]).fetchall()
    palaute = []
    for tulos in tulokset:
        palaute.append(tulos[0])
    return palaute

# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    palaute = db.execute("SELECT SUM(Kurssit.credits) FROM Opettajat, Opetustehtavat, Kurssit, Suoritukset WHERE Opetustehtavat.opettaja_id = Opettajat.id AND Kurssit.id = Opetustehtavat.kurssi_id AND Suoritukset.kurssi_id = Kurssit.id AND Opettajat.nimi = ?", [teacher_name]).fetchone()
    return palaute[0]

# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    tulokset = db.execute("SELECT Kurssit.nimi, Suoritukset.arvosana FROM Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id LEFT JOIN Opiskelijat ON Suoritukset.opiskelija_id = Opiskelijat.id WHERE Opiskelijat.nimi = ? ORDER BY Kurssit.nimi", [student_name]).fetchall()
    palaute = []
    for tulos in tulokset:
        palaute.append((tulos[0], tulos[1]))
    return palaute

# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    tulos = db.execute("SELECT SUM(Kurssit.credits) FROM Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id WHERE SUBSTR(Suoritukset.date, 1, 4) = ?", [str(year)]).fetchone()
    return tulos[0]

# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    tulokset = db.execute("SELECT COUNT(Suoritukset.arvosana) FROM Suoritukset LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id WHERE Kurssit.nimi = ? GROUP BY Suoritukset.arvosana", [course_name]).fetchall()
    palaute = dict()
    i = 1
    for tulos in tulokset:
        palaute[i] = (tulos[0])
        i += 1
    return palaute


# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    tulos1 = db.execute("SELECT Kurssit.nimi, COUNT(Opetustehtavat.id) FROM Kurssit LEFT JOIN Opetustehtavat ON Opetustehtavat.kurssi_id = Kurssit.id GROUP BY Kurssit.nimi ORDER BY Kurssit.nimi").fetchall()
    tulos2 = db.execute("SELECT COUNT(Suoritukset.id) FROM Kurssit LEFT JOIN Suoritukset ON Suoritukset.kurssi_id = Kurssit.id GROUP BY Kurssit.nimi ORDER BY Kurssit.nimi").fetchall()
    tulos = tuple(zip(tulos1, tulos2))
    return tulos
        

# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    pass

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    tulos = db.execute("SELECT Opiskelijat.nimi, Opettajat.nimi FROM Jasenyydet LEFT JOIN Ryhmat ON Jasenyydet.ryhma_id = Ryhmat.id LEFT JOIN Opiskelijat ON Jasenyydet.opiskelija_id = Opiskelijat.id LEFT JOIN Opettajat ON Jasenyydet.opettaja_id = Opettajat.id WHERE Ryhmat.nimi = ?", [group_name]).fetchall()
    palaute = []
    for outer in tulos:
        for inner in outer:
            if inner != None:
                palaute.append(inner)
    j = sorted(palaute)
    return j

# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    tulos = db.execute("SELECT Ryhmat.nimi, IFNULL(SUM(Kurssit.credits),0) FROM Ryhmat LEFT JOIN Jasenyydet ON Ryhmat.id = Jasenyydet.ryhma_id LEFT JOIN Opiskelijat ON Jasenyydet.opiskelija_id = Opiskelijat.id LEFT JOIN Suoritukset ON Suoritukset.opiskelija_id = Opiskelijat.id LEFT JOIN Kurssit ON Suoritukset.kurssi_id = Kurssit.id GROUP BY Ryhmat.nimi").fetchall()
    return tulos

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    tulos = db.execute("SELECT Ryhmat.nimi FROM Opiskelijat, Opettajat, Ryhmat, (SELECT * FROM Jasenyydet WHERE Opiskelija_id IS NOT NULL) AS Opiskelijajasenyydet, (SELECT * FROM Jasenyydet WHERE Opettaja_id IS NOT NULL) AS Opettajajasenyydet WHERE Opettajat.nimi = ? AND Opiskelijat.nimi = ? AND Opiskelijat.id = Opiskelijajasenyydet.opiskelija_id AND Opettajat.id = Opettajajasenyydet.opettaja_id AND Opiskelijajasenyydet.ryhma_id = Opettajajasenyydet.ryhma_id AND Opiskelijajasenyydet.ryhma_id = Ryhmat.id AND Opettajajasenyydet.ryhma_id = Ryhmat.id", [teacher_name, student_name]).fetchall()
    palaute = []
    for x in tulos:
        palaute.append(x[0])
    return palaute