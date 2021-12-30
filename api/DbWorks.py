import psycopg2
from config import config
import re
import json
from psycopg2.extensions import AsIs,quote_ident
class DbWorks:
    # establish connection to database described in config
    def __init__(self):
        self.conn=None
        self.cur=None
        try:
            params=config()
            print("testing connection")
            self.conn=psycopg2.connect(**params)
            self.cur=self.conn.cursor()
            print("connection successful")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    # disconnect before destruction
    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print('db connection broken, stopping dbWorks')

    # print version of connected db
    def dbInfo(self):
        if self.conn is not None and self.cur is not None:
            self.cur.execute('SELECT version()')
            version = self.cur.fetchone()
            return version
        else:
            return None

    # print schema of connected db
    def schema(self):
        if self.conn is not None and self.cur is not None:
            self.cur.execute(
                'SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\' ORDER BY tables.table_name')
            schema=self.cur.fetchall()
            return schema
        else:
            return None

    # TODO: one exposed API for doing all poll initializing
    def initializePoll(self,pollObj):
        pollTitle=pollObj["pollTitle"]
        pollTab=pollObj["pollTab"]
        survTab=pollObj["survTab"]
        pollStart=pollObj["pollStart"]
        pollEnd=pollObj["pollEnd"]

        # input validations
        if not re.match("^[\w]+$", pollTab) or not re.match("^[\w]+$", survTab) or not re.match("^[\w]+$", pollTitle) or not re.match("^\d{4}-\d{2}-\d{2}$", pollStart) or not re.match("^\d{4}-\d{2}-\d{2}$", pollEnd):
            raise ValueError("incorrect input/input format")

        answers=[]
        questions=[] 
        for quest in pollObj["pollQuestions"]:
            # input validations
            if "inputName" not in quest or "returnType" not in quest or "isReq" not in quest or "options" not in quest:
                raise KeyError("incorrect dict format")
            if quest["inputName"]==None or quest["returnType"]==None or quest["isReq"]==None or quest["options"]==None:
                raise ValueError("incorrect input/input format")
            answer={"inputName":quest["inputName"],
                    "returnType":quest["returnType"],
                    "isReq":quest["isReq"]}
            question={"inputName":quest["inputName"],
                      "options":quest["options"],
                      "isReq":quest["isReq"]}
            answers.append(answer)
            questions.append(question)
        
        # make sure connection is healthy
        if self.conn is None or self.cur is None:
            raise RuntimeError("database connection not established")
        try:
            # insert new row in polls to indicate new poll start
            sqlNewPoll="INSERT INTO polls (poll_table, surv_table, poll_title, poll_start, poll_end) VALUES (%s, %s, %s, %s, %s);"
            print(sqlNewPoll)
            newPollParam=[pollTab, survTab, pollTitle, pollStart, pollEnd]
            self.cur.execute(sqlNewPoll, newPollParam)

            # make new poll result table
            sqlNewPollRes="CREATE TABLE IF NOT EXISTS %s (res_id SERIAL PRIMARY KEY, "
            newPollResParam=[]
            newPollResParam.append(AsIs(pollTab))

            # for each answer column add one more line
            for answer in answers:
                sqlNewPollRes+="%s %s %s, "
                newPollResParam.append(AsIs(answer['inputName']))
                newPollResParam.append(AsIs(answer['returnType']))
                newPollResParam.append((AsIs('NOT NULL')) if answer['isReq'] else (AsIs('')))
            # remove last ","
            sqlNewPollRes=sqlNewPollRes[:-2]
            # add finish to query
            sqlNewPollRes+=");"
            print(sqlNewPollRes)
            self.cur.execute(sqlNewPollRes,newPollResParam)

            # make new poll question table
            sqlNewPollQuest="CREATE TABLE IF NOT EXISTS %s (que_id SERIAL PRIMARY KEY, name TEXT NOT NULL, options JSONB NOT NULL, is_req BOOLEAN NOT NULL);"
            print(sqlNewPollQuest)
            self.cur.execute(sqlNewPollQuest,(AsIs(survTab),))

            # insert each question requirement into new poll question table
            sqlNewQuestions="INSERT INTO %s (name, options, is_req) VALUES "
            newQuestParam=[]
            newQuestParam.append(AsIs(survTab))
            for question in questions:
                newQuestion="(%s, %s, %s), "
                sqlNewQuestions+=newQuestion
                newQuestParam.append(question['inputName'])

                newQuestParam.append(json.dumps(question['options']))
                newQuestParam.append('TRUE' if question['isReq'] else 'FALSE')
            sqlNewQuestions=sqlNewQuestions[:-2]
            sqlNewQuestions+=";"
            print(sqlNewQuestions)
            self.cur.execute(sqlNewQuestions,newQuestParam)

            # commit
            self.conn.commit()

            print("finish")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
          
    # TODO: update poll_res based on valid input
    # validate input here again
    def insertUserInput(self,input):
        if "pollId" not in input:
            raise ValueError("pollId not found")

        # make sure connection is healthy
        if self.conn is None or self.cur is None:
            raise RuntimeError("database connection not established")    
        try:
            pollId=int(input["pollId"])
            # remove pollId from dict for ease of later looping
            del input["pollId"]
            # find correct table to insert
            pollTableQuery="SELECT poll_table FROM polls WHERE poll_id = %s;"
            print(pollTableQuery)
            self.cur.execute(pollTableQuery,(pollId,))
            pollTable=self.cur.fetchone()[0]
            
            # start insert query construction
            insertQuery="INSERT INTO %s ("
            insertQueryParam=[]
            insertQueryParam.append(AsIs(pollTable))
            # loop over every key to grab column name
            for col in input:
                insertQuery+="%s, "
                insertQueryParam.append(AsIs(col))
            insertQuery=insertQuery[:-2]
            insertQuery+=") VALUES ("
            for col in input:
                insertQuery+="%s, "
                insertQueryParam.append(input[col])
            insertQuery=insertQuery[:-2]
            insertQuery+=");"
            print(insertQuery)
            self.cur.execute(insertQuery,insertQueryParam)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def initPoll(self):
        pollQ="CREATE TABLE IF NOT EXISTS polls (poll_id SERIAL PRIMARY KEY, poll_table TEXT NOT NULL, surv_table TEXT NOT NULL, poll_title TEXT NOT NULL, poll_start DATE NOT NULL, poll_end DATE NOT NULL);"
        # make sure connection is healthy
        if self.conn is None or self.cur is None:
            raise RuntimeError("database connection not established")
        try:
            self.cur.execute(pollQ)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def giveCur(self):
        return self.cur
worker=DbWorks()

jinga={'pollTitle':'chocolate_vs_vanilla_ice_cream',
       'pollTab':'fav_cream_res',
       'survTab':'fav_cream_quest',
       'pollStart':'2021-12-29',
       'pollEnd':'2022-01-05',
       'pollQuestions':[
           {'inputName':'fav_cream',
            'returnType':'TEXT',
            'options':{
                        'op1_vanilla':{'dispMsg':'vanilla','inputType':'radio','inputVal':'vani'},
                        'op2_chocolate':{'dispMsg':'chocolate','inputType':'radio','inputVal':'choc'},
                        'op3_other':{'dispMsg':'other flavor','inputType':'radio','inputVal':'othe'},
                        'op4_nothing':{'dispMsg':'not a fan of ice cream','inputType':'radio','inputVal':'noth'}
                      },
            'isReq':True
           }
       ]
    }
# worker.initializePoll(jinga)
