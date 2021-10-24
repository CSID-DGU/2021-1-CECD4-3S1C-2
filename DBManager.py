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

  #  def initDB(self):
  #      self.cursor.execute("CREATE TABLE KEYWORDS (keyword VARCHAR(30), positive FLOAT, negative FLOAT, ranks INT, mentions INT, news_id INT, primary key (keyword,news_id));")
  #      self.db.commit()

    def checkEmpty(self,id):
        sql="select EXISTS (select id from KEYWORDS where news_id=%s limit 1) as success"
        self.cursor.execute(sql,(id))
        self.db.commit()
        result=self.cursor.fetchall()
        return result

    def saveDB(self,news):
        keywordList= news.getKeywordList()
        valueList= news.getValueList()
        id=news.getId()
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
            #sql="insert into KEYWORDS (keyword, positive, negative, ranks, mentions, news_id) values (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE keyword=VALUES(keyword), positive=VALUES(positive), negative=VALUES(negative), ranks=VALUES(ranks), mentions=VALUES(mentions), news_id=VALUES(news_id)"
            sql="REPLACE INTO KEYWORDS (keyword, positive, negative, ranks, mentions, news_id) values (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (keyword, pos, neg, ranks, mentions, id))
            self.db.commit()
    
    def FetchData(self,id):
        sql="SELECT contents FROM comments WHERE news_id=%s" #select 할 테이블 이름
        self.cursor.execute(sql,(id))
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
