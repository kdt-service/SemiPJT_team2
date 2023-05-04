import streamlit as st
from input_keyword import KeywordExtractor
from input_summary import TextSummary
from company_keyword_tokenization import CompanyKeywords
from job_keyword_tokenization import JobKeywords
from job_recommend import *
from company_recommend import *
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from generate_text import *
import re
from PIL import Image

def streamlit_menu():
    
    with st.sidebar:
        selected = option_menu(
            menu_title="메인메뉴",  
            options=["서비스 소개", "자기소개서 분석", "자기소개서 문장 완성"],  
            icons=["patch-question", "bar-chart-line-fill", "pencil-square"],
            menu_icon="file-person",
            default_index=0,
            styles={"nav-link-selected": {"background-color": "#b1c8fa"}}
        )
    return selected

selected = streamlit_menu()

if selected == "서비스 소개":
    
    # 서비스 제작 동기
    st.markdown("<div style='text-align: center;'><h2>서비스 제작 이유</h2></div>", unsafe_allow_html=True)
    st.title(' ')

    left_co,last_co = st.columns([1,1])
    with left_co :
        image = Image.open("/home/ubuntu/workspace/SemiPJT_team2/SemiPJT_team2/others/i1.png")
        new_image = image.resize((700,600))
        st.image(new_image)
    with last_co :
        image = Image.open("/home/ubuntu/workspace/SemiPJT_team2/SemiPJT_team2/others/i2.png")
        new_image = image.resize((700,600))
        st.image(new_image)
    st.write(' ')
    st.markdown("<p align='center'> <font size = '4'> 취업준비생이 시간을 많이 투자하고 준비하기 힘들어하는   </font></p>", unsafe_allow_html=True)
    st.markdown("<p align='center'> <font size = '4'> 자기소개서를 쉽게 작성하고자 서비스를 제작하게 되었습니다.  </font></p>", unsafe_allow_html=True)

    # 서비스 사용방법   
    st.title(' ')
    st.markdown("<div style='text-align: center;'><h2>서비스 사용방법</h2></div>", unsafe_allow_html=True)
    st.title('')
    st.subheader('👨‍💻 자기소개서 분석 사용방법')
    s1 = """
    Step 1.  자기소개서 글을 문항별로 입력해주세요. \n 
    더 많은 문항 수를 원한다면  \'답변추가하기\'  버튼을 눌러주세요. 
    """
    s2 = """Step 2.  모든 문항을 다 입력했다면  \'분석하기\'  버튼을 눌러주세요. """
    s3 = """Step 3.  키워드 추출 & 요약 결과를 확인합니다. """
    s4 = """
    Step 4.  자신의 자기소개서와 관련된 직무와 기업 추천 확인하세요. \n
    키워드를 기반으로 가장 적합한 직무와 기업을 추천드립니다. 
    """
    st.success(s1)
    st.success(s2)
    st.success(s3)
    st.success(s4)
    # 자기소개서 문장 완성 사용방법
    st.title(' ')
    st.subheader('👨‍💻 자기소개서 문장 완성 사용방법')
    st.success('Step 1. 작성을 원하는 자기소개서 문항을 선택해주세요.')
    st.success('Step 2. 선택한 자기소개서 문항에 맞는 완성되지 않은 문장을 입력해주세요.')
    st.success('Step 3. \'문장 완성하기\' 버튼을 눌러주세요.')
    d1 = """
    Step 4. 완성된 3개의 문장을 확인합니다. \n
    Tip : 마음에 드는 문장이 없다면 문장 완성하기 버튼을 다시 한번 눌러 다른 결과도 확인 해보세요!
    """
    st.success(d1)

    # 만든사람들
    st.title(' ')
    st.title('')
    st.markdown("<div style='text-align: center;'><h2>만든 사람들</h2></div>", unsafe_allow_html=True)
    st.write('')
    st.markdown("<p align='center'> <font size = '5'> Made by 문다은 송세영 임희나 정경원 하정현</font></p>", unsafe_allow_html=True)
    st.markdown("<p align='center'> <font size = '3'>  본 서비스는 멀티캠퍼스 11회차 서비스산업 데이터분석가 취업캠프의 일환으로 </font></p>", unsafe_allow_html=True)
    st.markdown("<p align='center'> <font size = '3'>   세미프로젝트를 진행하며 만들어졌습니다. </font></p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1 :
        st.subheader("✔️ Check out our [Notion](https://www.notion.so/Semi-Project-Team-2-f7fe7122726345caae4a057fefa25620)")
    with col2 :
        st.subheader("✔️ Check out our [GitHub](https://github.com/kdt-service/SemiPJT_team2)")

    ending = """본 서비스는 멀티캠퍼스 11회차 서비스산업 데이터분석가 취업캠프의 일환으로\n
    세미프로젝트를 진행하며 만들어졌습니다.  """
        
    
if selected == "자기소개서 분석":
    left_recommend_column, right_recommend_columns=st.columns(2)
    first_recommend_column, sec_recommend_column=st.columns(2)
    
    if 'answer_count' not in st.session_state:
        st.session_state.answer_count = 1
    st.markdown("**<p align='center'> <font size = '8'> 자기소개서 분석</font></p>**", unsafe_allow_html=True)
    st.title('')
    st.markdown("<div style='text-align: center;'><h2>자기소개서 입력</h2></div>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")

    answers = []
    for i in range(st.session_state.answer_count):
        answers.append(st.text_area(f'✍️ 문항 {i + 1}에 대한 답변을 입력해주세요', height=200))

    st.write("")
    if st.button('답변 추가하기'):
        st.session_state.answer_count += 1

    st.write("")
    btn_clicked0 = st.button("분석하기")
    
    if btn_clicked0:
        # 키워드 제공 및 요약 제공을 위한 초기화
        top_keywords_list = []
        summarized_text_list = []
        input_text = ' '.join(answers)
        input_user= input_text

        for answer in answers:
            if not answer.strip():
                continue
            # 각 입력에 대한 키워드 제공
            extractor = KeywordExtractor()  # 인스턴스 생성
            top_keywords = extractor.extract_keywords(answer)
            top_keywords_list.append(', '.join(top_keywords))

            # 각 입력에 대한 요약 제공
            text_summary = TextSummary(answer)
            summarized_text = text_summary.summarize_text()
            summarized_text_list.append(summarized_text)

        # 각 입력에 대한 키워드 및 요약 결과를 세션 상태에 저장
        st.session_state.keyword_boxes = top_keywords_list
        st.session_state.summary_boxes = summarized_text_list

        # 직무 추천 제공
        user_keywords = extract_keywords(input_text)
        job_keywords_df = pd.read_csv('/home/ubuntu/workspace/SemiPJT_team2/job_keywords_top20.csv')
        similarity_scores = cosin_similarity(user_keywords, job_keywords_df)
        top_jobs = top_similar_jobs(similarity_scores, job_keywords_df)
        st.session_state.job_box1= top_jobs.직무[1]
        st.session_state.job_box2= top_jobs.직무[2]
        st.session_state.job_box3= top_jobs.직무[3]

        # 기업 추천 제공
        user_keywords = extract_keywords(input_text)
        company_keywords_df = pd.read_csv('/home/ubuntu/workspace/SemiPJT_team2/company_keywords_top20.csv')
        similarity_scores = cosin_similarity(user_keywords, company_keywords_df)
        top_companys = top_similar_companys(similarity_scores, company_keywords_df)
        st.session_state.company_box1= top_companys.기업[1]
        st.session_state.company_box2= top_companys.기업[2]
        st.session_state.company_box3= top_companys.기업[3]


    st.markdown("<div style='text-align: center;'><h2>나의 자기소개서 분석 결과</h2></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>단어의 문장 중요도를 기반으로 자기소개서를 분석한 결과입니다.</div>", unsafe_allow_html=True)
    st.write("")

    if 'keyword_boxes' in st.session_state and 'summary_boxes' in st.session_state:
        for i in range(len(st.session_state.keyword_boxes)):
            st.markdown(f"**<p align='center'> 문항 {i + 1}에 대한 분석 결과</p>**", unsafe_allow_html=True)
            
            st.write('👩‍💻 중요키워드')
            keyword_box = st.warning(st.session_state.keyword_boxes[i])
            
            st.write('')
            st.write('👩‍💻 요약 결과')
            summary_box = st.warning(st.session_state.summary_boxes[i])
            st.write('')
    else:
        for i in range(st.session_state.answer_count):
            st.markdown(f"**<p align='center'> 문항 {i + 1}에 대한 분석 결과</p>**", unsafe_allow_html=True)
            
            st.write('👩‍💻 중요키워드')
            keyword_box = st.warning('')
            
            st.write('')
            st.write('👩‍💻 요약 결과')
            summary_box = st.warning('')
            st.write('')
    
    st.title("")
    st.markdown("<div style='text-align: center;'><h2>이런 직무, 기업도 추천해요!</h2></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>나의 자기소개서로 지원할 수 있는 직무와 기업 추천 결과입니다.</div>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    # 첫 번째 행에 '직무'와 '기업' 표시
    first_recommend_column, sec_recommend_column=st.columns(2)
    with first_recommend_column: #직무추천
        st.markdown("<div style='text-align: center;'>직무</div>", unsafe_allow_html=True)
        st.write('')
        job_box1= st.info('1. '+st.session_state.get('job_box1',''))
        job_box2= st.info('2. '+st.session_state.get('job_box2',''))
        job_box3= st.info('3. '+st.session_state.get('job_box3',''))
        
    with sec_recommend_column:
        st.markdown("<div style='text-align: center;'>기업</div>", unsafe_allow_html=True)
        st.write('')
        company_box1= st.info('1. '+st.session_state.get('company_box1',''))
        company_box2= st.info('2. '+st.session_state.get('company_box2',''))
        company_box3= st.info('3. '+st.session_state.get('company_box3',''))
        
if selected == "자기소개서 문장 완성":
    
    #st.title(f"{selected}")
    st.markdown("<div style='text-align: center;'><h2>자기소개서 문장 입력</h2></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>완성하기 어려운 문장을 입력해주세요.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>합격자소서를 바탕으로 문장을 작성해드립니다.</div>", unsafe_allow_html=True)
    
    # 여백 생성
    st.write("")
    st.write("")
    
    # 셀렉트박스에 표시될 옵션 리스트
    options = ["지원동기", "입사 후 포부", "성장과정", "성격 장단점", "직무역량", "성취경험", "협력경험", "인생목표", "갈등경험", "자기소개", "직무 및 기업 이해도", "기타"]

    # 셀렉트박스 생성
    selected_option = st.selectbox("✍️문항을 선택해주세요", options)

    # 선택된 옵션 출력
    st.write("선택된 문항 :", selected_option)
    
    # 여백 생성
    st.write("")
    st.write("")
    st.write("")
    
    user_input = st.text_input('✍️완성하기 어려웠던 문장을 입력해주세요')
    
    model_input = selected_option + ' ' + user_input
    
    model = load_model()
    #generated_texts = generate_result(model_input, model)
    #modified_texts = [text.replace('</s>', '') for text in generated_texts if not any(option in text for option in options)]
    
    st.write("")# 여백 생성

    btn_clicked = st.button("문장 완성하기")
    
    st.write("") # 여백 생성
    
    if btn_clicked:
        with st.spinner('문장을 완성하고 있습니다. 잠시만 기다려주세요.'):
            generated_texts = generate_result(model_input, model)
            
            modified_texts = [text.replace("</s>", "") for text in generated_texts]
            modified_texts = [text.replace("`", "'") for text in modified_texts]
            modified_texts = [text.replace(selected_option, '') for text in modified_texts]
        
        # st.write(repr(modified_texts[0]))
        st.write('👩‍💻 결과 1')    
        st.warning(modified_texts[0])
        st.write("")
        st.write('👩‍💻 결과 2')
        st.warning(modified_texts[1])
        st.write("")
        st.write('👩‍💻 결과 3')
        st.warning(modified_texts[2])
    