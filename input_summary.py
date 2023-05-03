from gensim.summarization import summarize

class TextSummary:
    def __init__(self, input_text):
        self.input_text = input_text

    # gensim 문장 갯수
    def sentence_count_gensim(self, text):
        from gensim.summarization.textcleaner import split_sentences
        return len(split_sentences(text))

    def summarize_text(self):
        # 문장 갯수가 5개 미만이면 요약하지 않음
        sentence_count = self.sentence_count_gensim(self.input_text)
        if sentence_count < 5:
            return "입력한 텍스트의 문장 수가 5개 미만이므로 요약하지 않습니다."
        
        # 답변 요약 및 반환
        summary = summarize(self.input_text, word_count=140)
        if summary == "":
            return "요약 결과가 없습니다."
        else:
            return summary

if __name__ == "__main__":
    input_text = input("문자열을 입력하세요: ")
    text_summary = TextSummary(input_text)
    summarized_text = text_summary.summarize_text()
    #요약결과 summarize.txt 파일에 저장
    f= open('summarize.txt','w')
    f.write(summarized_text)
    f.close()
