from soynlp.noun import LRNounExtractor
from soynlp.tokenizer import LTokenizer
from konlpy.tag import Okt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction import CounterVectorizer


titles = [
    "사망한 사람들 유가족 앞에서 그런 말 해보시지요.",
    "1000명 중에 1명인데 5천만이면 ㅋㅋㅋ 5만명인데 저건 진짜 아니지.. 아니 도대체 무슨 생각으로 저런 말들을 내뱉는거지.. 그러니 욕처먹지..",
    "개인은 무시하는게 전체주의 입니다. 전체를 위해서 소수의 희생은 감수해야 한다는.. 그래서 문재인 뽑고.. 중국몽 찬양하는 거잖아..",
    "이거 이상한 여자인데요. 걱정하지 말라고??? 수백만명 접종해서 중증 이상반응이 나와 가족들에게 나오면 그게 100% 인건데 걱정하지 말라고?? 장난치냐?",
    "이상 반응 0.1%가 적은 건가요? 저런 말을 하니까 국민이 더 불신하는 겁니다.",
    "뻣뻣이 악수도 안한 한일 외교, 20분 만났지만 입장차 '팽팽'",
    "장례 마쳤지만 사인 규명은 아직…경찰, 한강 CCTV 분석",
    "여야, 청문 대치 정국…'29+α' 野패싱 임명 강행수순 가나 ",
    "임영웅, '실내흡연' 논란에 실망 드려 죄송…질책 새기겠다",
    "'세기의 이혼' 빌게이츠·멀린다 163조원 재산분할 돌입",
    "이낙연 군가산점 대신 제대 때 사회출발자금 3천만원 주자",
    "이재명 성적은 '미미'했지만 고집 세고 씩씩 초1 성적표 공개 ",
    "'뜨거운 감자' 경부고속도로 수도권 구간 지하화…이번엔 가능할까",
    "[르포] 코로나도 막지 못한 동심?…해운대 공룡모래축제 북적",
    "스가 내각 출범후 한일외교 첫 만남, 현안 입장차 '팽팽'",
    "미, 중국 우주정거장 22t 쓰레기 추적…지상추락 우려에 시끌",
    "'역주행' SG워너비 라이브음원 공개에 멤버들 협의없었다 반발",
    "한일 외교장관 첫 회담…미래지향적 관계발전 뜻 같이해",
    "문대통령 어린이들 신나게 뛰어놀 날 최대한 앞당기겠다",
    "'계엄군 총탄에 얼굴도 없이' 41년만에 사진 찾은 故 전재수 군",
    "'슈퍼 화요일' 치른 여야, 내일 김부겸 청문회로 '2라운드'",
    "日모테기, 정 장관에 위안부 소송 등에 '韓 적절 대응' 요구",
    "정의용·모테기 첫 회동…양국 의사소통 본격 재개 계기 ",
    "너는 선물이었다…눈물 속 한강공원 사망 대학생 발인식",
    "정부·공공기관, 가상화폐 관련 펀드에 500억 간접투자",
    "정의용·모테기 첫 회동…과거사·북핵 문제 논의",
    "[1보] 한미일 회담 후 정의용·모테기 첫 양자 회동",
    "돈만 댔다는 기성용, 사실이라면 아버지가 '사문서위조'",
    "한미일 외교장관 런던서 회동…정의용·모테기 첫 대면",
    "靑, 野 '장관후보자 3인 부적격'에 지금은 국회의 시간",
    "'한전규제 합리화' 이소영 곤욕…역시 초선5적, 당 떠나라",
    "이용수 할머니, 위안부 손해배상 항소…정의·인권 승리할 것"
]

print(len(titles))

# title_df = pd.DataFrame(titles)
# print(title_df)

okt = Okt()
title_topic = []
detokenized_doc = []

# * Topic Extraction Process
for i in range(len(titles)):
    nouns = okt.nouns(str(titles[i]))
    print(nouns)
    title_topic.append(okt.phrases(str(nouns)))
    t = ' '.join(title_topic[i])
    detokenized_doc.append(t)
print(detokenized_doc)
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(detokenized_doc)

print(X.shape)

lda_model = LatentDirichletAllocation(n_components=32, random_state=0)
lda_top = lda_model.fit_transform(X)

terms = vectorizer.get_feature_names()


def get_topics(components, feature_names, n=2):
    for idx, topic in enumerate(components):
        print("Topic %d :" % (
            idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])


get_topics(lda_model.components_, terms)
