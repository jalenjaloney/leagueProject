import requests
import os

summoner_region = 'americas'
summoner_id = 'saphenous'
summoner_tag = '115'

url = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_id}/{summoner_tag}'

my_api = os.environ.get('riot_api')

headers={
  'X-Riot-Token': my_api
}

account_by_riot_id = requests.get(url, headers = headers)

print(account_by_riot_id.json())