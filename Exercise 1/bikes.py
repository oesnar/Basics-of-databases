import sqlite3 

db = sqlite3.connect("bikes.db")
db.isolation_level = None

def distance_of_user(user):
    palaute = db.execute("SELECT SUM(Trips.distance) FROM Trips, Users WHERE Trips.user_id = Users.id AND Users.name=?", [user]).fetchone()
    return palaute[0]

def time_of_user(user):
    palaute = db.execute("SELECT SUM(Trips.duration) FROM Trips, Users WHERE Trips.user_id = Users.id AND Users.name=?", [user]).fetchone()
    return palaute[0]

def speed_of_user(user):
    distance = distance_of_user(user)
    time = time_of_user(user)
    speed = (distance/1000)/(time/60)
    return round(speed, 2)

def duration_in_each_city(day):
    palaute = db.execute("SELECT Cities.name, SUM(Trips.duration) FROM Trips LEFT JOIN Stops ON Trips.from_id = Stops.id LEFT JOIN Cities ON Stops.city_id = Cities.id WHERE Trips.day=? GROUP BY Cities.id", [day]).fetchall()
    return palaute

def users_in_city(city):
    palaute = db.execute("SELECT COUNT(Users.id) FROM Trips LEFT JOIN Cities ON Trips.from_id = Cities.id LEFT JOIN Users ON Trips.user_id = Users.id WHERE Cities.name = ?", [city]).fetchone()
    return palaute

def trips_on_each_day(city):
    palaute = db.execute("SELECT Trips.day, COUNT(Trips.id) FROM Trips LEFT JOIN Stops ON Trips.from_id = Stops.id LEFT JOIN Cities ON Stops.city_id = Cities.id WHERE Cities.name = ? GROUP BY Trips.day",[city]).fetchall()
    return palaute

def most_popular_start(city):
    palaute = db.execute("SELECT Stops.name, COUNT(Trips.from_id) FROM Trips LEFT JOIN Stops ON Trips.from_id = Stops.id LEFT JOIN Cities ON Stops.city_id = Cities.id WHERE Cities.name = ? GROUP BY Stops.id ORDER BY COUNT(Trips.from_id) DESC",[city]).fetchone()
    return palaute