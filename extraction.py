import comment_model_simple as model 
import CommentRanking as rank

filename = 'test.csv'
f= open(filename,'r',encoding='utf-8')
comment_list = f.readlines()

#키워드를 불러옴
keyword =rank.getKeyword()
result=[]

#키워드 개수만큼 2차원 배열 생성
for i in range(len(keyword)):
    line=[]
    line.append(' ')
    result.append(line)

#크롤링 자료에서 키워드들이 들어가 있는 댓글 추출
for comment in comment_list:
    for target in keyword:
        if target in comment:
            i=keyword.index(target)
            result[i].append(comment)


#각 키워드들 점수 계산

for i in range(len(keyword)):
    score=0
    for target in result[i]:
        predict=model.sentiment_predict(target)
        if predict >0.5:
            score=score+(predict-0.5)
        else:
            score=score-(0.5-predict)
    score=score/len(result[i])

    if score>0:
        print(keyword[i],'긍정 키워드입니다.',score)
    else:
        print(keyword[i],'부정 키워드입니다.',score)