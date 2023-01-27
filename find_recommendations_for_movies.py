import pickle
import json
import numpy as np
from scipy.sparse import csr_matrix
import loader
import utils
import sys
print("Hello World!")
# import os
# curr_dir = os.path.abspath(".")
sys.path.append('/app/recommendation-system')

# from curr_dir import utils
# from curr_dir import loader


def predict_similarity_matrix(matched_movieIds):
    # Load similarity matrix where the values are the similarity score, and the columns/index are the movieId
    # similarity_matrix = loader.load_similarity_matrix_locally()
    # print(similarity_matrix)

    movieId = matched_movieIds[0]

    # load sparse row in string format from database
    similarity_row = loader.load_movie_similarity_row_from_db(movieId)

    # #remove records in matched_movieIds, so we don't get recommendation results
    # 	#which have already been found in the search task
    filtered_row = similarity_row[~similarity_row.index.isin(matched_movieIds)]

    sorted_row = filtered_row.sort_values(ascending=False)
    recommended_movieIds = sorted_row[:24-len(matched_movieIds)].index

    result = json.dumps(recommended_movieIds.tolist())
    print(result)

    # utils.get_movie_titles_from_ids(recommended_movieIds)


matched_movieIds = json.loads(sys.argv[1])

predict_similarity_matrix(matched_movieIds)
