from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()

class Boats:
   
   id = db.Column(db.Integer, primaryKey = True)
   name = db.Column(db.String, nullable = False)
   capacity = db.Column(db.Integer, nullable = False)


class Times:
   
   id = db.Column(db.Integer, primaryKey = True)
   hour = db.Column(db.String, nullable = False)
   day = db.Column(db.String, nullable = False)


class BoatTimes:
   
   id = db.Column(db.Integer, primaryKey = True)
   boat_id = db.Column(db.Integer, nullable  = False)