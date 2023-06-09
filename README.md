# 취업준비생을 위한 자기소개서 서비스
자기소개서 내용을 바탕으로한 키워드, 요약 & 직무와 기업추천 & 파인튜닝을 활용한 문장완성 기능

## ⌨️ 프로젝트 소개
[잡코리아 합격자기소개서](https://www.jobkorea.co.kr/starter/passassay/)를 바탕으로 자기소개서를 입력받아 여러 기능을 제공해주는 서비스입니다.    
![image](https://user-images.githubusercontent.com/84755366/236085155-06a54018-a025-4441-ae7b-466f232d6394.png)

## 🕰️ 개발 기간 
- 23.04.21. ~ 23.05.04 

## 👩‍💻👨‍💻멤버구성 
- 문다은 : 크롤링 , 문항분류 , 키워드 추출, 요약, openapi_ChatGPT , Streamlit 제작
- 송세영 : 크롤링 , 토큰화 , 키워드 추출, 요약 , openapi_ChatGPT , 직무와 기업추천, Streamlit 제작
- 임희나 : 크롤링 , 문항분류 , 딥러닝 모델 & 파인튜닝, Streamlit 제작
- 정경원 : 크롤링 , 데이터클렌징,  딥러닝 모델 & 파인튜닝, Streamlit 제작
- 하정현(팀장) : 크롤링 , 문항분류 , 딥러닝 모델 & 파인튜닝 , Streamlit 제작 , 발표       
- ✔️ Check out our [Notion](https://www.notion.so/Semi-Project-Team-2-f7fe7122726345caae4a057fefa25620)

## ⚙️ 개발환경
- Python 3.8.16
- beautifulsoup4           4.12.2 
- gensim                   3.8.3
- konlpy                   0.6.0
- mecab-python3            1.0.6
- scikit-learn             1.0
- streamlit                1.22.0
- streamlit-option-menu    0.3.2
- tokenizers               0.13.3
- transformers             4.28.1

## ❓ 프로젝트 계획 이유

<img src ="https://user-images.githubusercontent.com/84755366/236082873-b3249c91-1b20-40d9-97bc-314dac009048.png" width="300" height="300"/>
취업준비생이라면 자기소개서를 준비하다가 막막하다는 느낌을 받은 경험이 한번쯤은 있을 것입니다. 이 프로젝트도 경험에서 비롯되어 취업준비생이 시간을 많이 투자하고 준비하기 힘들어하는 자기소개서를 쉽게 작성하기 위한 도움을 주고자 서비스를 제작하게 되었습니다.       

## 🔎 프로젝트 수행 절차 및 방법
+ 데이터 수집   
  + 잡코리아 합격자소서 BeautifulSoup으로 29489건 크롤링   
  + 컬럼명 : 지원분야(section), 기업(company), 지원시기(date), 신입/경력(work_type), 직무(job), 문항(question), 답변(answer)       
+ 전처리
  + 텍스트 클렌징 
    + Question에 소제목이 들어간 경우 drop명령문으로 해당 행 삭제
    + Question에 글자수와 관련된 내용 정규표현식으로 해당 부분 삭제
    + 한 지원자가 거의 같은 내용으로 여러 회사에 지원한 경우, 코사인 유사도를 통해 자기소개서 본문에 대해 유사도 0.95이상의 데이터 삭제 (유사도 0.95 이상은 동일한 자기소개서로 간주)
   + 토큰화
      + Mecab을 활용하여 직무별, 기업별 (Groupby 활용) 합격자소서 일반명사(NNG)만 토큰화 진행
   + 문항분류
      + 질문의 키워드 별로 문항분류 
      + 문항분류 유형 : 지원동기, 입사 후 포부, 성장과정, 성격&장단점, 직무역량, 성취경험, 협력경험, 최근이슈, 인생목표, 갈등경험
 + 키워드 추출 & 문장요약
   +  Mecab을 이용해 토큰화한 기업별, 직무별 합격자기소개서를 TF-IDF를 계산하여 상위 20개의 키워드 추출 & Gensim.summarization 통해 자기소개서 문장 요약 ( 데이터가 10개 미만인 기업,직무는 정확한 결과 도출이 어렵다고 생각되어 제외)
 + 기업, 직무 추천
    + INPUT 자기소개서도 위 키워드추출 방법과 동일하게 키워드를 추출하여 직무별, 그룹별  코사인 유사도가 높은 상위 3개의 직무, 기업 추천
 + 문장 자동 완성
    + 딥러닝 생성모델 파인튜닝
      + 사용모델 : KoGPT2
      + 학습 데이터 생성 과정
        + 중복 문항에 해당되는 자기소개서 처리 
        + Train, Test 데이터 분리 (80:20)
        + 문장 단위로 분리
      + 모델 학습
        + epoch 5,10 학습진행
        + 결과 비교 : epoch5 모델이 일반화된 문장을 더 잘 추출하는 것으로 판단하여 최종모델로 선정!
    + OpenAPi GPT
      + GPT openAPI 활용하여 파이썬 상에서 구현 ( 문장완성 기능, 문장요약 기능 가능)    
+ 프로토타입 제작
  + Streamlit 패키지를 사용하여 제작 
    + Streamlit 결과물은 아래에 있는 '주요기능' 을 클릭하면 확인이 가능합니다.  

## 📌 주요기능

#### 1. 입력
- 자기소개서를 문항별로 입력받는 기능입니다. 문항수가 4문항 이상이라면 '답변추가하기' 버튼을 눌러 문항 수를 늘릴 수 있습니다. 
#### 2. 키워드 추출
- 자기소개서를 다 입력한 다음 '분석하기' 버튼을 누르면 키워드를 제시해줍니다. 키워드를 통해 작성한 자기소개서에 어필하고 있는 주요부분을 전체적으로 볼 수 있습니다. 
#### 3. 요약
- 자기소개서를 다 입력한 다음 '분석하기' 버튼을 누르면 문항 별로 요약본을 제시해줍니다. 요약을 통해 주요문장들을 확인 할 수 있습니다. 
#### 4. 직무, 기업 추천
- 잡코리아에서 크롤링한 데이터를 바탕으로 직무별, 기업별 키워드 데이터를 갖고 있습니다. 키워드 추출에서 얻은 키워드를 바탕으로 가장 유사한 직무와 기업을 3개씩 추천합니다 
#### 5. 자동문장완성
- 작성을 원하는 자기소개서 문항을 선택하고, 완성하고자 하는 문장을 입력한 후 '문장 완성하기' 버튼을 누르면 완성된 3개의 문장을 제시해줍니다. 


