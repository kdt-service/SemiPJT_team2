import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_and_remove_duplicates(input_file, output_file, threshold=0.95):
    df = pd.read_csv(input_file)
    df.drop(df.index[28636: 28638],inplace=True) #28636~28638
    df.drop(df.index[27273],inplace= True)
    df.drop(df.index[26109 :26114],inplace=True) #26109 ~26113
    df.drop(df.index[25158 : 25160],inplace=True) #25158 ~25159
    df.drop(df.index[25011:25015],inplace=True) #25011 ~25014
    df.drop(df.index[22693:22696],inplace=True) #22693 ~22695
    df.drop(df.index[21204:21207],inplace=True) #21204 ~21206
    df.drop(df.index[19898:19902],inplace=True) #19898~19901
    df.drop(df.index[16941],inplace= True)
    df.drop(df.index[16927:16931],inplace=True) #16927~16930
    df.drop(df.index[16894:16898],inplace=True) #16894~16897
    df.drop(df.index[16581:16585],inplace=True) #16581~16584
    df.drop(df.index[16305],inplace= True)
    df.drop(df.index[16128:16130],inplace=True) #16128~16129
    df.drop(df.index[13519],inplace= True)
    df.drop(df.index[9580:9582],inplace=True) #9580~9581
    df.drop(df.index[9087:9090],inplace=True) #9087~9089
    df.drop(df.index[7915:7917],inplace=True) # 7915~7916
    df.drop(df.index[7497:7500],inplace=True) # 7497~7499
    df.drop(df.index[6644],inplace= True)
    df.drop(df.index[1526],inplace= True)
    df.drop(df.index[1207:1210],inplace=True) #1207~1209
    df.drop(df.index[1179:1186],inplace=True) # 1179, 1180, 1181, 1182, 1183, 1184, 1185 삭제
    
    df['question']=df['question'].map(lambda x:re.sub('  +', ' ', str(x)))
    df['answer']=df['answer'].map(lambda x:re.sub('  +', ' ', str(x)))
    # question 칼럼 전처리
    # 1. (400자 이내)와 같이 글자수 지정 내용 지우기!
    df['question']=df['question'].map(lambda x:re.sub('\(\d*,?\d*자 ?이내\)', '', str(x)))
    # 2. [400자 이내]와 같이 글자수 지정 내용 지우기!
    df['question']=df['question'].map(lambda x:re.sub('\[\d*,?\d*자 ?이내\]', '', str(x)))
    # 3. (600자)와 같이 글자수 지정 내용 지우기!
    df['question']=df['question'].map(lambda x:re.sub('\(\d+자.*\)', '', str(x)))
    # 4. (최소 100자, 최대 500자 입력가능)와 같이 글자수 지정 내용 지우기!
    df['question']=df['question'].map(lambda x:re.sub('\(.+\d자.+\d자.*\)', '', str(x)))
    # 5. [ 50자 이상 1000자 이내] 와 같이 글자수 지정 내용 지우기!
    df['question']=df['question'].map(lambda x:re.sub('\[.+\d자.+\d자.*\]', '', str(x)))
    # 6. (1200Byte) 와 같이 Byte 수 내용 지우기
    df['question']=df['question'].map(lambda x:re.sub('\(\d+,?\d+Byte\)', '', str(x)))


    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['answer'])
    cos_sim = cosine_similarity(X)

    dup_check = [True] * len(df)

    for i in range(len(df)):
        if dup_check[i]:
            for j in range(i+1, len(df)):
                similarity = cos_sim[i, j]
                if similarity >= threshold and df['section'][i] == df['section'][j]:
                    dup_check[j] = False

    unique_df = df[pd.Series(dup_check)]
    unique_df.to_csv(output_file, index=False, encoding='UTF-8')

input_file = 'jobkorea.csv'
output_file = 'jobkorea_unique0.95.csv'

preprocess_and_remove_duplicates(input_file, output_file, threshold=0.95)
