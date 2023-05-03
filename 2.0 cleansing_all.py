import pandas as pd
import numpy as np
import re
df=pd.read_csv('/home/ubuntu/workspace/SemiPJT_team2/jobkorea.csv')

# 1. Question에 소제목인 경우
# 코드 순서 변경 하면 안됩니다! # crawling 파일에 따라 인덱스 수정해줘야 합니다!! 
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

# 2. question 컬럼에 글자수 관련된 내용 정규표현식 활용하여 지우기
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

# 3. 문항 구분
df.dropna(subset=['question'], inplace=True) # question 정규표현식 활용하다가 공백생기는 경우 발생. 
df.reset_index(drop=True, inplace=True) # 이 경우 null인지 확인해서 없애기 진행 후 인덱스 다시 붙이기! 

keywords = ['희망', '입사', '이유', '지원', '동기', 
            '지원동기', '지원 동기', '기준', '일하고 싶은', 
            '해보고 싶은']
df['지원동기'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0 )

keywords = ['비전', '비젼','기여', '포부', '입사후 포부', 
            '목표', '어떤 일','발전 방향', '10년', '5년', 
            '입사 후', '계획', '희망직무', '시나리오', '공헌']
df['입사 후 포부'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['살아오면서', '학창생활', '학창 시절', '학창생활', 
            '생활 신조','살아오면서', '대학생활', '학창시절', 
            '가족', '영향을 끼친', '생활신조', '본인', '슬로건', 
            '성장과정', '성장배경', '존경', '가치관', '기억에 남는', '성장배경', '성장', '좌우명', '성장 과정']
df['성장과정'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['장,단점', '장.단점', '장/단점', '보완점', '강약점', 
            '성격', '강점', '장점' , '장단점', '성향']
df['성격 장단점'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['전공 과목', '전공과목', '수강', '능력', '전공', '기술', 
            '직무', '준비', '역량', '지식', '재능', '노력', '경쟁력', 
            '경력', '이력', '내역','인재', '전문성', '차별화', '채용']
df['직무역량'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['문제의식', '성공적', '프로젝트', '극복', '사례', '도전', 
            '열정', '위기 극복', '열정', '갈등', '해결', '개선', '어려웠던 경험',
            '경험', '극복경험','실패', '실행', '성취', '개선', '방법', '선택']
df['성취경험'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['사회생활', '교내외 활동', '교내외활동','사회봉사활동', '교내 활동', 
            '학교생활', '대외활동', '대화', '사회활동', '협업', '지도력', '추진력',
            '협의', '설득', '역할', '조직', '리더십', '직장생활', '타인', '공동',
            '팀', '소통', '동아리']
df['협력경험'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['비젼', '비전', '목표', '삶', '인생', '가치관']
df['인생목표'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['갈등', '갈등상황', '중재']
df['갈등경험'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['설명할', '상징단어', '단어', '소개', '관심사', '취미', '특기', 
            '평가', '표현', '자기 소개', '별명', 'PR', '좋아하는', '자기소개', 
            '자유 양식', '자기소개서', '자유양식', '비유', '책', '도서추천']
df['자기소개'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['방문', '개발언어', '이미지', '설명', '정의', '무엇이라고', '제시', 
            '발전', '제안', '제언', '견해', '이슈']
df['직무 및 기업 이해도'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

keywords = ['하고싶은 말', '소중하게','하고 싶은 말','의미 있는 시간', 
            '추가적', '기타', '어필', '특기사항', '비유']
df['기타'] = df['question'].apply(lambda x: 1 if any(keyword in x for keyword in keywords) else 0)

df.to_csv('/home/ubuntu/workspace/SemiPJT_team2/jobkorea_question_labeled_mecab.csv', index=False, encoding='UTF-8')