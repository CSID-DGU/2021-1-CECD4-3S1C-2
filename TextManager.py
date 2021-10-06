from ckonlpy.tag import Postprocessor
from ckonlpy.tag import Twitter
from ckonlpy.utils import load_replace_wordpair
from ckonlpy.utils import load_wordset
from ckonlpy.utils import load_ngram
from pykospacing import Spacing
from collections import Counter


class TextManager:

    def __init__(self):
        self.twitter=Twitter()
        self.spacing= Spacing()
        self.replace=load_replace_wordpair('./replacewords.txt') #단어 치환
        self.ngrams=load_ngram('./ngrams.txt') #ngram 단어 (띄어쓰기 복합명사)
        self.LoadDict('./CustomWord.txt') #단어 사전 로드
        self.keywordList=[] #상위 키워드 리스트

    def Processing(self,filename): #후처리 함수
        self.postprocessor = Postprocessor(self.twitter,replace =self.replace,ngrams=self.ngrams)
        f= open(filename,'r',encoding='utf-8')
        file = f.readlines()
        result=[]
        for sentence in file:
            sentence=self.spacing(sentence)
            line=''
            for word in self.postprocessor.pos(sentence): #문장 후처리
                line=line+word[0]
                line=self.spacing(line) #단어 띄어쓰기 처리
            result.append(line)
        return result

    def ExtractKeyword(self,number,filename): #키워드 추출 
        passtags={'Noun'}
        stopwords = load_wordset('./stopwords.txt')
        self.postprocessor = Postprocessor(self.twitter,stopwords=stopwords,passtags=passtags,replace =self.replace,ngrams=self.ngrams)

        f= open(filename,'r',encoding='utf-8')
        file = f.readlines()

        result=[]
        for sentence in file:
            sentence=self.spacing(sentence)
            temp=self.postprocessor.pos(sentence)
            for word in temp:
                if len(word[0]) > 1:
                    result.append(word[0])

        count = Counter(result)
        result = count.most_common(number) #most_common() : 매개변수 개수만큼 등수 추출
        return result
    
    def pos(self,sentence):
        print(self.twitter.pos(sentence))


    def AddWord(self,word): #사용자 지정 단어 추가
        self.twitter.add_dictionary(word, 'Noun')
    
    def LoadDict(self,file): #사용자 지정 단어사전
        f= open(file,'r',encoding='utf-8')
        words = f.readlines()
        for word in words:
            word=word.strip('\n')
            self.twitter.add_dictionary(word, 'Noun')

    def ExtractComments(self,keywords,file): #키워드가 포함된 문장 추출
        comments=self.Processing(file)
        result=[]
        for i in keywords:
            line=[]
            line.append(i)
            result.append(line)
        for target in comments:
            for index in range(0,len(keywords)):
                if keywords[index] in target:
                    result[index].append(target)
        return result

'''
text=TextManager('./test2.csv')
temp=text.ExtractKeyword(2)
keywords=[]
for i in temp:
    keywords.append(i[0])
text.ExtractComments(keywords,'./test2.csv')
#print(text.ExtractKeyword(5))
#print(text.Processing())
'''