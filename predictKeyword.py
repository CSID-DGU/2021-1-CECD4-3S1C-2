import comment_model_simple as model 
from TextManager import TextManager
from SaveDB import saveDB

filename='./test.csv'
text=TextManager()
db=saveDB()
keywordList=text.ExtractKeyword(filename,10)
keyword=[]
for i in keywordList:
    keyword.append(i[0])
commentList=text.ExtractComments(keyword,filename)

filename2='./result.txt'
f= open(filename2,'w')
valueList=[]
for line in commentList:
    score=0
    for i in range(1,len(line)):
        predict=model.sentiment_predict(line[i])
        f.write(str(predict)+'\n')
        score=score+predict
    score=score/len(line)
    valueList.append(score)
    if score >0.4:
        print(line[0],'긍정 키워드입니다.',score)
    elif score >= 0.30103:
        print(line[0],'중립 키워드입니다.',score)
    else:
        print(line[0],'부정 키워드입니다.',score)

f.close()
db.saveDB(keywordList,valueList)