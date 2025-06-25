import requests
import os

def get_puuid(summoner_region, summoner_id, summoner_tag):
  url = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_id}/{summoner_tag}'
  puuid = (requests.get(url, headers = headers)).json()['puuid']
  return puuid

def get_past_matches(summoner_region, account_puuid, num_matches = 20):
  if num_matches > 100:
    return 'The maximum number of matches are displayed.'
  url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_puuid}/ids?start=0&count={num_matches}'
  past_ids = requests.get(url, headers=headers).json()
  return past_ids

def get_player_by_puuid(match_data, account_puuid):
    for player in match_data["info"]["participants"]:
        if player["puuid"] == account_puuid:
            return player
    return None

def calculate_win_loss(summoner_region, account_puuid, match_ids, wins=0, losses=0):
  for id in match_ids:
    url = f'https://{summoner_region}.api.riotgames.com/lol/match/v5/matches/{id}'
    match = requests.get(url, headers=headers).json()
    player_match_data = get_player_by_puuid(match, account_puuid)
    did_win = player_match_data['win']
    early_surrender = player_match_data['gameEndedInEarlySurrender']

    if not did_win:
      losses += 1
    elif not early_surrender: #ensures early surrenders are not counted as wins
      wins += 1
  return wins, losses

def win_loss_message(wins, losses, num_matches=20):
  message = "-"*19
  message += "\nPast " + str(num_matches) + " Games\n" + "Wins: " + str(wins) + " Losses: " + str(losses) + "\n"
  message += str(int((wins/(wins+losses))*100)) + "% Win Rate\n"
  message += "-"*19
  return message

#retrieves environment variable api key 
my_api = os.environ.get('riot_api')

headers={
  'X-Riot-Token': my_api
}

summoner_region = input('Enter region (americas, asia, europe): ').lower()
#asks for region until valid region is provided
while summoner_region not in ['americas', 'asia', 'europe']:
  summoner_region = input('Not a valid region. Try again: ').lower()

#a riot id is comprised of a game name and 3-5 character tag which is preceeded by a #
summoner_id = input('Enter Summoner ID: ').lower()
summoner_tag = input('Enter Summoner Tag: ').lower()

#retrieves encrypted 78 character PUUID associated with account
account_puuid = get_puuid(summoner_region, summoner_id, summoner_tag)

#retrieves the match ids of the past n games played
past_ids = get_past_matches(summoner_region, account_puuid)

#loops through each match id
wins, losses = calculate_win_loss(summoner_region, account_puuid, past_ids)

#prints wins, losses, and win rate over the past 20 games
print(win_loss_message(wins, losses))

'''
#PUUID is used to find the active server of the account (e.g. NA1, EUW)
server = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/region/by-game/lol/by-puuid/{account_puuid}'
server = (requests.get(server, headers=headers)).json()['region']
'''