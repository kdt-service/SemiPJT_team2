import pandas as pd
from konlpy.tag import Mecab

df = pd.read_csv('./jobkorea_unique0.95.csv')

# 한국어 불용어 불러오기
# 공백문자 제거하고 set으로 저장함(중복제거)
with open('stopwords-ko.txt', 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f)

# 텍스트를 입력받아 불용어 처리 후 Mecab을 사용하여 품사 태깅을 수행하는 함수
def mecab_tokenize(text, stopwords):
    Tag = []
    mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")
    tokens = mecab.morphs(text)
    # 불용어가 아닌 단어들을 태깅
    filtered_tokens = [token for token in tokens if token not in stopwords]
    for token in filtered_tokens:
        tagged_token = mecab.pos(token)
        # 'NNG', 'NNP', 'NNB', 'NR', 'VV' 태그를 가진 토큰만 추가
        # ('단어','태그')형태이므로 태그부분 참조
        Tag += [t for t in tagged_token if t[1] in ('NNG', 'NNP', 'NNB', 'NR', 'VV')]
    return Tag  # 태깅된 토큰들

# 데이터프레임에 불용어 처리된 품사 태깅 결과를 저장
df['pos'] = df['answer'].apply(lambda x: mecab_tokenize(x, stopwords))
df.to_csv('jobkorea_pos_mecab_NV_0.95.csv')
