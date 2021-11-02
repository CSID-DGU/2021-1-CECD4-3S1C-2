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
    def saveDB(self,news):
        pass
    def checkEmpty(self):
        pass
class KeywordDB(DB):

    def saveDB(self,news):
        self.checkEmpty()
        keywordList= news.getKeywordList()
        valueList= news.getValueList()
        for i in range(0,len(keywordList)):
            keyword=keywordList[i][0]
            ranks=i+1
            mentions=keywordList[i][1]
            if valueList[i] < 0.30103:
                value=(1-valueList[i])*100
                neg= round(value,2)
                pos= 100-neg
            else:
                value=valueList[i]*100
                pos= round(value,2)
                neg= 100-pos  
            sql="REPLACE INTO devkeywords (keyword, positive, negative, ranks, mentions,id) values (%s, %s, %s, %s, %s,%s)"
            self.cursor.execute(sql, (keyword, pos, neg, ranks, mentions, 0))    
            self.db.commit()

        sql="DELETE FROM keywords"
        self.cursor.execute(sql)
        self.db.commit()
        sql="INSERT INTO keywords SELECT * FROM devkeywords"
        self.cursor.execute(sql)
        self.db.commit()
        
        
    def checkEmpty(self):
        sql="select EXISTS (select * from devkeywords limit 1) as success"
        self.cursor.execute(sql)
        self.db.commit()
        result=self.cursor.fetchone()
        if result:
            sql="DELETE FROM devkeywords"
            self.cursor.execute(sql)
            self.db.commit()

    
    def FetchData(self):
        sql="SELECT contents FROM comments" 
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
        self.checkEmpty()
        keywordList= news.getKeywordList()
        relKeywordList=news.getRelList()
        for i in range(0,len(keywordList)):
            keyword=keywordList[i][0]
            relkeyword=relKeywordList[i]
            for j in range(0,len(relkeyword)):
                tuple=(*relkeyword[j],keyword)
                sql="REPLACE INTO devrelkeywords (content, mentions, keyword) values (%s, %s, %s)"
                self.cursor.execute(sql, tuple)
                self.db.commit()

        sql="DELETE FROM relkeywords"
        self.cursor.execute(sql)
        self.db.commit()
        sql="INSERT INTO relkeywords SELECT * FROM devrelkeywords"
        self.cursor.execute(sql)
        self.db.commit()
    
    def checkEmpty(self):
        sql="select EXISTS (select * from devrelkeywords limit 1) as success"
        self.cursor.execute(sql)
        self.db.commit()
        result=self.cursor.fetchone()
        if result:
            sql="DELETE FROM devrelkeywords"
            self.cursor.execute(sql)
            self.db.commit()
