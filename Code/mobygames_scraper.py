import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from collections import defaultdict
import datetime as dt
from dateutil.parser import parse
import pickle
import re
import time
import os

class MobyGamesScraper:
	def __init__(self):
		pass

	def get_platforms_list(self):
		platform_names = []
		platform_urls = []
		url = 'https://www.mobygames.com/browse/games/full,1/'
		html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
		soup = BeautifulSoup(html, 'html.parser')
		platforms = soup.find(class_='browseTable')('div')
		num_cells = len(platforms)
		current_cell = 2
		while current_cell < (num_cells - 1):
			platform = platforms[current_cell]
			platform_names.append(platform.text)
			platform_urls.append(platform.find('a')['href'])
			current_cell += 2
		return list(zip(platform_names, platform_urls))

	def get_games_count(self, url):
		html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
		soup = BeautifulSoup(html, 'html.parser')
		try:
			header = soup.find(class_='mobHeaderItems').text
			total_number = int(header[15:-1])
		except:
			try:
				header = soup.find(class_='mobHeader').text
				total_number = int(header.split()[2])
			except:
				total_number = 1
		return total_number

	def get_games_url(self, url):
		url_list = []
		html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
		soup = BeautifulSoup(html, 'html.parser')
		gametable = soup.find(id='mof_object_list')
		tablerows = gametable.find('tbody')('tr')
		for row in tablerows:
			raw_tag = row.find('a')
			url_list.append(raw_tag['href'])
		return url_list

	def get_games_list(self, url):
		self.games_list = []
		url_head = url + '/offset,'
		offset = 0
		url_tail = '/so,0a/list-games/'
		total_games = self.get_games_count(url_head + str(offset) + url_tail)
		while offset <= (total_games):
			url = url_head + str(offset) + url_tail
			games_on_page = self.get_games_url(url)
			self.games_list += games_on_page
			offset += 25
		return self.games_list	

	def get_game_info(self, url):
		self.game = {'title': '',
					 'console': '',
					 'published by': '',
					 'released': '',
					 'developed by': '',
					 'official site': '',
					 'esrb rating': '',
					 'genre': '',
					 'perspective': '',
					 'visual': '',
					 'art': '',
					 'pacing': '',
					 'gameplay': '',
					 'interface': '',
					 'sport': '',
					 'educational': '',
					 'vehicular': '',
					 'narrative': '',
					 'setting': '',
					 'add-on': '',
					 'misc': '',
					 'special edition': ''
					}

		try:
			html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
			self.game['url'] = url
			self.soup = BeautifulSoup(html, 'html.parser')
			self.scrape()
		except:
			pass

		# Get main info
		try:
			header = self.soup.find(class_='niceHeaderTitle')('a')
			self.game['title'] = header[0].text
			self.game['console'] = header[1].text
		except:
			print("WARNING: Problem getting main information")
			pass			

		# Get info about release
		try:		
			game_info = self.soup.find(id='coreGameRelease')('div')
			num_cells = len(game_info)
			current_cell = 0
			while current_cell < (num_cells - 1):
				field = game_info[current_cell].text.replace('\xa0', ' ').lower()
				value = game_info[current_cell + 1]
			
				if field in self.game:
					self.game[field] = ' | '.join([content.text.replace('\xa0', ' ') for content in value.contents if content != ', '])
				current_cell += 2
		except:
			print("WARNING: Problem getting release information")
			pass

		# Get info about genre
		try:
			genre_info = self.soup.find(id='coreGameGenre')('div')
			num_cells = len(genre_info)
			if genre_info[0].text == '':
				current_cell = 2
			else:
				current_cell = 1
			while current_cell < (num_cells - 1):
				field = genre_info[current_cell].text.replace('\xa0', ' ').lower()
				value = genre_info[current_cell + 1]
			
				if field in self.game:
					self.game[field] = ' | '.join([content.text.replace('\xa0', ' ') for content in value.contents if content != ', '])
				current_cell += 2			
		except:
			print("WARNING: Problem getting genre information")
			pass

		return self.game

mobygames_scraper = MobyGamesScraper()
#print(mobygames_scraper.get_game_info('https://www.mobygames.com/game/switch/fire-emblem-warriors'))
#print(mobygames_scraper.get_game_info('https://www.mobygames.com/game/007-the-world-is-not-enough_'))
#print(mobygames_scraper.get_games_list('https://www.mobygames.com/browse/games/1292-advanced-programmable-video-system/'))
#print(mobygames_scraper.get_games_url('https://www.mobygames.com/browse/games/n64/list-games/'))
#print(mobygames_scraper.get_games_count('https://www.mobygames.com/browse/games/altair-680/offset,0/so,0a/list-games/'))
#print(mobygames_scraper.get_platforms_list())