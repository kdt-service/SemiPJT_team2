import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# 기획전략, 1page 로 임의로 설정
URL = 'https://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart=10038&isSaved=1&Page=2'
header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
response = requests.get(URL, headers = header)

schPart_dict = { "기획·전략" : 10026, "법무·사무·총무" : 10027, "인사·HR" :10028,
 "회계·세무" :10029, "마케팅·광고·MD" :10030,  "개발·데이터" : 10031,
 "디자인" :10032, "물류·무역" :10033, "운전·운송·배송" :10034,
 "영업" : 10035, "고객상담·TM" :10036, "금융·보험" :10037, "식·음료" :10038,
 "고객서비스·리테일" : 10039, "엔지니어링·설계" :10040, "제조·생산" :10041, "교육" :10042,
 "건축·시설" :10043, "의료·바이오" :10044, "미디어·문화·스포츠" :10045, "공공·복지" :10046}

df= pd.DataFrame(columns= ['section','company','date','work_type','job','question','answer'])

for kor_cate, num_cate in schPart_dict.items(): #ex) 기획·전략 10026
    for page in range(1,100): # 영업이 최대페이수 보유. 81페이지. 
        BASE_URL = 'https://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart={}&isSaved=1&Page={}'
        URL= BASE_URL.format(num_cate,page)
        response = requests.get(URL, headers = header)
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.select('.selfLists li div p') # 목록사이트에 있는 공고개수
        
        if len(tags)==0 : # 목록의 개수가 0이라는 것은 마지막 페이지를 넘어갔다는 뜻!
                break # 다음 section으로 이동! 
                
        for tag in tags : 
            company = tag.select_one('a .titTx').text.strip() # 기업명
            date = tag.select_one('.linkArray .career').text.strip() # 지원시기
            work_type = tag.select_one('.linkArray .field').text.strip() # 신입/경력    

            # 자소서 세부 url로 들어가기
            url = 'https://www.jobkorea.co.kr/'+ tag.find('a').get('href') # 세부 url
            response= requests.get(url, headers= header)
            soup= BeautifulSoup(response.text, 'html.parser')

            # job에 대한 부분이 없는 경우 존재해서 try, except
            try : 
                job = soup.select_one('.viewTitWrap .hd em').text.strip().split()[-1] # 직무
            except:
                job = '' 
            questions= soup.select('.qnaLists dt .tx') # 문항_리스트
            answers = soup.select('.qnaLists dd .tx') # 답변_리스트
            counts = soup.select('.txSpllChk') # 글자수, bytes수 정보  

            # /r 없애기
            for j in range(len(answers)):
                # 아쉬운점 mark 없애기
                question= questions[j].text #문항
                answer = answers[j].text.replace('\r','').strip()
                answer = answer.replace(counts[j].text,'').strip() #답변

                # 좋은점, 아쉬운점 없애기
                try:
                    advice_marks= soup.select('.qnaLists dd .tx .sup') #아쉬운점 
                    for am in advice_marks :
                        answer= answer.replace(am.text, '') 
                except : 
                    pass

                df.loc[len(df)]= [kor_cate, company, date, work_type, job, question, answer] # df에 정보 넣기! 
            
        if len(tags)<20 : # 목록의 개수가 20보다 작다는것은 해당 section의 마지막 페이지라는 뜻
                break # 다음 section으로 이동! 

# csv로 저장하는 코드
df.to_csv('/home/ubuntu/workspace/SemiPJT_team2/jobkorea.csv',index=False)