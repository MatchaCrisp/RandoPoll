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

        dataPack={
            "poll":{
                "title":"Vanilla or Chocolate Ice Cream?",
                "type":"vbar",
                "res":{
                    "Vanilla":"12",
                    "Chocolate":"11",
                    "Other flavor":"5",
                    "Not a fan of ice cream":"3"
                }
            }
        }
        return dataPack
    # case of user submitting input
    else:
        # TODO: sanitize and validate user input
        return None
        # TODO: return relevant error message in case of wrong input

        # TODO: return affirmative message with valid input
    pass
