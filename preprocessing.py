import loader, saver
import utils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import pickle


def preprocess_movies():

	# movies_df = loader.load_original_movies_locally()
	movies_df = loader.get_movies_from_db()
	print(movies_df.columns)
	print(len(movies_df))

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.replace("|", " "))
	# print(movies_df)

	#clean movie titles
	movies_df['clean_title'] = movies_df['title'].apply(lambda x: utils.clean_string(x))
	# print(movies_df)

	#countries
	movies_df['countries'] = movies_df['title'].apply(lambda x: utils.get_random_countries())
	# print(movies_df)

	movies_df['country_flag_urls'] = movies_df['countries'].apply(lambda x: utils.get_country_flag_urls(x))
	# print(movies_df[['countries', 'country_flag_urls']])

	#providers	
	movies_df['providers'] = movies_df['title'].apply(lambda x: utils.get_random_providers())
	# print(movies_df)

	movies_df['provider_icon_urls'] = movies_df['providers'].apply(lambda x: utils.get_provider_icon_urls(x))
	# print(movies_df[['providers', 'provider_icon_urls']])


	#Inspired by: https://medium.com/geekculture/creating-content-based-movie-recommender-with-python-7f7d1b739c63
	movies_df['genres'] = movies_df['genres'].str.replace('Sci-Fi', "SciFi")
	movies_df['genres'] = movies_df['genres'].str.replace('Film-Noir', "FilmNoir")

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.split())
	# print(movies_df['genres'])

	movies_df.drop_duplicates(subset='title', inplace=True)
	print(len(movies_df))

	movies_df['movieId'] = range(0, len(movies_df))
	# print("No. movies in dataset: ", len(movies_df))
	# print(movies_df.tail(20))

	#save locally and to database		
	saver.save_preprocessed_movies_locally(movies_df)
	saver.post_preprocessed_movies_to_db(movies_df)
	
	return


def compute_similarity_matrix():
	np.set_printoptions(threshold=np.inf)

	movies_df = loader.load_processed_movies_locally()
	print(movies_df)

	features = movies_df[['movieId','genres']]
	features['genres'] = features['genres'].apply(lambda x: ''.join(x))

	#Inspired by: https://medium.com/geekculture/creating-content-based-movie-recommender-with-python-7f7d1b739c63
	tfidf = TfidfVectorizer(stop_words='english')
	#each movie will get 21 columns, each value representing the 'weight'
		# of the feature (in this case genre) on describing the dataset.
	tfidf_matrix = tfidf.fit_transform(features['genres'])

	similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
	movieIds = movies_df['movieId'].values
	similarity_matrix = pd.DataFrame(data=similarity_matrix, columns=movieIds, index=movieIds)
	print(similarity_matrix)

	#create df with columns "movieId" and "similarity_row" containing a dict with sparse similarities
	similarity_matrix.reset_index(inplace=True)
	similarity_matrix.rename(columns={'index': 'movieId'}, inplace=True)
	print("similarity_matrix")
	print(similarity_matrix)
	# print(similarity_matrix.dtypes)
	# print("")

	sparse_similarity_matrix = pd.DataFrame()
	sparse_similarity_matrix['movieId'] = similarity_matrix['movieId']
	# result = json.dumps(recommended_movieIds.tolist())
	# sparse_similarity_matrix['similarity_row'] = similarity_matrix.apply(lambda row: json.dumps(dict(csr_matrix(row).todok().items())), axis=1)
	sparse_similarity_matrix['similarity_row'] = similarity_matrix.apply(lambda row: pickle.dumps(csr_matrix(row)), axis=1)
	print(sparse_similarity_matrix)
	print(sparse_similarity_matrix.dtypes)
	print()


	# saver.save_sparse_similarity_matrix_locally(sparse_similarity_matrix)
	saver.save_sparse_similarity_matrix_to_db(sparse_similarity_matrix)
	return

def explore_datasets():

	big_movies_df = pd.read_csv('./input/big_dataset/movies_metadata.csv')
	big_movies_df = big_movies_df[['title', 'release_date','genres', 'overview']]

	#count number of records with NaN release_date
	# is_nan_release_date = big_movies_df['release_date'].isna()
	# num_nan_release_date = is_nan_release_date.sum()
	# print(is_nan_release_date)
	# movies_with_nan_release_date = big_movies_df[is_nan_release_date]['title'].values
	# print(movies_with_nan_release_date)

	#filter out records which do not have a release date
	is_not_nan_release_date = big_movies_df['release_date'].notna()
	filtered_big_movies_df = big_movies_df[is_not_nan_release_date]
	# print(filtered_big_movies_df)

	#filter out records with invalid release dates
	invalid_dates = filtered_big_movies_df['release_date'].apply(utils.is_invalid_date_format)
	records_with_invalid_dates = filtered_big_movies_df[invalid_dates]
	print("Number of records with invalid dates in big movies",records_with_invalid_dates.sum())
	filtered_big_movies_df = filtered_big_movies_df[~invalid_dates]

	#extract year from 'release_date'
	filtered_big_movies_df['year'] = filtered_big_movies_df['release_date'].apply(utils.get_year_from_date)

	#get clean_title so we can merge with small movies dataset
	filtered_big_movies_df['clean_title'] = filtered_big_movies_df.apply(lambda row: utils.clean_string(row['title']) + str(row['year']), axis=1)

	#drop duplicates
	filtered_big_movies_df.drop_duplicates(subset='title', inplace=True)

	#import small dataset so we can merge
	small_processed_movies_df = loader.load_processed_movies_locally()
	print(small_processed_movies_df.shape)
	print('Number of NaN in big movies overview column: ' + str(filtered_big_movies_df['overview'].isna().sum()))
	print(small_processed_movies_df.shape)

	#merge
	merged_df = small_processed_movies_df.merge(filtered_big_movies_df[['overview','year','clean_title']], how='left', left_on='clean_title', right_on='clean_title')
	merged_df.drop_duplicates(inplace=True)
	print("Number of NaN in merged movies overview column: " + str(merged_df['overview'].isna().sum()))

	print(merged_df.shape)


preprocess_movies()
# explore_datasets()
# compute_similarity_matrix()