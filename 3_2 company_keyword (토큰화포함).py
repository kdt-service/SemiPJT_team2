import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Mecab
import warnings
warnings.filterwarnings('ignore')

class CompanyKeywords:
    def __init__(self, data_path):
        self.data_path = data_path
        self.keywords_df = pd.DataFrame(columns=['company', 'keywords', '자소서갯수'])

    # 데이터 불러오고 기업별 자소서 갯수가 10개 미만인 기업 제외
    def load_data(self):
        self.df = pd.read_csv(self.data_path)
        counts = self.df['company'].value_counts()
        under10 = counts[counts<10].index
        self.df = self.df.drop(self.df[self.df['company'].isin(under10)].index)

    # 기업별로 자기소개서 그룹화
    def group_data(self):
        self.grouped_df = self.df.groupby('company')['answer'].apply(' '.join).reset_index()
        self.content_counts = self.df['company'].value_counts().reset_index()
        self.content_counts.columns = ['company', '자소서갯수']

    # Mecab을 이용해 일반명사 추출
    def extract_nouns(self, text):
        mecab = Mecab()
        tagged = mecab.pos(text)
        return ' '.join([word for word, pos in tagged if pos == 'NNG'])

    # tf-idf을 계산하여 상위 20개의 키워드 추출
    def calculate_tfidf(self):
        self.grouped_df['nouns'] = self.grouped_df['answer'].apply(self.extract_nouns)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.grouped_df['nouns'])
        feature_names = vectorizer.get_feature_names_out()

        for idx, row in self.grouped_df.iterrows():
            company = row['company']
            tfidf_scores = tfidf_matrix[idx].toarray().flatten().tolist()
            top_20_indices = sorted(range(len(tfidf_scores)), key=lambda i: tfidf_scores[i], reverse=True)[:20]
            top_20_words = [feature_names[i] for i in top_20_indices]
            top_20_keywords = ', '.join(top_20_words)
            content_count = self.content_counts.loc[self.content_counts['company'] == company, '자소서갯수'].values[0]
            self.keywords_df = self.keywords_df.append({'company': company, 'keywords': top_20_keywords, '자소서갯수': content_count}, ignore_index=True)

    # 데이터 저장
    def save_keywords(self, output_path):
        self.keywords_df.to_csv(output_path, index=False, encoding='UTF-8')

    # 통합
    def run(self, output_path):
        self.load_data()
        self.group_data()
        self.calculate_tfidf()
        self.save_keywords(output_path)

if __name__ == "__main__":
    extractor = CompanyKeywords('csv/jobkorea_question_labeled_mecab.csv')
    extractor.run('company_keywords_top20.csv')
