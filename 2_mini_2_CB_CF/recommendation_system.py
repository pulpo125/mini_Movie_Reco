# Collaborative Filtering

def cf_search_movie(name, cf_df, movie_pivot):
    import numpy as np
    search_movie_id = cf_df.loc[cf_df['Name'] == name, 'Movie_ID'].unique()[0]
    index = np.where(movie_pivot.index == search_movie_id)[0][0]
    return index

def collaborative_filtering(index, n, cf_df, movie_pivot, indices, distances):
    result_list = []
    for i in range(n):
        movie_name = cf_df.loc[cf_df['Movie_ID'] == movie_pivot.index[indices[index][i]], 'Name'].values[0] # movie_df
        distance = '{:.3f}'.format(distances[index][i])
        result_list.append([movie_name, distance])
    return result_list


def cb_get_index(title, cb_df):
    index = cb_df.index[cb_df['title'] == title][0]
    return index


def content_based_filtering(cb_df, cosine_similarity_matrix, idx, top_n=10):
    cb_df['cosine_similarity'] = cosine_similarity_matrix[idx]
    return cb_df.sort_values(by='cosine_similarity', ascending=False)[:top_n]