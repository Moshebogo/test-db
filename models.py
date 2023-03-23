from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()

class Boats(db.Model):
   __tablename__ = 'boat'
   
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String, nullable = False)
   capacity = db.Column(db.Integer, nullable = False)

   boat_times = db.relationship('BoatTimes', backref = 'boat')


class Times(db.Model):
   __tablename__ = 'time'
   
   id = db.Column(db.Integer, primary_key = True)
   hour = db.Column(db.String, nullable = False)
   day = db.Column(db.String, nullable = False)

   boat_times = db.relationship('BoatTimes', backref = 'time')


class BoatTimes(db.Model):
   __tablename__ = 'boat_times'
   
   id = db.Column(db.Integer, primary_key = True)

   boat_id = db.Column(db.Integer, db.ForeignKey('boat.id'), nullable  = False)
   time_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable  = False)
   