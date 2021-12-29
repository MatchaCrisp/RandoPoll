import psycopg2
from config import config
import re
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
            schema=self.cur.fetchone()
            return schema
        else:
            return None

    # TODO: update polls based on valid input
    def newPoll(self, pollTab,survTab,pollTitle,pollStart,pollEnd):
        # input validations
        if not re.match("^[\w]+", pollTab):
            return False
        if not re.match("^[\w]+", survTab):
            return False
        if not re.match("^[\w]+", pollTitle):
            return False
        if not re.match("^\d{4}-\d{2}-\d{2}$", pollStart):
            return False
        if not re.match("^\d{4}-\d{2}-\d{2}$", pollEnd):
            return False
        
        sqlTemp='INSERT INTO polls (poll_table, surv_table, poll_title, poll_start, poll_end) VALUES (%s, %s, %s, %s, %s);' % (
                pollTab, survTab, pollTitle, pollStart, pollEnd)
        print(sqlTemp)
        if self.conn is not None and self.cur is not None:
            self.cur.execute(sqlTemp)
            return True
        
        return False
    # TODO: create poll_res table given series of arguments
    def newPollResTable(self,pollTab,answers):
        # input validations
        if not re.match("^[\w]+", pollTab):
            return False
        if answers.length>0:
            for answer in answers:
                if len(answer) != 3:
                    return False
        else:
            return False
        # start query build
        sqlTemp="CREATE TABLE [IF NOT EXISTS] %s (res_id SERIAL PRIMARY KEY, " % (pollTab)
        # for each answer column add one more line
        for answer in answers:
            sqlTemp+="%s %s %s, " % (answer.inputName, answer.returnType, "NOT NULL" if answer.isReq else "")
        # remove last ","
        sqlTemp=sqlTemp[:-1]
        # add finish to query
        sqlTemp+=");"

        print(sqlTemp)

        if self.conn is not None and self.cur is not None:
            self.cur.execute(sqlTemp)
            return True
        
        return False

        
    # TODO: create poll_que table given series of arguments
    def newPollQueTable(self,survTab,questions):
        # input validations
        if not re.match("^[\w]+", survTab):
            return False
        if questions.length>0:
            for question in questions:
                if len(question) != 3:
                    return False
        else:
            return False
        # start query build
        sqlTemp="CREATE TABLE [IF NOT EXISTS] %s (res_id SERIAL PRIMARY KEY, name TEXT NOT NULL, options JSONB NOT NULL, is_req BOOLEAN NOT NULL);" % (survTab)
        print(sqlTemp)
        if self.conn is not None and self.cur is not None:
            self.cur.execute(sqlTemp)
            # insert into table as row
            for question in questions:
                newQuestion="INSERT INTO %s (name, options, is_req) VALUES (%s, %s, %s);" % (survTab, question.inputName, question.options, "TRUE" if question.isReq else "FALSE")
                print(newQuestion)
                self.cur.execute(newQuestion)
            return True
        else:
            return False
       
    # TODO: update poll_res based on valid input

worker=DbWorks()

print(worker.dbInfo())
print(worker.schema())