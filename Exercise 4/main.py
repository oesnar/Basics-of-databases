import sqlite3
import os

os.remove("transaktiot.db")
db = sqlite3.connect("transaktiot.db")
db.isolation_level = None

db.execute("CREATE TABLE Testi (x INTEGER)") 
db.execute("INSERT INTO Testi (x) VALUES (1)")

#testi1

db.execute("BEGIN")
db.execute("UPDATE Testi SET x=2;")

input()
testi1 = db.execute("SELECT x FROM Testi;").fetchall()
db.execute("COMMIT")
print("Testi1: " + str(testi1))
