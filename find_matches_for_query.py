try: 
    # import os
    # curr_dir = os.path.abspath(__file__ + "/..")
    # # print(curr_dir)
    import sys
    # sys.path.append('/app/recommendation-system')

    import json
    # from curr_dir import utils
    # from curr_dir import loader
    # from utils import clean_string, get_string_similarity
    # from loader import get_processed_movies_from_db
    import utils
    import loader


    def find_movieIds_from_closest_titles_to(query, n):
        # movies_df = loader.load_processed_movies_locally()
        movies_df = loader.load_processed_movies_from_db()
        # print(movies_df.head())
        # print(movies_df['title'])
        # print(movies_df['clean_title'])

        clean_query = utils.clean_string(query)
        # # print(clean_query)

        movies_df['similarity_to_query'] = movies_df['clean_title'].apply(
            lambda clean_title: utils.get_string_similarity(clean_title, clean_query))
        # print(movies_df['similarity_to_query'])

        # sort
        movies_df.sort_values(by='similarity_to_query',
                              ascending=False, axis=0, inplace=True)
        # print(movies_df)

        # no matches found
        if movies_df['similarity_to_query'].iloc[0] < 0.7:
            print(json.dumps([]))
        else:
            # Get top n values
            top_movieIds = movies_df['movieId'][:n].values
            # print(movies_df['similarity_to_query'][:n])

            # utils.get_movie_titles_from_ids(top_movieIds)
            # results = top_movieIds.tolist()
            # print(results)

            print(json.dumps(top_movieIds.tolist()))


    # result = find_movieIds_from_closest_titles_to('iron man', 5)
    # print(result)
    query = str(sys.argv[1])
    n = int(sys.argv[2])
    find_movieIds_from_closest_titles_to(query, n)

except Exception as e:
    print(e)
