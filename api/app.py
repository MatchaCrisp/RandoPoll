from flask import Flask, request
app = Flask(__name__)
from DbWorks import DbWorks
from datetime import datetime

"""
Backend API
complete sanitization and validation of user input from POST
handle valid submission by updating database
handle invalid submission gracefully
handles only approved api requests via API_KEY
return current poll result via GET
"""
glossary1={
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

glossary2={
    "type":"vbar",
    "pollTabSchema":{
        "main":"coff_tea"
    },
    "dispMsgs":{
    "coff":"Coffee",
    "tea":"Tea",
    "noth":"Neither"
    },
    "barColors":{
        "Coffee":"#634832",
        "Tea":"#b30000",
        "Neither":"#FFC0CB"
    }
}

glossary3={
    "type":"vbar",
    "pollTabSchema":{
        "main":"skyrim_age"
    },
    "dispMsgs":{
    "18min":"under 18",
    "30min":"10 to 30",
    "50min":"30 to 50",
    "65min":"50 to 65",
    "plus":"65 plus",
    "noth":"don't play skyrim"
    },
    "barColors":{
        "under 18":"#000000",
        "10 to 30":"#303030",
        "30 to 50":"606060",
        "50 to 65":"#909090",
        "65 plus":"#c0c0c0",
        "Neither":"#F0F0F0"
    }
}

@app.route('/poll', methods=["GET"])
def poll():

    dbWorker=DbWorks()
    try:
        dataPack=dbWorker.getPollResMain(datetime.today().strftime('%Y-%m-%d'), glossary3["pollTabSchema"]["main"])
        if dataPack == None:
            return None
        dataPack["poll"]["type"]=glossary3["type"]
        dataPack["poll"]["title"]=dataPack["poll"]["title"].replace("_", " ")
        dataPack["poll"]["glossary"]=glossary3["dispMsgs"]
        dataPack["poll"]["colors"]=glossary3["barColors"]

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

        return dataPack
    except:
        return None


@app.route('/submitSurv', methods=['GET','POST'])
def submitSurv():
    if request.method=='POST':
        # validation done at dbworks
        
        dbWorker=DbWorks()
        try:
            # dbworks validates pollid, and each response key/value pair
            dbWorker.insertUserInput(request.json["data"])
            return {"registered":True}
        except:
            return {"registered":False}

