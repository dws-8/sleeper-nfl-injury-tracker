from sleeper_app import get_my_roster_data, get_my_user_data, pop_player_data
from app import app, db
from models import Roster, Players
from flask import render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy


@app.route('/injury_report')
def injury_report():

    get_my_user_data()

    get_my_roster_data()
    
    pop_player_data()
    
    with app.app_context():
     
     # query database for injured players, compare roster to player data and only bring in players with an injury status that is not 'None'
     current_injured = db.session.query(Players.first_name, Players.last_name, Players.injury_status, Players.injury_body_part, Players.injury_notes, Roster).filter(Roster.player_id == db.foreign(Players.player_id), Players.injury_status!=None).all()
     
    # List for players data
     players=[]

     for player in current_injured:
        players.append(player)
        print (*player)
    return render_template('RosterInjuryRpt.html', players = players)
     




#get_my_user_data()

#get_my_roster_data()

#injury_report()