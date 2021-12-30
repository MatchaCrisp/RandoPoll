from flask import Flask, request
app = Flask(__name__)
from DbWorks import DbWorks
"""
Backend API
complete sanitization and validation of user input from POST
handle valid submission by updating database
handle invalid submission gracefully
handles only approved api requests via API_KEY
return current poll result via GET
"""

@app.route('/poll', methods=["GET"])
def poll():

    # TODO: find relevant dataset in database and return
    dbWorker=DbWorks()
    # sample data structure with sample data
    dataPack = {
        "poll": {
            "pollId": "1",
            "title": "Vanilla or Chocolate Ice Cream?",
            "type": "vbar",
            "res": {
                    "Vanilla": "12",
                    "Chocolate": "11",
                    "Other flavor": "5",
                    "Not a fan of ice cream": "3"
            }

        }
    }
    return dataPack

        

@app.route('/surv', methods=['GET'])
def surv():
    dataPack = {
        "surv":{
            "pollId": "1",
            "title": "Vanilla or Chocolate Ice Cream?",
            "questions": [
             {"questionName": "fav_cream",
              "questionOptions": {
                  "op1_vanilla": {
                      "dispMsg": "Vanilla",
                      "inputType": "radio",
                      "inputVal": "vani"},
                  "op2_chocolate": {
                      "dispMsg": "Chocolate",
                      "inputType": "radio",
                      "inputVal": "choc"},
                  "op3_other": {
                      "dispMsg": "Other flavor",
                      "inputType": "radio",
                      "inputVal": "othe"},
                  "op4_nothing": {
                      "dispMsg": "Not a fan of ice cream",
                      "inputType": "radio",
                      "inputVal": "noth"}
              },
                 "questionReq": True
              }
         ]}
    }

    return dataPack


@app.route('/submitSurv', methods=['GET','POST'])
def submitSurv():
    if request.method=='POST':
        # TODO: sanitize and validate user input
        print(request.json)
        
        # 1: connect to database and fetch relevant datapack 
        # TODO: return relevant error message in case of wrong input

        # TODO: return affirmative message with valid input
        return {"registered":True}

