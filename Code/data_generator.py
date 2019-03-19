import csv
from metacritic_scraper import MetaCriticScraper

platforms = ['ps4', 'xboxone', 'switch', 'pc', 'wii-u', '3ds', 'vita', 'ps3', 'ps2', 'ps',
           'xbox360', 'xbox', 'wii', 'ds', 'gamecube', 'n64', 'gba', 'psp', 'dreamcast']
          
metacritic_scraper = MetaCriticScraper()
for platform in platforms:
     games = []
     games_list = metacritic_scraper.get_games_list(platform)
     print(f'Platform - {platform}')
     for i, game in enumerate(games_list):
          games.append(metacritic_scraper.get_game_info('https://www.metacritic.com' + game))
          print(f'{i} / {len(games_list)}')

     keys = games[0].keys()
     with open('metacritic_' + platform + '.csv', 'w') as f:
          dict_writer = csv.DictWriter(f, keys, delimiter=';')
          dict_writer.writeheader()
          dict_writer.writerows(games)