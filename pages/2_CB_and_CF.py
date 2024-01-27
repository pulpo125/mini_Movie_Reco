import streamlit as st
import pandas as pd
import pickle
from recommendation_system import cf_search_movie
from recommendation_system import cb_get_index
from recommendation_system import collaborative_filtering
from recommendation_system import content_based_filtering 

# 함수 선언
def print_cf(cf):
    st.write('- **협업 필터링 추천 영화**')
    for i in range(1, len(cf)):
        st.write(f'[{i}] {cf[i][0]} | distance: {cf[i][1]}')

def print_cb(cb):
    cb = cb.reset_index(drop=True)
    st.write('- **콘텐츠 기반 추천 영화**')
    for i in range(1, len(cb)):
        st.write(f'[{i}] {cb["title"][i]} | cosine_similarity: {cb["cosine_similarity"][i]}')

# 데이터 로드
movie_df = pd.read_csv('./data/2_movie_df.csv')
cf_df = pd.read_csv('./data/2_cf_df.csv')
cb_df = pd.read_csv('./data/2_cb_df.csv')

with open('./data/2_movie_pivot.pickle', 'rb') as f: 
    movie_pivot = pickle.load(f)
with open('./data/2_distances.pickle', 'rb') as f: 
    distances = pickle.load(f)
with open('./data/2_indices.pickle', 'rb') as f: 
    indices = pickle.load(f)
with open('./data/2_cosine_similarity_matrix.pickle', 'rb') as f: 
    cosine_similarity_matrix = pickle.load(f)

# reset idx
movie_index = 0

# Header
st.subheader("Mini Project 2")
st.title(":heart_eyes: What's your Favorite Movie?")
st.write("좋아하는 영화를 영어로 입력하고 **Enter**를 누르세요. 영화 6개를 추천해드립니다.")
st.caption("추천 검색어: Love Actually, About Time, The Conjuring, A Cinderella Story, Scream 3")

# 영화 검색
movie_name = st.text_input('좋아하는 영화 이름을 입력하세요.')

if movie_name:
    # reset index
        movie_index = {} 

        # 영화가 있으면
        if len(movie_df[movie_df['Name'] == movie_name]) == 1:
            search_movie = movie_df.loc[movie_df['Name'] == movie_name]
            if ((search_movie['cf'] == 1) & (search_movie['cb'] == 0)).values[0]:
                movie_index['cf'] = (cf_search_movie(movie_name, cf_df, movie_pivot))
            elif ((search_movie['cf'] == 0) & (search_movie['cb'] == 1)).values[0]:
                movie_index['cb'] = (cb_get_index(movie_name, cb_df))
            else:
                movie_index['cf'] = (cf_search_movie(movie_name, cf_df, movie_pivot))
                movie_index['cb'] = (cb_get_index(movie_name, cb_df))

        # 영화가 없으면        
        else:
            st.write('해당 영화가 없습니다. 다시 입력해주세요.')

# 영화 추천
if movie_index:
    # reset
    cf = 0
    cb = 0

    # 둘 다 있으면
    if len(movie_index) == 2:
        cf = collaborative_filtering(movie_index['cf'], 4, cf_df, movie_pivot, indices, distances)
        cb = content_based_filtering(cb_df, cosine_similarity_matrix, movie_index['cb'], top_n=4)
        print_cf(cf)
        print_cb(cb)

    elif 'cf' in movie_index:
        cf = collaborative_filtering(movie_index['cf'], 7, cf_df, movie_pivot, indices, distances)
        print_cf(cf)

    elif 'cb' in movie_index:
        cb = content_based_filtering(cb_df, cosine_similarity_matrix, movie_index['cb'], top_n=7)
        print_cb(cb)
else:
    st.empty()