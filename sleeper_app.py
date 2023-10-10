from flask import Flask
from api_util import get_user_data, get_roster, get_players
from models import db, User, Roster, Players
from app import app  # Import the app instance
import json


# Function takes response from API call in api_util for getting user data and updates database table.

def get_my_user_data():
    with app.app_context():
      db.create_all()
      username = 'dansannn'
      my_user_data = get_user_data(username)
      if my_user_data:
        user_id = my_user_data['user_id']
        username = my_user_data['username']

      # Check if user exists in users table using the user_id
        existing_user = User.query.filter_by(user_id=user_id).first()
        if existing_user:
           print('User id already exists in database.')
        else:
          my_user = User(user_id=user_id, username=username)
          db.session.add(my_user) #Write data to table
          db.session.commit()
          print('User data was updated.')
      else:
        print('Failed to get user data from Sleeper API.')


# Function takes response from API call in api_util and uses it to update database table.
def  get_my_roster_data():
  with app.app_context():
    # Call API function to get current roster
    my_roster_data = get_roster()
    # Query Roster table to get current players in DB to compare
    players_in_db= Roster.query.all()

   
    print(players_in_db)
    for team_data in my_roster_data:
        if team_data['owner_id'] == '869056602236461056': # hard coding ID for now
           players = team_data['players']
           roster = team_data['roster_id']
           owner = team_data['owner_id']
           print(players)

           # Create a list of players in the database based on their ID 
           db_player_ids = [player_db.player_id for player_db in players_in_db]
           for player in players:   # Loop through players list, check for numerics..If they are all numbers convert to INT and write to database. 
              if player.isnumeric():
                player_id = int(player)
                roster_id = roster
                owner_id = owner
                 # Check if user exists in users table using the player_id if it exists do nothing for now
                 # Else they are a new player add them to the database
                if player_id in db_player_ids:
                 print('Player already exists in database.. nothing to do here')
                else:
                  roster_record = Roster(player_id=player, roster_id=roster, owner_id=owner)    
                  db.session.add(roster_record)
                  db.session.commit()

 #  If the player is defense aka non numeric ID do nothing save off the string incase we want to do something else with it later.
           else:                 
             print(player)
        
              # Check if player exists but not in the API resposnse...This means the player has been dropped and the record should be removed from the database
             for db_player in players_in_db:
              if not any(player.isdigit() and int(player) == db_player.player_id for player in players):
                print('Trying to delete player ' + str(db_player.player_id))
                db.session.delete(db_player)
                db.session.commit()

def pop_player_data():
  with app.app_context():
    #json_response_path='player_data.json'
    #with open(json_response_path, 'r') as file:
     player_data = get_players()
     # Purge all database records before writing the updates.
     db.session.query(Players).delete()
     db.session.commit()
     if player_data is None:
            # Handle the case where get_players() returns None
            print("Error: get_players() returned None")
            return

     for player_record in player_data:
      # Check if player is active and not a defense... if so add to the players table
      if player_record.isnumeric() and player_data[player_record]['status'] != 'Inactive':
       player_id = player_data[player_record]['player_id']
       first_name = player_data[player_record]['first_name']
       last_name = player_data[player_record]['last_name']
       injury_status = player_data[player_record]['injury_status']
       #print(first_name, last_name, injury_status)
    # Because we want this to be updated everytime whether the player already exists or not, we are not checking to see if this player exists.
       player = Players(player_id=player_id, first_name=first_name, last_name=last_name, injury_status=injury_status)
       db.session.add(player)
       db.session.commit()


get_my_user_data()

get_my_roster_data()

pop_player_data()