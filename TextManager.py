from ckonlpy.tag import Postprocessor
from ckonlpy.tag import Twitter
from ckonlpy.utils import load_replace_wordpair
from ckonlpy.utils import load_wordset
from ckonlpy.utils import load_ngram
from pykospacing import Spacing
from collections import Counter
from News import News



class TextManager:

    def __init__(self):
        self.twitter=Twitter()
        self.spacing= Spacing()
        self.replace=load_replace_wordpair('./replacewords.txt') #단어 치환
        self.ngrams=load_ngram('./ngrams.txt') #ngram 단어 (띄어쓰기 복합명사)
        self.LoadDict('./CustomWord.txt') #단어 사전 로드

    def Processing(self,data): #후처리 함수
        self.postprocessor = Postprocessor(self.twitter,replace =self.replace,ngrams=self.ngrams)
        result=[]
        for sentence in data:
            sentence=self.spacing(sentence)
            line=''
            for word in self.postprocessor.pos(sentence): #문장 후처리
                line=line+word[0]
            line=self.spacing(line) #단어 띄어쓰기 처리
            result.append(line)
        return result

    def ExtractKeyword(self,data,size): #키워드 추출 
        passtags={'Noun'}
        stopwords = load_wordset('./stopwords.txt')
        self.postprocessor = Postprocessor(self.twitter,stopwords=stopwords,passtags=passtags,replace =self.replace,ngrams=self.ngrams)

        result=[]
        for sentence in data:
            sentence=self.spacing(sentence)
            temp=self.postprocessor.pos(sentence)
            for word in temp:
                if len(word[0]) > 1:
                    result.append(word[0])

        count = Counter(result)
        result = count.most_common(size) #most_common() : 매개변수 개수만큼 등수 추출
        return result
    
    def pos(self,sentence):
        result=[]
        temp=self.postprocessor.pos(sentence)
        for word in temp:
            if len(word[0]) > 1:
                result.append(word[0])
        return result


    def AddWord(self,word): #사용자 지정 단어 추가
        self.twitter.add_dictionary(word, 'Noun')
    
    def LoadDict(self,file): #사용자 지정 단어사전
        f= open(file,'r',encoding='utf-8')
        words = f.readlines()
        for word in words:
            word=word.strip('\n')
            self.twitter.add_dictionary(word, 'Noun')

    def ExtractComments(self,keywordList,data): #키워드가 포함된 문장 추출
        result=[]
        comments=self.Processing(data)
        for i in range(0,len(keywordList)):
            line=[]
            result.append(line)
        for target in comments:
            for index in range(0,len(keywordList)):
                if keywordList[index][0] in target:
                    result[index].append(target)
        return result

    def ExtractRelKeyword(self,news,size):
        passtags={'Noun'}
        stopwords = load_wordset('./stopwords.txt')
        self.postprocessor = Postprocessor(self.twitter,stopwords=stopwords,passtags=passtags,replace =self.replace,ngrams=self.ngrams)
        keywordList=news.getKeywordList()
        result=[]
        for i in range(0,len(keywordList)):
            commentLine=news.getCommentLine(i)
            lineresult=[]
            for sentence in commentLine:
                sentence=self.spacing(sentence)
                temp=self.postprocessor.pos(sentence)
                for word in temp:
                    if len(word[0]) > 1 and word[0] != keywordList[i]:
                        lineresult.append(word[0])

            count = Counter(lineresult)
            lineresult = count.most_common(size) #most_common() : 매개변수 개수만큼 등수 추출
            result.append(lineresult)
        return result



    def PrintValue(self):
        for i in range(0,len(self.keywordList)):
            if self.valueList[i] >0.4:
                print(self.keywordList[i][0],'긍정 키워드입니다.',self.valueList[i])
            elif self.valueList[i] >= 0.30103:
                print(self.keywordList[i][0],'중립 키워드입니다.',self.valueList[i])
            else:
                print(self.keywordList[i][0],'부정 키워드입니다.',self.valueList[i])
