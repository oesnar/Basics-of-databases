import sqlite3
import os

db = sqlite3.connect("transaktiot.db")
db.isolation_level = None



db.execute("BEGIN")
db.execute("UPDATE Testi SET x=2;")
testi2 = db.execute("SELECT x FROM Testi;").fetchall()
db.execute("COMMIT")
print("Testi 2: "+ str(testi2))