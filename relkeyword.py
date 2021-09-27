import CommentRanking as rank
import extraction as ex
from konlpy.tag import Okt
import operator

class Relation:
    keyword=[]
    rel={}
    def __init__(self):
        pass
        
    def setKeyword(self,keyword):
        self.keyword=keyword
    
    def getKeyword(self):
        return self.keyword

    def setRel(self,keyword):
        self.rel=keyword

    def getRel(self):
        return self.rel

rel=Relation()
rel.setKeyword(rank.getKeyword())

okt=Okt()
keyword_list = rank.getKeyword()
for keyword in keyword_list:
    rel={}
    comments= ex.getComment(keyword)
    for comment in comments:
        tokens=okt.nouns(comment)
        for item in tokens[:]:
            if len(item)<2: #명사의 길이가 2이상인 것만 추출 => 불용어 사전 만들어서 제거해야함.
                tokens.remove(item)  
        for item in tokens:  
         if item != keyword:
                try: rel[item] +=1
                except: rel[item]=1
    rel= sorted(rel.items(), key=operator.itemgetter(1),reverse=True)
    rel= rel[:10]
    print(keyword,rel)


    
    #keyword에서 상위 10개 불러오기 -> 전체 댓글에서 상위 10개 나온 댓글들만 추출 -> 해당 댓글에서 같이 나온 적 있는 단어들 추출 -> 각 단어들 기준 상위 3개씩만 연관키워드로 추출 