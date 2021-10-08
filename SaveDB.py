import pymysql
from TextManager import TextManager

class saveDB:
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

    def initDB(self):
        self.cursor.execute("CREATE TABLE keywords(id INT AUTO_INCREAMENT, keyword VARCHAR(100), positive FLOAT, negative FLOAT, rank INT, mentions INT")
        self.db.commit()

    def saveDB(self,keywordList,valueList):
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
            sql="""insert into KEYWORDS (keyword, positive, negative, ranks, mentions) values (%s, %s, %s, %s, %s)"""
            #sql="""INSERT INTO keywords VALUES('{}','{}','{}');""".format(keyword, rank, mentions)
            self.cursor.execute(sql, (keyword, pos, neg, ranks, mentions))
            self.db.commit()

    def savePredictDB(self,valueList):
        for value in valueList:
            if value < 0.5:
                value=(1-value)*100
                neg= round(value,2)
                pos= 100-neg
                print(neg)
            else:
                value=value*100
                pos= round(value,2)
                neg= 100-pos
                print(neg)
            sql="""update KEYWORDS (positive, negative) values (%s, %s)"""
            self.cursor.execute(sql, (pos, neg))
            self.db.commit()

#tx=TextManager()
#db=saveDB()
#keyword=tx.ExtractKeyword('./test.csv',10)
#db.initDB()
#db.saveKeywordDB(keyword)
#db.savePredictDB(valueList)