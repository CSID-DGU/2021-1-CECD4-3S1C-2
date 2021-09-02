from konlpy.tag import Okt
from collections import Counter

#파일 경로 설정
filename = ' '
f= open(filename,'r',encoding='utf-8')
news = f.read()

#댓글 중 명사만 추출
okt=Okt()
noun = okt.nouns(news)
for i,item in enumerate(noun):
    if len(item)<2: #명사의 길이가 2이상인 것만 추출 
        noun.pop(i)

count = Counter(noun)
f.close()

noun_list = count.most_common(1000) #most_common() : 매게변수 개수만큼 등수 추출
for list in noun_list:
    print(list)