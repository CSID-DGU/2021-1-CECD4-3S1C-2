import pymysql

class DB:
    def __init__(self):
        self.db=pymysql.connect(
            host="3.35.115.140",
            port=3306,
            user="root",
            passwd="1234",
            database="news",
            charset="utf8"
        )
        self.cursor=self.db.cursor()

class KeywordDB(DB):

    def saveDB(self,news):
        keywordList= news.getKeywordList()
        valueList= news.getValueList()
        for i in range(0,len(keywordList)):
            keyword=keywordList[i][0]
            ranks=i+1
            mentions=keywordList[i][1]
            if valueList[i] < 0.5:
                value=(1-valueList[i])*100
                neg= round(value,2)
                pos= 100-neg
            else:
                value=valueList[i]*100
                pos= round(value,2)
                neg= 100-pos   
            
            sql="REPLACE INTO keywords (keyword, positive, negative, ranks, mentions) values (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (keyword, pos, neg, ranks, mentions))    
            self.db.commit()
    
    def FetchData(self):
        sql="SELECT contents FROM comments" #select 할 테이블 이름
        self.cursor.execute(sql)
        self.db.commit()
        temp=self.cursor.fetchall()
        data=[]
        for target in temp:
            target=str(target)
            target=target.rstrip(')')
            target=target.rstrip(',')
            target=target.rstrip("'")
            target=target.lstrip('(')
            target=target.lstrip("'")
            target=target.replace('\\n','')
            data.append(target)
        return data
        
class RelDB(DB):
    def saveDB(self,news):
        keywordList= news.getKeywordList()
        contentList=news.getRelList()
        for keywords in keywordList:
            keyword=keywords[0]
            for contents in contentList:
                for temp in contents:
                    content=temp[0]
                    mentions=temp[1]
                    sql="REPLACE INTO relkeywords (content, keyword, mentions) values (%s, %s, %s)"
                    self.cursor.execute(sql, (content, keyword, mentions))
                    self.db.commit()
