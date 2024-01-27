import streamlit as st
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/1_IMBD_eda.csv')

# Sidebar_1) how to use
with st.sidebar:
    st.subheader("How to use")
    st.markdown("""<span style='color:grey'>IMDB Top 250 영화 데이터를 이용하여<span/><br/>
    <span>년도별, 장르별, 감독별로 순위에<span/><br/>
    <span>가장 많이 랭킹된 Top 5를 분석합니다.:smile:<span/><br/>
    <span>컬럼을 선택하고 자세히 보고 싶은 데이터를 선택한 후<span/><br/>
    <span>상세정보가 궁금한 영화의 순위를 검색창에 입력해주세요.<span/><br/>
    <hr style='margin: 0px; border-bottom: 3px dashed rgba(49, 51, 63, 0.2);'>""", unsafe_allow_html=True)

# Sidebar_2) 컬럼 selectbox 생성
with st.sidebar:
    group_by_option = st.selectbox('컬럼을 선택하세요: ', ['None'] + ['year'] + ['genre'] + ['director_name'])


# Main) Title
st.subheader("Mini Project")
st.title(':movie_camera: 3-Steps 영화 추천 시스템')
st.markdown('''
            3개의 미니프로젝트를 담아 점점 발전하는 추천 시스템을 경험할 수 있습니다.  
            왼쪽 사이드바에서 원하는 추천 시스템을 선택하세요!
            ''')
st.markdown('''
            **Step 1) 규칙 기반 추천 시스템  
            Step 2) 콘텐츠 기반 필터링과 협업 필터링 추천 시스템  
            Step 3) Matrix Factorization 추천 시스템**
            ''')

st.divider()

st.subheader(':bar_chart: IMDB Top 250 Movies Analysis')
# Main) 컬럼별 Top 5
selected_data = 'None'
if group_by_option == 'None':
    ## 컬럼을 선택하지 않으면 전체 데이터 보여주기
    main_df = df[['title', 'imbd_votes', 'imbd_rating']]

    ## 데이터프레임 인덱스 rank로 변환
    main_df.index=main_df.index+1     # 인덱스 + 1 = rank
    main_df.index.name = 'rank'                              
    st.dataframe(main_df, width=700)

else:
    ## 컬럼을 선택하면 Top 5 그래프 생성
    st.subheader(f'{group_by_option}별 가장 많이 랭킹된 Top 5')
    selected_column_df = df[group_by_option].value_counts()[:5].reset_index()       ## Top 5 추출
    selected_column_df = pd.DataFrame(selected_column_df).rename(columns={group_by_option:'count', 'index':group_by_option})
    st.bar_chart(selected_column_df, x = group_by_option, y = 'count')  # 차트 생성

    ## 선택한 컬럼 리스트 형태로 저장
    group_list = selected_column_df[group_by_option].to_list()

    # Sidebar_3) 데이터 selectbox 생성
    with st.sidebar:
        selected_data = st.selectbox('데이터를 선택해주세요: ', ['None'] + list(group_list))

# Main) 컬럼 선택 후 데이터 보여주기
if selected_data == 'None':
    ## 데이터를 선택하지 않으면 공간 비워두기
    st.empty()

else:
    ## 데이터를 선택하면 해당 데이터셋 보여주기
    st.subheader(f'{selected_data}의 데이터셋')
    tmp_df = df[df[group_by_option].isin([selected_data])][['title', 'imbd_votes', 'imbd_rating']]
    tmp_df.index = tmp_df.index+1
    tmp_df.index.name = 'rank'
    st.dataframe(tmp_df, width=700)

# Sidebar_3) 검색: 랭킹 입력 - 링크 아웃풋
with st.sidebar:
    st.markdown("<hr style='margin: 0px; border-bottom: 3px dashed rgba(49, 51, 63, 0.2);'>", unsafe_allow_html=True)
    idx = st.text_input('검색하고 싶은 순위(rank)를 입력해주세요.')
    if idx:
        st.write(df.loc[int(idx)-1]['link'])

    else:
        st.empty()


# Main) 깃허브 링크
'''
    [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/pulpo125/habang/tree/develop/movie_pj) 

'''
st.markdown("<br>",unsafe_allow_html=True)