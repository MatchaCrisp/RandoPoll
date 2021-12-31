from flask import Flask, request
app = Flask(__name__)
from DbWorks import DbWorks
from datetime import datetime
import re
"""
Backend API
complete sanitization and validation of user input from POST
handle valid submission by updating database
handle invalid submission gracefully
handles only approved api requests via API_KEY
return current poll result via GET
"""
glossary={
    "type":"vbar",
    "pollTabSchema":{
        "main":"fav_cream"
    },
    "dispMsgs":{
    "vani":"Vanilla",
    "choc":"Chocolate",
    "othe":"Other flavor",
    "noth":"Not a fan of ice cream"
    },
    "barColors":{
        "Vanilla":"#fdf6f6",
        "Chocolate":"#857063",
        "Other flavor":"#FFC0CB",
        "Not a fan of ice cream":"#272643"
    }
}
@app.route('/poll', methods=["GET"])
def poll():

    dbWorker=DbWorks()
    try:
        dataPack=dbWorker.getPollResMain(datetime.today().strftime('%Y-%m-%d'), glossary["pollTabSchema"]["main"])
        if dataPack == None:
            return None
        dataPack["poll"]["type"]=glossary["type"]
        dataPack["poll"]["title"]=dataPack["poll"]["title"].replace("_", " ")
        dataPack["poll"]["glossary"]=glossary["dispMsgs"]
        dataPack["poll"]["colors"]=glossary["barColors"]

        return dataPack
    except:
        return None


        

@app.route('/surv', methods=['GET'])
def surv():
    dbWorker=DbWorks()
    try:
        dataPack=dbWorker.getPollSurvMain(datetime.today().strftime('%Y-%m-%d'))
        if dataPack == None:
            return None
        dataPack["surv"]["title"]=dataPack["surv"]["title"].replace("_", " ")
        print(dataPack,"flask")
        return dataPack
    except:
        return None


@app.route('/submitSurv', methods=['GET','POST'])
def submitSurv():
    if request.method=='POST':
        # validation done at dbworks
        print(request.json)
        
        dbWorker=DbWorks()
        try:
            # dbworks validates pollid, and each response key/value pair
            dbWorker.insertUserInput(request.json["data"])
            return {"registered":True}
        except:
            return {"registered":False}

