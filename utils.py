import re
import string
import random
from difflib import SequenceMatcher
# from fuzzywuzzy import fuzz
import loader
from datetime import datetime

def clean_string(s):
	#Lowercase string
	s = s.lower()

	#Remove all spaces
	s = s.replace(' ', '')

	#Inspired by: https://bart.degoe.de/building-a-full-text-search-engine-150-lines-of-code/
	PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
	s = PUNCTUATION.sub('', s)
	# print(s)
	return s
	
# clean_string("Hello: World!!!!")

def is_invalid_date_format(date_string):
	try:
		date = datetime.strptime(date_string, "%Y-%m-%d")
		# print(date)
		return False
	except:
		return True

def get_year_from_date(date_string):
	# print(date_string)
	date = datetime.strptime(date_string, "%Y-%m-%d")
	# print(date.year)
	return date.year

# date_string = '1906-01-01'
# get_year_from_date(date_string)

def get_string_similarity(string1, string2):
	return SequenceMatcher(None, string1, string2).ratio()


countries = [
	'Portugal',
	'United Kingdom',
	'United States',
	'France',
	'Brazil',
	'China',
	'India',
]

country_flag_urls = {
	'Portugal': 'http://www.geognos.com/api/en/countries/flag/PT.png',
	'United Kingdom': 'http://www.geognos.com/api/en/countries/flag/GB.png',
	'United States': 'http://www.geognos.com/api/en/countries/flag/US.png',
	'France': 'http://www.geognos.com/api/en/countries/flag/FR.png',
	'Brazil': 'http://www.geognos.com/api/en/countries/flag/BR.png',
	'China': 'http://www.geognos.com/api/en/countries/flag/CN.png',
	'India': 'http://www.geognos.com/api/en/countries/flag/IN.png',
}
def get_country_flag_urls(countries):
	urls = []
	for country in countries:
		urls.append(country_flag_urls[country])

	return urls

# print(get_country_flag_urls(['Portugal', 'Brazil']))


#Copyright-free icons from https://img.icons8.com/ 
provider_icon_urls = {
	'Netflix': 'https://img.icons8.com/office/50/000000/no-video--v2.png',	
	'Amazon Video': 'https://img.icons8.com/material-rounded/452/video-playlist.png',	
	'HBO Max': 'https://img.icons8.com/material-outlined/50/000000/laptop-play-video.png',	
	'Youtube': 'https://img.icons8.com/ios/344/video-message.png',	
}

def get_provider_icon_urls(providers):
	urls = []
	for provider in providers:
		urls.append(provider_icon_urls[provider])

	return urls

# print(get_provider_icon_urls(['Youtube', 'HBO Max']))

providers = [
	'Netflix',
	'HBO Max',
	'Amazon Video',
	'Youtube'
]

def get_random_countries():
	global countries
	#print(countries)

	#get random number of random countries
		#choose random number
	r = random.randint(2, len(countries))	

	selected_countries = []
	for i in range(1,r):
		random_country = random.choice(countries)
		if(random_country not in selected_countries):
			selected_countries.append(random_country)

	# print(selected_countries)
	return selected_countries

def get_random_providers():
	global providers
	#print(providers)

	#get random number of random countries
		#choose random number
	r = random.randint(2, len(providers))	

	selected_providers = []
	for i in range(1,r):
		random_provider = random.choice(providers)
		if(random_provider not in selected_providers):
			selected_providers.append(random_provider)

	# print(selected_providers)
	return selected_providers

# get_random_countries()
# get_random_providers()



def get_movie_titles_from_ids(movieIds):
	print()
	movies_df = loader.load_processed_movies_locally()
	titles = []
	for movieId in movieIds:
		# print(movies_df[movies_df['movieId'] == movieId])
		# titles.append(movies_df.loc[movieId]['title'])
		# print(movies_df[movies_df['movieId'] == movieId]['title'].values[0], "with movieId: " + str(movieId))
		print(movies_df[movies_df['movieId'] == movieId]['title'].values[0])

	print()
