from bs4 import BeautifulSoup
import requests

class MetaCriticScraper:
	def __init__(self):
		pass

	def get_games_list(self, platform):
		self.games_list = []
		page = 0
		last_page = False

		while (last_page == False):
			url = 'https://www.metacritic.com/browse/games/release-date/available/' + platform + '/date?page=' + str(page)
			html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
			soup = BeautifulSoup(html, 'html.parser')
			if not soup.find('p', class_='no_data'):
				self.games_list += [game.find('a')['href'] for game in soup.find('ol', class_='list_products list_product_condensed').findAll('div', class_='basic_stat product_title')]
				page += 1
			else:
				last_page = True

		return self.games_list
	
	def get_game_info(self, url):
		self.game = {'title': '',
					 'platform': '',
					 'publisher': '',
					 'release_date': '',
					 'critic_score': '',
					 'critic_count': '',
					 'critic_positive': '',
					 'critic_mixed': '',
					 'critic_negative': '',
					 'user_score': '',
					 'user_count': '',
					 'user_positive': '',
					 'user_mixed': '',
					 'user_negative': '',
					 'developer': '',
					 'genre': '',
					 'players': '',
					 'rating': '',
					 'director': '',
					 'writer': '',
					 'composer': ''
					}
		
		try:
			html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
			html_details = requests.get(url + '/details', headers={'User-Agent': 'Mozilla/5.0'}).content
			
			self.game['url'] = url
			self.soup = BeautifulSoup(html, 'html.parser')
			self.soup_details = BeautifulSoup(html_details, 'html.parser')
			self.scrape()
		except:
			pass

		# Get title and platforms
		try:
			product_title_div = self.soup.find('div', class_='product_title')
			self.game['title'] = product_title_div.a.text.strip()
			self.game['platform'] = product_title_div.span.a.text.strip()
		except:
			print('WARNING: Problem getting title and platform information')
			pass
			
		# Get publisher and release date
		try:
			self.game['publisher'] = self.soup.find('li', class_='summary_detail publisher').a.text.strip()
			self.game['release_date'] = self.soup.find('li', class_='summary_detail release_data').find('span', class_='data').text.strip()
		except:
			print('WARNING: Problem getting publisher and release date information')
			pass
			
		# Get critic information
		try:
			critics = self.soup.find('div', class_='details main_details')
			self.game['critic_score'] = critics.find('span', itemprop='ratingValue').text.strip()
			critics_reviews = self.soup.find('div', class_='module reviews_module critic_reviews_module')
			score_counts = critics_reviews.find('ol', class_='score_counts hover_none')
			self.game['critic_positive'], self.game['critic_mixed'], self.game['critic_negative'] = (str(score.text.split()[0]).replace(',', '') for score in 
																										score_counts.findAll('span', class_='count'))
			self.game['critic_count'] = str(int(self.game['critic_positive']) + int(self.game['critic_mixed']) + int(self.game['critic_negative']))
		except:
			print('WARNING: Problem getting critic score information')
			pass
			
		# Get user information
		try:
			users = self.soup.find('div', class_='details side_details')
			self.game['user_score'] = users.find('div', class_='metascore_w').text.strip()
			users_reviews = self.soup.find('div', class_='module reviews_module user_reviews_module')
			score_counts = users_reviews.find('ol', class_='score_counts hover_none')
			self.game['user_positive'], self.game['user_mixed'], self.game['user_negative'] = (str(score.text.split()[0]).replace(',', '') for score in 
																								score_counts.findAll('span', class_='count'))
			self.game['user_count'] = str(int(self.game['user_positive']) + int(self.game['user_mixed']) + int(self.game['user_negative']))
		except:
			print('WARNING: Problem getting user score information')
			pass
				
		# Get remaining information
		try:
			product_info = self.soup.find('div', class_='section product_details').find('div', class_='details side_details')
			self.game['developer'] = product_info.find('li', class_='summary_detail developer').find('span', class_='data').text.strip()
			self.game['players'] = product_info.find('li', class_='summary_detail product_players').find('span', class_='data').text.strip()
			self.game['rating'] = product_info.find('li', class_='summary_detail product_rating').find('span', class_='data').text.strip()
			self.game['genre'] = ', '.join([genre.text.strip() for genre in 
									product_info.find('li', class_='summary_detail product_genre').findAll('span', class_='data')])
		except:
			print('WARNING: Problem getting miscellaneous game information')
			pass

		# Get credits information
		try:	
			details_info = self.soup_details.find('div', class_='credits_list').find('tbody')
			directors = []
			writers = []
			composers = []
			for tr in details_info.findAll('tr'):
				role = tr.find('td', class_='role').text.strip()
				person = tr.find('td', class_='person').text.strip()
				if role == 'Director':
					directors.append(person)
				elif role == 'Writer':
					writers.append(person)
				elif role == 'Composer':
					composers.append(person)
			self.game['director'] = ', '.join(directors)
			self.game['writer'] = ', '.join(writers)
			self.game['composer'] = ', '.join(composers)
		except:
			print('WARNING: Problem getting credits information')
			pass

		return self.game	