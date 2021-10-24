from News import News
import comment_model_simple as model 
from TextManager import TextManager
from DBManager import KeywordDB


text=TextManager()
db=KeywordDB()
news=News()
# for id in idList:
id=3 #분석할 뉴스 아이디
size=10 #분석할 키워드 개수


news.setId(id)
data=db.FetchData(id)
news.setKeywordList(text.ExtractKeyword(data,size)) 
news.setCommentList(text.ExtractComments(news.getKeywordList(),data)) 
news.setRelList(text.ExtractRelKeyword(news,10)) 


for line in news.getCommentList():
    score=0
    for comment in line:
        predict=model.sentiment_predict(comment)
        score=score+predict
    score=score/len(line)
    news.setValueList(score)

db.saveDB(news) # 저장