import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import warnings
warnings.filterwarnings("ignore")

URL = 'https://www.jobkorea.co.kr/Starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart={}&isSaved=1&Page={}' 
header = {'User-agent' : 'Mozila/2.0'}  
df = pd.DataFrame(columns = ['section', 'company', 'date', 'work_type', 'job', 'question', 'answer'])

section_list = {'10026':'기획·전략', '10027':'법무·사무·총무', '10028':'인사·HR', '10029':'회계·세무', '10030':'마케팅·광고·MD', '10031':'개발·데이터', '10032':'디자인', '10033':'물류·무역', 
                '10034':'운전·운송·배송', '10035':'영업', '10036':'고객상담·TM', '10037':'금융·보험', '10038':'식·음료', '10039':'고객서비스·리테일', '10040':'엔지니어링·설계', '10041':'제조·생산',
                '10042':'교육', '10043':'건축·시설', '10044':'의료·바이오', '10045':'미디어·문화·스포츠', '10046':'공공·복지'} 

#섹션별 페이지 수 확인
pages = []
for section_code, section_name in section_list.items():
    response = requests.get("https://www.jobkorea.co.kr/Starter/PassAssay?schPart={}&schWork=&schEduLevel=&schCType=&schGroup=&isSaved=1&isFilterChecked=1&OrderBy=0&schTxt=".format(section_code), headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    doc_count = int(soup.select_one('#titSelCount').text.strip())
    page_count= math.ceil(doc_count/20)
    pages.append(page_count)

for i, (section_code, section_name) in enumerate(section_list.items()):
    section_pages = pages[i]
    for page in range(1, section_pages+1):
        response = requests.get(URL.format(section_code, page), headers=header)
        soup = BeautifulSoup(response.text, 'html.parser') 
        li_tag = soup.select('.selfLists li') 
        for li in li_tag:
            company = li.select_one('span.titTx').text.strip()
            date = li.select_one('span.career').text.strip()
            work_type = li.select_one('span.linkArray').text.strip()[10:12]
            job = li.select_one('span.linkArray').text.strip()[13:]
            #지원분야, 기업, 지원시기, 신입 or 경력 or 인턴, 직무 까지 가져옴.
            
            detail_url = li.select_one('.tit a').get('href') #자소서 문답 볼 수 있는 링크 가져오기
            full_detail_url = f"https://www.jobkorea.co.kr{detail_url}"
            detail_url_response = requests.get(full_detail_url, headers=header)
            detail_url_soup = BeautifulSoup(detail_url_response.text, 'html.parser')
            
            #문항 가져와야함 (한문항-한답변 세트 하나씩)
            q_list = detail_url_soup.select('.qnaLists span.tx')
            for i, q in enumerate(q_list):
                question = q.text.strip()
                a_list = detail_url_soup.select('.qnaLists div.tx')
                answer = a_list[i].text.replace('\r','').strip() #뒤에 글자수 744자1,287Byte 지워야함
        
            #데이터 프레임에 넣기
                data = {'section': section_name, 'company': company, 'date': date, 'work_type': work_type, 'job': job, 'question': question, 'answer': answer}
                df = df.append(data, ignore_index=True)                