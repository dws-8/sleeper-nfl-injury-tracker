import os
import requests, json
import datetime



current_day = datetime.datetime.now() 
today = current_day.strftime("%b") + ' ' + current_day.strftime("%d")

print(today) 
#roster_data = get_my_roster()

# Request user data for use in roster table and populate User table. If we get a good response update the table. We are not checking if record exists because we are looking for only 1 user.
def get_user_data(username):
    username = 'dansannn'
    api_url = f"https://api.sleeper.app/v1/user/{username}" # Set API url Hardcoding my username
    response = requests.get(api_url)
    if response.status_code==200:
        return response.json() # Return json from api get request if not return error.
    else:
        return response.status_code



# Request league roster data and add player ID's to table from sleeper
# user_id and ownerid = 869056602236461056
def get_roster():
    api_url="https://api.sleeper.app/v1/league/993209494500937728/rosters"
# If we get a OK resposne pass the data to the main app function
    response = requests.get(api_url)
    if response.status_code==200:
        return response.json()
    else:
        return response.status_code
    

   
# Function used to populate database from sleeper api, NON inactive players only.
def get_players():
 # Path to file where we will store the last date this function was ran to avoid running function more than once per day.
 date_file_path = 'last_updated_date.txt'
 json_response_path='player_data.json'
 # Check day of the week.
 if os.path.exists(date_file_path):
    with open(date_file_path, 'r') as file:
     stored_date = file.read()
     # compare file to today's day value if it's not the same run the code.
     if today != stored_date:
        api_url="https://api.sleeper.app/v1/players/nfl"
    # If we get OK response pass data to the main app function to populate player db
        response = requests.get(api_url)
        if response.status_code==200:
            with open(date_file_path, 'w') as file:
               file.write(today)
            #with open(json_response_path, 'w') as file:
              # file.write(str(response.json()))
            return response.json()
        print('Updated Players database successfully.')
     else:
         print('Already retrieved up to date data.')
            