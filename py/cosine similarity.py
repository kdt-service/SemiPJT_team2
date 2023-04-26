import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('./jobkorea_unique0.ky.csv')

# 데이터 전처리 및 벡터화
vectorizer = TfidfVectorizer()
# answer컬럼 데이터값을 벡터화하여 X에 저장(TF-IDF를 사용하면 단어의 중요도를 고려한 수치화 가능)
X = vectorizer.fit_transform(df['answer'])

# X의 코사인 유사도 계산
cos_sim = cosine_similarity(X)

# 유사도 임계값 설정
### 이 부분 수정 가능 ###
threshold = 0.95

# 각 answer에 대한 중복 체크 리스트
# 모든값이 True로 생성(모든 자기소개서가 중복되지 않는다는 가정)
dup_check = [True] * len(df)
#['TRUE','FALSE''TRUE''TRUE''TRUE']

for i in range(len(df)):
    # 현재 자기소개서가 중복되지 않았다면
    if dup_check[i]:
        # 비교 대상
        for j in range(i+1, len(df)):
            # 코사인 유사도 계산
            similarity = cos_sim[i, j]
            # 0.95 이상이라면
            if similarity >= threshold and df['section'][i] == df['section'][j]:
                # 중복 자기소개서로 표시함(False)로 표시
                dup_check[j] = False

# unique_df에 중복이 아닌 자기소개서만 필터링하여 데이터프레임에 저장
# 이 값으로 행을 선택
unique_df = df[pd.Series(dup_check)]
## 수정하면 파일 이름 변경! ##
unique_df.to_csv('jobkorea_unique0.95.csv', index=False, encoding='UTF-8')
