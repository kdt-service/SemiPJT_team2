import pandas as pd
import re

df = pd.read_csv('./jobkorea_소제목 포함 질문 제거.csv')


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

df.to_csv('jobkorea_unique0.ky.csv', index=False, encoding='UTF-8')