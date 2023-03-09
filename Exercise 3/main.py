import sqlite3
import os
import random
import time
from string import ascii_lowercase

#Initializes a database with no indexes
def initialize1():
    os.remove("nopeustesti1.db")
    db = sqlite3.connect("nopeustesti1.db")
    db.isolation_level = None
    db.execute("CREATE TABLE Elokuvat(id INTEGER PRIMARY KEY, nimi TEXT, vuosi INTEGER)")
    return db


#Initializes a database with indexes on vuosi
def initialize2():
    os.remove("nopeustesti2.db")
    db = sqlite3.connect("nopeustesti2.db")
    db.isolation_level = None
    db.execute("CREATE TABLE Elokuvat(id INTEGER PRIMARY KEY, nimi TEXT, vuosi INTEGER)")
    db.execute("CREATE INDEX idx_vuosi ON Elokuvat (vuosi)")
    return db

#Initializes a database with no indexes
def initialize3():
    #os.remove("nopeustesti3.db")
    db = sqlite3.connect("nopeustesti3.db")
    db.isolation_level = None
    db.execute("CREATE TABLE Elokuvat(id INTEGER PRIMARY KEY, nimi TEXT, vuosi INTEGER)")
    return db

def create_data(times, db, measure = False):
    start_time = time.time()
    db.execute("BEGIN")
    for i in range(times):
        db.execute("INSERT INTO Elokuvat(nimi, vuosi) VALUES (?, ?)", ["".join(random.choice(ascii_lowercase) for i in range(8)), random.randrange(1900, 2001)])
    db.execute("COMMIT")
    process_time = time.time() - start_time
    if measure:
        return process_time, db
    else:
        return db

def data_lookup(times, db, measure = False):
    start_time = time.time()
    for i in range(times):
        db.execute("SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?", [random.randrange(1900, 2001)])
    process_time = time.time() - start_time
    if measure:
        return process_time
    else:
        return

def data_lookup_idx(times, db, measure = False):
    start_time = time.time()
    db.execute("CREATE INDEX idx_vuosi ON Elokuvat (vuosi)")
    for i in range(times):
        db.execute("SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?", [random.randrange(1900, 2001)])
    process_time = time.time() - start_time
    if measure:
        return process_time
    else:
        return

def main():
    db1 = initialize1()
    db2 = initialize2()
    db3 = initialize3()

    creation_time1, db1 = create_data(1000000, db1, True)
    lookup_time1 = data_lookup(1000, db1, True)
    total_time1 = creation_time1 + lookup_time1

    creation_time2, db2 = create_data(1000000, db2, True)
    lookup_time2 = data_lookup(1000, db2, True)
    total_time2 = creation_time2 + lookup_time2

    creation_time3, db3 = create_data(1000000, db3, True)
    lookup_time3 = data_lookup_idx(1000, db3, True)
    total_time3 = creation_time3 + lookup_time3

    print("Database 1: Creation time: " + str(creation_time1) + ", Lookup time: " + str(lookup_time1) + ", Total time: " + str(total_time1))
    print("Database 2: Creation time: " + str(creation_time2) + ", Lookup time: " + str(lookup_time2) + ", Total time: " + str(total_time2))
    print("Database 3: Creation time: " + str(creation_time3) + ", Lookup time: " + str(lookup_time3) + ", Total time: " + str(total_time3))    

if __name__ == "__main__":
    main()