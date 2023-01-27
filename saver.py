import pymongo
import pandas as pd
import pickle
from scipy.sparse import csr_matrix


uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']



def save_preprocessed_movies_locally(movies_df):
	try:
		directory = './processed-data/'
		filename = 'movies_processed.csv'
		movies_df.to_csv(directory+filename, index=False)
		print(f'processed movies dataframe successfully saved in {directory} as: {filename}')

	except Exception as e:
		print('An error occurred while attempting to save processed movie_df locally') 
		print(e)


def post_preprocessed_movies_to_db(movies_df):
	db.movies.delete_many({})
	# print('all movie records in movie collection deleted')

	# print("Hello from saver.py, working db upload")
	# print(movies_df.head(20))
	# print(movies_df.tail(20))
	# print(movies_df.dtypes)

	db.movies.insert_many(movies_df.to_dict('records'))
	print("inserted movies from dataset into movie collection")
	return

def save_similarity_matrix_to_db(similarity_matrix):
	print("Hello from saver.py")
	similarity_matrix.reset_index(inplace=True)
	similarity_matrix.rename(columns={'index': 'movieId'}, inplace=True)
	print("similarity_matrix")
	print(similarity_matrix)
	print(similarity_matrix.dtypes)
	print("")

	movieIds = similarity_matrix['movieId']
	columns = similarity_matrix.columns[1:].map(str)
	# print(columns)

def save_sparse_similarity_matrix_to_db(sparse_similarity_matrix):
	try:
		db.similarity_matrix.delete_many({})
		db.similarity_matrix.insert_many(sparse_similarity_matrix.to_dict('records'))
		print('similarity_matrix successfully saved in db')
	except Exception as e:
		print('Something went wrong while attempting to save similarity_matrix')
		print(e)
	pass
	

def save_similarity_matrix_locally(similarity_matrix):
	try:
		print(similarity_matrix)
		similarity_matrix.to_csv("./processed-data/similarity_matrix.csv", index=False, compression="gzip")
		# pickle.dump(similarity_matrix, open('./processed-data/similarity_matrix.dat','wb'))
		print('similarity_matrix successfully saved!')
	except Exception as e:
		print('Something went wrong while attempting to save similarity_matrix')
		print(e)
	pass
