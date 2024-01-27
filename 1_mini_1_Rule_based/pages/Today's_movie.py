import streamlit as st
import pandas as pd

# 데이터 로드
df = pd.read_csv('../data/1_IMBD_top250_eda.csv')


## Sidebar
# How to use
with st.sidebar:
    st.subheader("How to use")
    st.markdown("""<span style='color:grey'>오늘은 또 어떤 영화를 감상해야 할지 고민인 당신!<span/><br/>
    <span>지금 당신의 상황을 입력해주세요.:smile:<span/><br/>
    <span>IMDB TOP 250 영화 데이터를 기반으로 추천해드립니다.<span/><br/>
    <hr style='margin: 0px; border-bottom: 3px dashed rgba(49, 51, 63, 0.2);'>""", unsafe_allow_html=True)


# 질문 1: 시간 관련
with st.sidebar:
    st.subheader('Question')
    hour = st.radio(
        'Q1. 얼마나 시간이 있나요?',
        ['1시간 정도 있어요', '영화는 2시간 이상이 기본이죠']
    )


# 시간 선택에 따른 데이터셋 추출
if hour == '1시간 정도 있어요':
    running_time = '1h'
else: 
    running_time = '2h|3h'

duration_contains = df['duration'].str.contains(running_time)
df_duration = df[duration_contains]


# 질문 2: 장르 관련
genre_dic = {'웃고 싶은 날':'Comedy', '울고 싶은 날':'Drama', '가족과 함께하는 날':'Family', '상상의 나라로 고고':'Sci-Fi', '연애 하고 싶은 날':'Romance',
             '동심의 세계로 고고':'Animation'}

with st.sidebar:
    what_day_lst = st.multiselect('Q2. 오늘은 어떤 날인가요? (2개 이상 선택해주세요.)', ['웃고 싶은 날', '울고 싶은 날', '가족과 함께하는 날',
                                                       '상상의 나라로 고고', '연애 하고 싶은 날', '동심의 세계로 고고'])
    
try:
    # 장르 선택에 따른 데이터셋 추출
    if what_day_lst:
        genre_lst = []
        for genre in what_day_lst:
            genre_lst.append(genre_dic.get(genre))

        genre_contains = df['genre'].str.contains("|".join(genre_lst))
        df_genre = df[genre_contains]

    else:
        # 비교를 위해 임시로 df_genre를 만듦
        df_genre = pd.DataFrame({'tmp': [0,0]})

    ## Main
    # Title
    st.title(':thinking_face:오늘의 영화는?')
    
    ## 추천 결과
    if len(df_genre) == 2:
        # 장르 선택을 하지 않으면 빈칸
        st.subheader("사이드바에 있는 질문에 답해주세요.")
    else:
        # 데이터 프레임 합치기
        df_result = pd.concat([df_duration, df_genre])

        # 랜덤으로 하나만 추출
        movie_recommendation = df_result.sample(n=1)
        idx = int(list(movie_recommendation.index)[0])

        # 추천 영화 info
        st.markdown("""<style>
        span.info_name{font-size: 20px; font-weight: bold; }
        p{color: black; display:inline; font-size: 17px; margin-bottom:3px;}
        div.box{ background-color:rgba(255, 228, 0, 0.4); padding:20px;}
        <style/>
        """, unsafe_allow_html=True)
        
        st.header("'"+df_duration.loc[int(idx)]['title'] + "' 입니다.")
        st.markdown(f"""<div class='box'>
            <span class="info_name">장르)  <p>{df_duration.loc[int(idx)]['genre']}<p/><span/><br/>
            <span class="info_name">러닝타임)  <p>{df_duration.loc[int(idx)]['duration']}<p/><span/><br/>
            <span class="info_name">감독)  <p>{df_duration.loc[int(idx)]['director_name']}<p/><span/><br/>
            <span class="info_name">작가)  <p>{df_duration.loc[int(idx)]['writer_name']}<p/><span/><br/>
            <span class="info_name">줄거리)<br/><p>{df_duration.loc[int(idx)]['storyline']}<p/><span/><br/>
            <span class="info_name"><a href="{df_duration.loc[int(idx)]['link']}">Go to Detailed Information!</a><span/>
        <div/>""", unsafe_allow_html=True)
except:
    st.empty()