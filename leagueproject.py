import requests
import os

summoner_region = input('Enter region (americas, asia, europe): ').lower()

#asks for region until valid region is provided
while summoner_region not in ['americas', 'asia', 'europe']:
  summoner_region = input('Not a valid region. Try again: ').lower()


#a riot id is comprised of a game name and 3-5 character tag which is preceeded by a #
summoner_id = input('Enter Summoner ID: ').lower()
summoner_tag = input('Enter Summoner Tag: ').lower()

#retrieves environment variable api key 
my_api = os.environ.get('riot_api')

headers={
  'X-Riot-Token': my_api
}

#retrieves encrypted 78 character PUUID associated with account
account_url = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_id}/{summoner_tag}'
user_puuid = (requests.get(account_url, headers = headers)).json()['puuid']

#PUUID is used to find the active server of the account (e.g. NA1, EUW)
server = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/region/by-game/lol/by-puuid/{user_puuid}'
server = (requests.get(server, headers=headers)).json()['region']

#retrieves the match ids of the past 30 games played
past_30_matches_url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_puuid}/ids?start=0&count=30'
past_30_ids = requests.get(past_30_matches_url, headers=headers).json()

wins = 0
losses = 0

#loops through each match id
for match_id in past_30_ids:
  #retrieves information of a match
  match_url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
  match = requests.get(match_url, headers=headers).json()
  #loops through the players in match, finds the specified account, checks for win/loss and increments correspondingly
  for players in match['info']['participants']:
    if players['puuid'] == user_puuid:
      if not players['win']:
        losses += 1
      elif not players['gameEndedInEarlySurrender']: #ensures remakes are not counted as wins
        wins += 1

#prints wins, losses, and win rate over the past 30 games
print("-"*19)
print("Past 30 Games\n" + "Wins:", wins, "Losses:", losses)
print(str(int((wins/(wins+losses))*100)) + "% Win Rate")
print("-"*19)