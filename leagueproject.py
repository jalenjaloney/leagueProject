import requests
import os

summoner_region = input('Enter your region (americas, asia, europe): ').lower()
while summoner_region not in ['americas', 'asia', 'europe']:
  summoner_region = input('Not a valid region. Try again: ').lower()

summoner_id = input('Enter your Summoner ID: ')

summoner_tag = input('Enter your Summoner Tag: ')

url = f'https://{summoner_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_id}/{summoner_tag}'

my_api = os.environ.get('riot_api')

headers={
  'X-Riot-Token': my_api
}

account_by_riot_id = requests.get(url, headers = headers)

print(account_by_riot_id.json())