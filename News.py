class News:
    def __init__(self):
        self.__keywordList=[] #상위 키워드 리스트 (키워드, 언급 횟수) 튜플 구조 리스트
        self.__commentList=[]#키워드와 맵핑되는 인덱스에 댓글을 저장하는 2차원 리스트 [댓글1,댓글2..] 구조
        self.__valueList=[]#각 키워드의 긍/부정 점수를 저장하는 리스트
        self.__relList=[] #각 키워드의 연관키워드를 저장하는 리스트
        self.__newsId=-1 #뉴스의 ID값

    def setId(self,id):
        self.__newsId=id
    
    def getId(self):
        return self.__newsId
        
    def setKeywordList(self,data):
        self.__keywordList = data
    
    def getKeywordList(self):
        return self.__keywordList

    def setCommentList(self,data):
        self.__commentList=data
    
    def getCommentList(self):
        return self.__commentList
    
    def getCommentLine(self,index):
        return self.__commentList[index]
    
    def setValueList(self,data):
        self.__valueList.append(data)
    
    def getValueList(self):
        return self.__valueList

    def setRelList(self,data):
        self.__relList=data
    
    def getRelList(self):
        return self.__relList