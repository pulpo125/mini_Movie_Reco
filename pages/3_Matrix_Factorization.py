import streamlit as st
import pandas as pd
import time
import os.path
import pickle as pkle
from streamlit_js_eval import streamlit_js_eval
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from top_rating import get_top_idx, get_top_movies
from recommendation import compute_scores, user_recommendations

# mysql 연동
# conn = pymysql.connect(host='127.0.0.1'
#                 , port=3306
#                 , user = 'root'
#                 , password='root1234'
#                 , db = 'movie_pj'
#                 , charset='utf8'
#                 ) 

# cursor = conn.cursor()

# user data load
user_df = pd.read_csv("./data/3_users.csv")

# multi page 구현
pages=['user','user_rating','recommendation']
if os.path.isfile('next.p'):
    next_clicked = pkle.load(open('next.p', 'rb'))
    print('next_clicked:', next_clicked)

choice = st.sidebar.radio("Pages",('user','user_rating', 'recommendation'), index=next_clicked)
pkle.dump(pages.index(choice), open('next.p', 'wb'))

#--------------------------------------------------------------------------------------------------#
# user 페이지
if choice=='user':

    # header
    st.subheader("Mini Project 3")
    st.title('당신의 오늘 영화는 어떤 것입니까?')
    st.subheader('당신의 영화를 추천해드립니다 정보를 입력하세요!')

    # sign up
    # 유저 정보 입력
    name=st.text_input("당신의 이름을 입력하세요")
    age=st.text_input("당신의 나이를 입력하세요(만나이기준)")
    st.write("당신의 성별을 입력하세요")
    pick=['M','F']
    status=st.radio('성별',pick)
    if status==pick[0]: 
        sex=pick[0]
    elif status==pick[1]:
        sex=pick[1]
    oc=st.text_input("당신의 직업을 입력해주세요")

    button_state = st.button("제출")

    # 제출 버튼을 누르면 DB에 회원정보 등록 및 다음 페이지로 넘어감
    if button_state:
        # sql=f'Insert into users(user_id,age,sex,occupation) values((select max(a.user_id)+1 from users a), {int(age)}, "{sex}", "{oc}");'
        # cursor.execute(sql)
        # conn.commit()
        new_idx = user_df.shape[0]
        new_user = {'user_id' : new_idx, 'age' : age, 'sex' : sex, 'occupation': oc}
        user_df = user_df.append(new_user, ignore_index=True)
        user_df.to_csv('./data/3_new_users.csv', index=False)
        st.text('데이터가 반영이 되었습니다. 다음 페이지로 넘어갑니다.')
        time.sleep(2)

        choice = 'user_rating'
        pkle.dump(pages.index(choice), open('next.p', 'wb'))
        print('버튼 한 번 클릭')
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

#--------------------------------------------------------------------------------------------------#    
# user_rating 페이지
elif choice=='user_rating':

    # DB
    # cursor = conn.cursor()
    # rating data load
    rating_df = pd.read_csv("./data/3_ratings.csv")
    # new user id 
    new_user_df = pd.read_csv("./data/3_new_users.csv")
    new_user_idx = user_df.shape[0]

    # movielens table
    movielens = pd.read_csv('./data/3_movielens.csv')

    # header
    st.title('환영합니다!')
    st.subheader('좋아하는 :red[영화]를 선택한 후 :red[평점]을 남겨주세요. :smile:')

    # contents
    # info
    st.write('**1(나쁨)~5(좋음) 사이로 평점을 입력해주세요.**')
    st.write("**총 10개 이상의 영화를 평가해야 좋은 추천을 받을 수 있습니다.**")

    # 좋아하는 영화 선택
    top_movie_id = get_top_idx(movielens)
    top_rating_movies = get_top_movies(movielens, top_movie_id)
    favorite_movies = st.multiselect('좋아하는 영화를 선택해주세요.', top_rating_movies)
    rating_list = []
    for i in range(len(favorite_movies)):
        rating = st.slider(f'{favorite_movies[i]}의 평점을 입력해주세요.', 0, 5)
        rating_list.append(rating)

    rating_cnt = len(rating_list) - rating_list.count(0)

    if rating_cnt == 0:
        btn_state = st.button('제출', disabled=True)
    else:
        btn_state = st.button('제출', disabled=False)

    ## db insert
    if btn_state:
        # user_rating 
        user_rating_dic = list(zip(top_movie_id, rating_list))
        user_rating_df = pd.DataFrame(user_rating_dic)
        user_rating_df.columns = ['movie_id', 'rating']
        id = [new_user_idx for i in range(len(user_rating_dic))]
        user_rating_df['user_id'] = id

        new_rating_df = pd.concat([rating_df, user_rating_df], ignore_index=True)
        new_rating_df.to_csv('./data/3_new_ratings.csv', index=False)

        # db ratings 테이블에 insert
        # for i in range(len(user_rating_dic)):
            # cursor.execute(f"INSERT INTO ratings (user_id, movie_id, rating) VALUES \
            #        ((select max(a.user_id) from users a), {user_rating_dic[i][0]}, {user_rating_dic[i][1]});") 
        
        # conn.commit()
        st.text('데이터가 반영이 되었습니다. 다음 페이지로 넘어갑니다.')
        import time
        time.sleep(2)

        choice = 'recommendation'
        pkle.dump(pages.index(choice), open('next.p', 'wb'))
        print('버튼 한 번 클릭')
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

#--------------------------------------------------------------------------------------------------#    
# recommendation 페이지
elif choice=='recommendation':

    # Data Load
    # movies_sql = 'SELECT * FROM movies'
    # movies = pd.read_sql(movies_sql, conn)
    # ratings_sql = 'SELECT * FROM ratings'
    # ratings = pd.read_sql(ratings_sql, conn)
    movies = pd.read_csv("./data/3_movies.csv")
    ratings = pd.read_csv("./data/3_new_ratings.csv")

    # new user id 
    new_user_df = pd.read_csv("./data/3_new_users.csv")
    user_id = user_df.shape[0]


    # user_id
    # cursor = conn.cursor()
    # cursor.execute('select max(a.user_id) from users a')
    # idx = cursor.fetchall()
    # user_id = idx[0][0] # ((365,))

    # similar
    pvt=ratings.pivot_table(index='user_id',columns='movie_id',values='rating').fillna(0)
    cos_sim=cosine_similarity(pvt,pvt)
    cos_sim_df=pd.DataFrame(data=cos_sim)

    similar_user_id = cos_sim_df[user_id].sort_values(ascending=False).index[1]

    # CFModel
    CFModel03 = tf.keras.models.load_model('./data/3_CFModel03.h5', compile=False)
    CFModel03.embeddings = {
        'user_id': CFModel03.get_layer('user_embedding').weights[0].numpy(), # U (943, 30)
        'movie_id': CFModel03.get_layer('movie_embedding').weights[0].numpy() # V (1682, 30)
    }

    # recommendation
    # 새로운 유저이면 비슷한 유저의 결과를 보여줌
    st.title('추천 결과입니다. :smile:')
    similar_result = user_recommendations(CFModel03, movies, ratings, k=10, user_id=similar_user_id, exclude_rated=True)
    st.dataframe(similar_result)

    # 기존 유저
    # user_result = user_recommendations(CFModel03, movies, ratings, k=10, user_id=user_id, exclude_rated=True)
    # st.write(f'유저 결과: {user_id}')
    # st.dataframe(user_result)

# conn.commit()
# conn.close()