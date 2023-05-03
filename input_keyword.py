import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Mecab
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class KeywordExtractor:
    def __init__(self):
        self.mecab = Mecab(dicpath=r"/tmp/mecab-ko-dic-2.1.1-20180720")
        self.vectorizer = TfidfVectorizer()

    def extract_nouns(self, text):
        tagged = self.mecab.pos(text)
        return ' '.join([word for word, pos in tagged if pos == 'NNG'])

    def extract_keywords(self, text):
        nouns = self.extract_nouns(text) # 텍스트 명사 추출
        tfidf_matrix = self.vectorizer.fit_transform([nouns])    # 명사 기반 TF-IDF 행렬 생성
        feature_names = self.vectorizer.get_feature_names()  # 행렬에서 키워드 목록 가져오기
        tfidf_scores = tfidf_matrix.toarray().flatten().tolist()    # 행렬 1차원 리스트로 변환
        top_indices = sorted(range(len(tfidf_scores)), key=lambda i: tfidf_scores[i], reverse=True)[:20]    # 상위 20개 키워드 인덱스 구하기
        top_keywords = [feature_names[i] for i in top_indices]  # for 문 돌면서 키워드 추출
        return top_keywords


if __name__ == "__main__":
    extractor = KeywordExtractor()
    text = input("텍스트를 입력하세요: ")
    top_keywords = extractor.extract_keywords(text)
    print(top_keywords)