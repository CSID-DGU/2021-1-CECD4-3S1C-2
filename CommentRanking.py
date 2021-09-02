from konlpy.tag import Okt
from collections import Counter

#파일 경로 설정
filename = 'comment_collection.csv'
f= open(filename,'r',encoding='utf-8')
news = f.read()

#댓글 중 명사만 추출
okt=Okt()
noun = okt.nouns(news)

for item in noun[:]:
    if len(item)<2: #명사의 길이가 2이상인 것만 추출 
        noun.remove(item)


count = Counter(noun)
f.close()

noun_list = count.most_common(10) #most_common() : 매개변수 개수만큼 등수 추출
for list in noun_list:
    print(list)