from metacritic_scraper import MetaCriticScraper

metacritic_scraper = MetaCriticScraper()
games_list = metacritic_scraper.get_games_list('ps4')
games = []
for game in games_list[:10]:
     games.append(metacritic_scraper.get_game_info('https://www.metacritic.com' + game))

import csv
keys = games[0].keys()
with open('metacritic.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(games)