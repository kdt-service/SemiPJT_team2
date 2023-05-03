import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Mecab
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Mecab을 이용해 일반명사 추출
def extract_nouns(text):
    mecab = Mecab()
    tagged = mecab.pos(text)
    return ' '.join([word for word, pos in tagged if pos == 'NNG'])

# tf-idf을 계산하여 상위 20개의 키워드 추출
def extract_keywords(text):
    nouns = extract_nouns(text) # 텍스트 명사 추출
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([nouns])    # 명사 기반 TF-IDF 행렬 생성
    feature_names = vectorizer.get_feature_names()  # 행렬에서 키워드 목록 가져오기
    tfidf_scores = tfidf_matrix.toarray().flatten().tolist()    # 행렬 1차원 리스트로 변환
    top_indices = sorted(range(len(tfidf_scores)), key=lambda i: tfidf_scores[i], reverse=True)[:20]    # 상위 20개 키워드 인덱스 구하기
    top_keywords = [feature_names[i] for i in top_indices]  # for 문 돌면서 키워드 추출
    return top_keywords

# input 자기소개서와 job_keywords.csv파일의 키워드 추출을 내용을 유사도 검사
def cosin_similarity(user_keywords, job_keywords_df):
    vectorizer = TfidfVectorizer()
    job_keywords_matrix = vectorizer.fit_transform(job_keywords_df['keywords'])     # 직무 키워드 기반 TF-IDF 행렬 생성
    
    user_keywords_str = ', '.join(user_keywords)    # input데이터 키워드 콤마구분
    user_keywords_matrix = vectorizer.transform([user_keywords_str])    # input데이터 키워드 기반 TF-IDF 행렬 생성
    
    similarity_scores = cosine_similarity(user_keywords_matrix, job_keywords_matrix)    # 행렬간 코사인 유사도 계산
    
    return similarity_scores

def top_similar_jobs(similarity_scores, job_keywords_df):
    job_keywords_df = job_keywords_df.rename(columns={'job':'직무'})
    top_indices = np.argsort(-similarity_scores.flatten())[:3]  # 유사도 점수를 내림차순으로 정렬한 인덱스 배열을 얻고 상위 3개 인덱스 선택
    top_similar_jobs = job_keywords_df.iloc[top_indices].drop(labels=['keywords', '자소서갯수'], axis=1)  # 상위 인덱스에 해당하는 행을 가져오고 불필요한 열 삭제
    top_similar_jobs.reset_index(drop=True, inplace=True)  # 인덱스를 재설정하고 원래 인덱스 삭제
    top_similar_jobs.index += 1  # 인덱스를 1부터 시작하도록 이동
    return top_similar_jobs  # 수정된 데이터프레임 반환

if __name__ == "__main__":
    user_input = input("자기소개서 내용을 입력하세요: ")
    user_keywords = extract_keywords(user_input)
    
    job_keywords_df = pd.read_csv('/home/ubuntu/workspace/SemiPJT_team2/job_keywords_top20.csv')
    similarity_scores = cosin_similarity(user_keywords, job_keywords_df)
    top_jobs = top_similar_jobs(similarity_scores, job_keywords_df)

    print(top_jobs.columns)
    print(top_jobs)
    