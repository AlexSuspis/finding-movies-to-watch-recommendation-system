import pandas as pd
import pymongo
import loader


uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']




ratings_df = loader.get_ratings_from_db()
print(ratings_df)

#Preprocess data

#Get a dataframe with movieIds as index, and userIds as each column. Values are 
final_df = ratings_df.pivot(index = 'movieId', columns='userId', values='rating')

#1) Null/missing values	
final_df.fillna(0, inplace=True)
# print(final_df)

#Count number of ratings each movie got
no_ratings_per_movie = ratings_df.groupby('movieId')['rating'].agg('count')
# print(no_ratings_per_movie)

#2) Discard movies with too few user ratings
filter_movies_with_low_amount_ratings = no_ratings_per_movie > 50

final_df = final_df.loc[filter_movies_with_low_amount_ratings,:]
#3) Discard users with too few rated movies

#Count number of movies each user rated
no_movies_rated_per_user = ratings_df.groupby('userId')['rating'].agg('count')
# print(no_movies_rated_per_user)

filter_users_with_low_amount_ratings = no_movies_rated_per_user > 50
# print(filter_users_with_low_amount_ratings)

final_df = final_df.loc[:,filter_users_with_low_amount_ratings]
print(final_df)




#Create Knn model
from sklearn.neighbors import NearestNeighbors
knn_model = NearestNeighbors(n_neighbors=11, algorithm='ball_tree')
knn_model.fit(final_df)
print(knn_model)


#Save model

import pickle

def save_model_in_database():
	db.models.delete_many({})

	encoded_knn_model = pickle.dumps(knn_model)
	# print(encoded_knn_model)

	db.models.insert_one({'name': 'knn-model','model': encoded_knn_model})
	print("Knn model inserted into database!")


def save_model_locally():
	# save knn model with pickle
	# https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
	path = './recommendation-models/knn_model.sav'
	pickle.dump(knn_model, open(path, 'wb'))
	print('knn_model saved to current directory!')

	#save final_df with pickle
	#https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
	path = './processed-data/final_df.csv'

	# pickle.dump(final_df.to_csv, open(filename, 'wb'))
	final_df.to_csv('final_df.csv')
	print('final_df saved to current directory!')




save_model_in_database()
save_model_locally()
