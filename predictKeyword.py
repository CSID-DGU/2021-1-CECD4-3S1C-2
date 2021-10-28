from News import News
import comment_model_simple as model 
from TextManager import TextManager
from DBManager import KeywordDB
from DBManager import RelDB


text=TextManager()
db=KeywordDB()
reldb=RelDB()
news=News()

size=30 #분석할 키워드 개수
relsize=30 #분석할 연관 키워드 개수

data=db.FetchData()
news.setKeywordList(text.ExtractKeyword(data,size)) 
news.setCommentList(text.ExtractComments(news.getKeywordList(),data)) 
news.setRelList(text.ExtractRelKeyword(news,relsize)) 


for line in news.getCommentList():
    score=0
    for comment in line:
        predict=model.sentiment_predict(comment)
        score=score+predict
    score=score/len(line)
    news.setValueList(score)

db.saveDB(news) # 저장
reldb.saveDB(news) #연관 키워드 저장