import csv
from pykospacing import spacing # 띄어쓰기 보정 라이브러리
from hanspell import spell_checker # 맞춤법 수정 라이브러리
from soynlp.normalizer import * # 반복되는 문자 정제
from konlpy.tag import Okt # 형태소분석기 라이브러리

## 1. csv파일 한줄 읽기
f = open('news_articles_10.csv', 'r', encoding='utf-8')
reader = csv.reader(f)
row1 = next(reader) #의미없는 문자
row2 = next(reader) #row2는 list 자료형에 1개의 str 문장을 갖은 구조
row2 = row2.pop() # 리스트자료형에서 str 문장 추출

## 2. 띄어쓰기가 제대로 안되어 있을 수도 있으니, 띄어쓰기 보정 PyKoSpacing 적용

kospacing_row2 = spacing(row2)
print("띄어쓰기 수정 후 : " + kospacing_row2)

#3. 맞춤법 수정

spelled_row2 = spell_checker.check(kospacing_row2) #맞춤법 검사 (띄어쓰기 또한 보정함)
hanspell_row2 = spelled_row2.checked # 맞춤법에 맞게 수정
print("맞춤법 수정 후 : " + hanspell_row2)

#4. 의미없이 반복되는 이모티콘 문자 정제 (ex : ㅋㅋㅋㅋㅋ -> ㅋㅋ  ,  ㅠㅠㅠㅠㅠㅠ -> ㅠㅠ)

emoticon_normalized_row2 = emoticon_normalize(hanspell_row2, num_repeats=2) # num_reapeats : 5개라면 2개로 줄인다
print("반복 이모티콘문자 정제 : " +emoticon_normalized_row2)

#5. 형태소 분석기를 이용하여 형태소 별로 분리

okt=Okt()
morphed_row2 = okt.morphs(emoticon_normalized_row2) # 형태소 분석기를 이용하여 토큰화

print("형태소 별로 분리 후 : ")
print(morphed_row2)

print("명사만 분리 후 : ")
print(okt.nouns(emoticon_normalized_row2)) # str 문자열에 명사만 추출해준다. 띄어쓰기를 안해도 괜찮다.

print("어절만 분리 후 : ")
print(okt.phrases(emoticon_normalized_row2)) # str 문자열에 어절만 추출해준다.

print("형태소 품사태깅 후 : ")
print(okt.pos(emoticon_normalized_row2)) # 형태소 단위로 쪼갠 후 품사를 태깅해서 리스트형태로 반환
