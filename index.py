from bottle import app, route, run, template
import loader
import json
import utils
import numpy as np
from bottle_cors_plugin import cors_plugin

# Connect to database
db = loader.getDatabase()


@route('/')
def index():
    print("hi")
    return("Hello world")

# Find matches for query


@route('/matches/<query>/<n>')
def index(query, n):
    print("query is:", query)
    try:

        n = int(n)
        movies_df = loader.load_processed_movies_from_db()

        clean_query = utils.clean_string(query)

        movies_df['similarity_to_query'] = movies_df['clean_title'].apply(
            lambda clean_title: utils.get_string_similarity(clean_title, clean_query))
        # print(movies_df['similarity_to_query'])

        # sort
        movies_df.sort_values(by='similarity_to_query',
                              ascending=False, axis=0, inplace=True)
        # print(movies_df)

        # no matches found
        if movies_df['similarity_to_query'].iloc[0] < 0.7:
            return(json.dumps([]))
        else:
            # Get top n values
            top_movieIds = movies_df['movieId'][:n].values
            # print(movies_df['similarity_to_query'][:n])

            # utils.get_movie_titles_from_ids(top_movieIds)
            # results = top_movieIds.tolist()
            # print(results)

            return(json.dumps(top_movieIds.tolist()))

    except Exception as e:
        print("error:", e)
        return(e.json())


@route('/recommendations/<matched_movieIds>')
def index(matched_movieIds):

    # Load similarity matrix where the values are the similarity score, and the columns/index are the movieId
    # similarity_matrix = loader.load_similarity_matrix_locally()
    # print(similarity_matrix)
    matched_movieIds = json.loads(matched_movieIds)

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

    return result


# Configure server
app = app()
app.install(cors_plugin('*'))

run(host='0.0.0.0', port=3000)
