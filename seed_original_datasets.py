import pandas as pd
import pymongo
import pickle

#original movies
original_movies = pd.read_csv('./input/small_dataset/movies.csv')
#original ratings
original_ratings = pd.read_csv('./input/small_dataset/ratings.csv')


#pymongo
uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']

#seed original movies
db.original_movies.delete_many({})
db.original_movies.create_index('movieId')
db.original_movies.insert_many(original_movies.to_dict('records'))
print("original movies saved in database")

#seed original ratings
db.original_ratings.delete_many({})
db.original_ratings.insert_many(original_ratings.to_dict('records'))
print("original ratings saved in database")