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
            DATABASE_URL='postgres://fhfowpfvftednf:e589aac2b9c183f4d3353634d49e0005a916a68b84b1bd9b883d68a296d0f000@ec2-18-211-185-154.compute-1.amazonaws.com:5432/d1upk6nq13jqdr'

            print("testing connection")

            # establish connection and set cursor
            self.conn=psycopg2.connect(DATABASE_URL,sslmode='require')
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
        # make sure connection is healthy
        if self.conn is None or self.cur is None:
            raise RuntimeError("database connection not established")
        try:
            self.cur.execute('SELECT version()')
            version = self.cur.fetchone()
            return version
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # print schema of connected db
    def schema(self):
        # make sure connection is healthy
        if self.conn is None or self.cur is None:
            raise RuntimeError("database connection not established")
        try:
            self.cur.execute(
                'SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\' ORDER BY tables.table_name')
            schema=self.cur.fetchall()
            return schema
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # one exposed API for doing all poll initializing
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
        # gather relevant info for res_table into answers, and relevant info for question_table into questions
        for quest in pollObj["pollQuestions"]:
            # input validations
            if "inputName" not in quest or "returnType" not in quest or "isReq" not in quest or "options" not in quest:
                raise KeyError("incorrect dict format")
            # TODO: more specific validations
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

            self.cur.execute(sqlNewPollRes,newPollResParam)

            # make new poll question table
            sqlNewPollQuest="CREATE TABLE IF NOT EXISTS %s (que_id SERIAL PRIMARY KEY, name TEXT NOT NULL, options JSONB NOT NULL, is_req BOOLEAN NOT NULL);"

            self.cur.execute(sqlNewPollQuest,(AsIs(survTab),))

            # insert each question requirement into new poll question table
            sqlNewQuestions="INSERT INTO %s (name, options, is_req) VALUES "
            newQuestParam=[]
            newQuestParam.append(AsIs(survTab))
            # for each additional question add another row
            for question in questions:
                newQuestion="(%s, %s, %s), "
                sqlNewQuestions+=newQuestion
                newQuestParam.append(question['inputName'])

                newQuestParam.append(json.dumps(question['options']))
                newQuestParam.append('TRUE' if question['isReq'] else 'FALSE')
            sqlNewQuestions=sqlNewQuestions[:-2]
            sqlNewQuestions+=";"

            self.cur.execute(sqlNewQuestions,newQuestParam)

            # commit
            self.conn.commit()


        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # validate input here again
    def insertUserInput(self,input):
        # validate pollId
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

            self.cur.execute(pollTableQuery,(pollId,))
            pollTable=self.cur.fetchone()[0]
            
            # start insert query construction
            insertQuery="INSERT INTO %s ("
            insertQueryParam=[]
            insertQueryParam.append(AsIs(pollTable))
            # loop over every key to grab column name
            for col in input:
                # validate format of col (\w)
                if not re.match("^[\w\d]+$", col):
                    # case of special characters getting in
                    raise ValueError("incorrect column format")
                insertQuery+="%s, "
                insertQueryParam.append(AsIs(col))
            insertQuery=insertQuery[:-2]
            insertQuery+=") VALUES ("
            for col in input:
                # validate col data
                if not re.match("^[\w\d]+$",input[col]):
                    # case of special characters getting in
                    raise ValueError("incorrect column data format")
                insertQuery+="%s, "
                insertQueryParam.append(input[col])
            insertQuery=insertQuery[:-2]
            insertQuery+=");"

            self.cur.execute(insertQuery,insertQueryParam)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # only used to start new polls table 
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

    # returns dataPack formed to the order of backend /poll
    def getPollResMain(self,date,aggCol):
        # input validation
        if not re.match("^\d{4}-\d{2}-\d{2}$",date):
            raise ValueError("incorrect date/date format")
        if not re.match("^[\w]+$",aggCol):
            raise ValueError("incorrect column name/format")
        try:
            dataPack={
                "poll":{
                    "pollId":"",
                    "title":"",
                    "res":{}
                }
            }
            # make query to select the correct pollTable
            pollTabQuery="SELECT poll_id, poll_title, poll_table FROM polls WHERE to_date(%s,'YYYY-MM-DD') >= poll_start AND to_date(%s, 'YYYY-MM-DD') <= poll_end;"
            self.cur.execute(pollTabQuery,(date,date,))
            qRes = self.cur.fetchone()
            if qRes == None:
                return None
            dataPack["poll"]["pollId"]=qRes[0]
            dataPack["poll"]["title"]=qRes[1]
            pollTab=qRes[2]
            resQuery="SELECT %s, COUNT(%s) FROM %s GROUP BY %s;"
            self.cur.execute(resQuery,(AsIs(aggCol), AsIs(aggCol), AsIs(pollTab), AsIs(aggCol),))
            qpRes = json.loads(json.dumps(self.cur.fetchall()))

            for res in qpRes:
                dataPack["poll"]["res"][res[0]]=res[1]
            return dataPack
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    # returns dataPack formed to the order of backend /surv
    def getPollSurvMain(self,date):
        # input validation
        if not re.match("^\d{4}-\d{2}-\d{2}$",date):
            raise ValueError("incorrect date/date format")

        try:
            dataPack={
                "surv":{
                    "pollId":"",
                    "title":"",
                    "questions":[]
                }
            }
            # make query to select the correct pollTable
            pollTabQuery="SELECT poll_id, poll_title, surv_table FROM polls WHERE to_date(%s,'YYYY-MM-DD') >= poll_start AND to_date(%s, 'YYYY-MM-DD') <= poll_end;"
            self.cur.execute(pollTabQuery,(date,date,))
            qRes = self.cur.fetchone()
            if qRes == None:
                return None
            dataPack["surv"]["pollId"]=qRes[0]
            dataPack["surv"]["title"]=qRes[1]
            survTab=qRes[2]
            resQuery="SELECT name, options, is_req FROM %s;"
            self.cur.execute(resQuery,(AsIs(survTab),))

            for row in self.cur:

                question={"questionName":row[0],
                          "questionOptions":row[1],
                          "questionReq":row[2]}
                dataPack["surv"]["questions"].append(question)

            return dataPack
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

poll1={'pollTitle':'chocolate_vs_vanilla_ice_cream',
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

poll2={'pollTitle':'coffee_or_tea',
       'pollTab':'coff_tea_res',
       'survTab':'coff_tea_quest',
       'pollStart':'2022-01-06',
       'pollEnd':'2022-01-12',
       'pollQuestions':[
           {'inputName':'coff_tea',
            'returnType':'TEXT',
            'options':{
                        'op1_coffee':{'dispMsg':'coffee','inputType':'radio','inputVal':'coff'},
                        'op2_tea':{'dispMsg':'tea','inputType':'radio','inputVal':'tea'},
                        'op3_nothing':{'dispMsg':'neither','inputType':'radio','inputVal':'noth'}
                      },
            'isReq':True
           }
       ]
    }

poll3={'pollTitle':'skyim_player_age',
       'pollTab':'skyrim_age_res',
       'survTab':'skyrim_age_quest',
       'pollStart':'2022-01-13',
       'pollEnd':'2022-01-19',
       'pollQuestions':[
           {'inputName':'skyrim_age',
            'returnType':'TEXT',
            'options':{
                        'op1_18':{'dispMsg':'under 18','inputType':'radio','inputVal':'18min'},
                        'op2_30':{'dispMsg':'18 to 30','inputType':'radio','inputVal':'30min'},
                        'op3_50':{'dispMsg':'30 to 50','inputType':'radio','inputVal':'50min'},
                        'op3_65':{'dispMsg':'50 to 65','inputType':'radio','inputVal':'65min'},
                        'op3_plus':{'dispMsg':'65 plus','inputType':'radio','inputVal':'plus'},
                        'op3_noth':{'dispMsg':'neither','inputType':'radio','inputVal':'noth'}
                      },
            'isReq':True
           }
       ]
    }

worker=DbWorks()
# 22-01-06 -> 22-01-12
# worker.initializePoll(poll2)

# 22-01-13 -> 22-01-19
# worker.initializePoll(poll3)
