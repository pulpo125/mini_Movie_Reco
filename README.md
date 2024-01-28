### Mini Project
# 🎥 3-Steps 영화 추천 시스템

## 📂 프로젝트 개요
- ‘3-Steps 영화 추천 시스템’은 총 3개의 영화 추천 시스템 미니 프로젝트를 종합하여 정리한 프로젝트로, 점점 발전하는 추천 시스템을 담아내고자 했습니다.

## 📚 프로젝트 내용
```
Mini 1) 규칙 기반 추천 시스템 - 오늘의 상황별 영화 추천
Mini 2) 콘텐츠 기반 필터링, 협업 필터링 - 좋아하는 영화 기반 추천
Mini 3) Matrix Factorization - 평점 기반 추천
```

## 🔨 개발 기술 스택
|Stack|사용목적|
|:---:|:---:|
|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">|프로그래밍 언어|
|<img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white">|머신러닝&딥러닝|
|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">|데이터베이스|
|<img src="https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">|웹 개발|
|<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">|프로젝트&형상 관리|

## 🙋 주요 담당 업무

### 1. Rule-based Recommendation System 개발
- 사용자의 현재 상황을 기반으로 러닝 타임 및 장르로 필터링하여 랜덤으로 영화를 추천하여 사용자에게 신선하고 다양한 영화를 제공

### 2. Hybrid Recommendation System 개발
- **협업 필터링과 콘텐츠 기반 필터링 두 가지 추천 시스템을 결합**하여 사용자에게 다양하고 정확한 영화 추천을 제공하는 시스템 구축
    - 아이템 기반 협업 필터링: KNN을 기반으로 영화를 기준으로 사용자들이 비슷한 평점을 내린 유사한 영화를 추천
    - 콘텐츠 기반 필터링: 범주형 데이터를 원 핫 인코딩을 사용하여 각 영화를 벡터 형태로 변환하고, 이러한 벡터 간의 유사성을 코사인 유사도로 계산하여 사용자에게 추천할 영화를 선별

### 3. Matrix Fatorization Recommendation System 개발
- **Tensorflow를 사용하여 사용자와 영화에 대한 embedding을 dot product로 결합하여 평점을 예측 Matrix Factorization 모델 생성**
- **Cold Start 문제 해결**: 신규 사용자에게 초기에는 가장 비슷한 평점을 매긴 사용자의 추천을 제공하며, 이후 모델 업데이트를 통해 사용자의 평점 정보가 더 쌓이면 보다 맞춤화된 추천을 제공하는 방식을 도입

## 💻 Streamlit 실행방법
1. Git 레포지터리 다운
2. mini_movie_reco/data 폴더에 구글 드라이브에 있는 ['streamlit data'](https://drive.google.com/file/d/1PTW_TQKn8R1ui3JDHmNxPpb8vG1v0fFa/view?usp=sharing) 데이터 다운받아 넣기
3. 터미널 > mini_movie_reco 위치에서 ```streamlit run Home.py``` 실행

## 📚 프로젝트 결과
![영화1](https://github.com/pulpo125/mini_Movie_Reco/assets/118874524/7eb7f9be-9c2d-4be2-a6f8-d7236d542de2)
![영화2](https://github.com/pulpo125/mini_Movie_Reco/assets/118874524/ae38723b-b544-4610-b8dd-8cc71a614dcc)
![영화3-1](https://github.com/pulpo125/mini_Movie_Reco/assets/118874524/7d85460f-43fe-44d0-a684-0d1c6c88289c)
![영화3-2](https://github.com/pulpo125/mini_Movie_Reco/assets/118874524/0ca6565f-8c4c-447c-ac18-d6f03c4f13f6)

## 👀 Insight
- **다양한 모델 적용과 발전**: 다양한 추천 시스템 모델을 구현하며 추천 시스템의 다양한 모델과 알고리즘에 대한 이해를 향상했고, 각 모델의 특징과 한계를 경험적으로 이해할 수 있었습니다.
- **협업 필터링의 한계와 극복**: Item-based Collaborative Filtering의 간단하면서도 직관적인 방식은 데이터 희소성으로 인한 한계를 가졌습니다. 이를 극복하기 위해 Matrix Factorization 알고리즘을 활용하여 행렬 분해를 통한 잠재 요인 학습으로 희소성에 대한 제한을 극복했습니다.
