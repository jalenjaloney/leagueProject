import requests
import os

summoner_region = input('Enter region (americas, asia, europe): ').lower()
while summoner_region not in ['americas', 'asia', 'europe']:
  summoner_region = input('Not a valid region. Try again: ').lower()

summoner_id = input('Enter Summoner ID: ').lower()

summoner_tag = input('Enter Summoner Tag: ').lower()

my_api = os.environ.get('riot_api')

headers={
  'X-Riot-Token': my_api
}

account_url = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_id}/{summoner_tag}'
user_puuid = (requests.get(account_url, headers = headers)).json()['puuid']

server = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/region/by-game/lol/by-puuid/{user_puuid}'
server = (requests.get(server, headers=headers)).json()['region']


summoner_url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{user_puuid}'

summoner = requests.get(summoner_url, headers = headers).json()

past_30_matches_url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_puuid}/ids?start=0&count=30'
past_30_ids = requests.get(past_30_matches_url, headers=headers).json()

wins = 0
losses = 0

for match_id in past_30_ids:
  match_url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
  match = requests.get(match_url, headers=headers).json()
  for participants in match['info']['participants']:
    if participants['puuid'] == user_puuid:
      if participants['win'] and not participants['gameEndedInEarlySurrender']:
        wins += 1
      else:
         losses += 1

print("-"*19, "\nPast 30 Games\n" + "Wins:", wins, "Losses:", losses)