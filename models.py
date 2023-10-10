from flask_sqlalchemy import SQLAlchemy
from app import db

# Create table for user data

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique = True)
    rosters = db.relationship('Roster', backref='user', lazy=True)
    
    def __repr__(self):
        return "{}".format(self.user_id)
   


# Creat table for Team roster data

class Roster(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    roster_id = db.Column(db.Integer, index =True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index =True)
    
    def __repr__(self):
        return "{}".format(self.player_id)

# Create a table for all player data from Sleeper API
class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), index=True)
    last_name = db.Column(db.String(80), index=True)
    injury_status = db.Column(db.String(50), index=True)
    
    def __repr__(self):
        return "{}".format(self.player_id)

# Use an inner join query to populate from roster and players table. Display list using an HTML template.
