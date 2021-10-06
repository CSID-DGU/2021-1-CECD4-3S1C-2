import comment_model_simple as model 
from TextManager import TextManager

text=TextManager()
temp=text.ExtractKeyword(30,'./comment_collection.csv')
keyword=[]
for i in temp:
    keyword.append(i[0])
commentList=text.ExtractComments(keyword,'./comment_collection.csv')


for line in commentList:
    score=0.5
    for i in range(1,len(line)):
        predict=model.sentiment_predict(line[i])
        if predict >0.5:
            score=score+(predict-0.5)
        elif predict == 0.5:
            pass
        else:
            score=score-(0.5-predict)
    score=score/len(line)

    if score >0.6:
        print(line[0],'긍정 키워드입니다.',score)
    elif score >= 0.4:
        print(line[0],'중립 키워드입니다.',score)
    else:
        print(line[0],'부정 키워드입니다.',score)