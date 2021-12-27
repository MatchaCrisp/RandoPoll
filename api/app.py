from flask import Flask, request
import mysql.connector
app = Flask(__name__)
"""
Backend API
complete sanitization and validation of user input from POST
handle valid submission by updating database
handle invalid submission gracefully
handles only approved api requests via API_KEY
return current poll result via GET
"""
@app.route('/poll', methods=["GET", "POST"])
def poll():
    # case of wanting to view the curr poll
    if request.method=="GET":
        # TODO: find relevant dataset in database and return

        # sample data structure with sample data
        # TODO: add required key for required
        dataPack={
            "poll":{
                "title":"Vanilla or Chocolate Ice Cream?",
                "type":"vbar",
                "res":{
                    "Vanilla":"12",
                    "Chocolate":"11",
                    "Other flavor":"5",
                    "Not a fan of ice cream":"3"
                },
                "questions":[
                        {"questionName":"fav_cream",
                        "questionOptions":{
                            "op1_vanilla":{
                                "dispMsg":"Vanilla",
                                "inputType":"radio",
                                "inputVal":"vani"},
                            "op2_chocolate":{
                                "dispMsg":"Chocolate",
                                "inputType":"radio",
                                "inputVal":"choc"},
                            "op3_other":{
                                "dispMsg":"Other flavor",
                                "inputType":"radio",
                                "inputVal":"othe"},
                            "op4_nothing":{
                                "dispMsg":"Not a fan of ice cream",
                                "inputType":"radio",
                                "inputVal":"non"}
                            },
                        "questionReq":True
                        }
                      ]
            }
        }
        return dataPack
    # case of user submitting input
    else:
        # TODO: sanitize and validate user input
        print(request.json)
        return {"registered":True}
        # TODO: return relevant error message in case of wrong input

        # TODO: return affirmative message with valid input
    pass
