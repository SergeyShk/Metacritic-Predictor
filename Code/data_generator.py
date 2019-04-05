import csv
from metacritic_scraper import MetaCriticScraper
from mobygames_scraper import MobyGamesScraper

platforms_mc = ['ps4', 'xboxone', 'switch', 'pc', 'wii-u', '3ds', 'vita', 'ps3', 'ps2', 'ps',
           'xbox360', 'xbox', 'wii', 'ds', 'gamecube', 'n64', 'gba', 'psp', 'dreamcast', 'ios']

metacritic_scraper = MetaCriticScraper()
for platform in platforms_mc:
	print(f'Platform - {platform}')
	games = []
	games_list = metacritic_scraper.get_games_list(platform)
	
	for i, game in enumerate(games_list):
		games.append(metacritic_scraper.get_game_info('https://www.metacritic.com' + game))
		print(f'{i + 1} / {len(games_list)}')

	keys = games[0].keys()
	with open('Data/metacritic_' + platform + '.csv', 'w') as f:
		dict_writer = csv.DictWriter(f, keys, delimiter=';')
		dict_writer.writeheader()
		dict_writer.writerows(games)

mobygames_scraper = MobyGamesScraper()
platforms_mg = mobygames_scraper.get_platforms_list()
for i, (platform_name, platform_url) in enumerate(platforms_mg):		
	print(f'Platform - {platform_name}')
	games = []
	games_list = mobygames_scraper.get_games_list(platform_url)

	for j, game in enumerate(games_list):
		games.append(mobygames_scraper.get_game_info(game))
		print(f'{j + 1} / {len(games_list)}')

	keys = games[0].keys()
	with open('Data/mobygames.csv', 'a') as f:
		dict_writer = csv.DictWriter(f, keys, delimiter=';')
		if i == 0:
			dict_writer.writeheader()
		dict_writer.writerows(games)