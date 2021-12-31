import React from 'react';
import {useForm} from "react-hook-form";
import '../styleSheets/Survey.scss';

// form validation and POST back to flask backend
const Survey=({surv, submitStat, setSubmiss})=>{
    const { register, handleSubmit} = useForm();

    // first validation check: check to see if all required questions are answered
    const firstValidify=(data)=>{
        let validify = true;
        // cycle through all questions in survey
        for (const { questionName, questionReq } of surv.questions) {
            if (questionReq) {
                // case of required question not answered
                if (!(questionName in data)) {
                    validify = false;
                    break;
                }
            }
        }
        return validify;
    }

    // second validation check: check to see if all user input are part of the survey
    const secondValidify=(data)=>{
        // keep track of overall validity
        let validify=true;
        // keep track of this specific user answer validity
        let validify2 = false;
        // cycle through all user answers
        for (const questionAns in data){
            validify2=false;
            // cycle through all questions to see if it is part of survey
            for (const {questionName} of surv.questions) {
                if (questionName === questionAns){
                    validify2=true;
                    break;
                }
            }
            // case of answer not found in survey at all
            if (!validify2){
                validify=false;
                break;
            }
        }
        return validify;
    }

    // displayed when submitted
    const submitted=()=>{
        return (<div className="submitForm"><p className="submitMsg">Thank you for your submission</p></div>)
    }

    // displays when submittd form contains invalid data
    const wrongSubmit=()=>{
        return (<div className="submitForm"><p className="submitMsg">Wrong form data!</p></div>)
    }

    // displays when submission in progress
    const submitInProg=()=>{
        return <img src="https://raw.githubusercontent.com/MatchaCrisp/RandomQuote.github.io/main/src/img/loading.gif" alt="loading" />
    }

    // no submissions so far AKA the form itself
    const noSubmission = () => {
        // surv = {title:title,  
        //          questions:[{inputName:
        //                  {opId:{
        //                          dispMsg:display-msg,    
        //                          inputType:input-type,
        //                          inputVal:input-value
        //                          }
        //                   },
        //             ...]
        const jsx = [];
        // process only when data fetched 
        if (surv.questions) {
            // questions is an array containing question objects
            // {questionName:name,
            //  questionOptions:{op1_id:{dispMsg,inputType,inputVal},
            // questionReq:bool}
            // for each question object, destructure into each key
            for (const { questionName, questionOptions, questionReq } of surv.questions) {
                for (const optionId in questionOptions) {
                    // destructure each question id 
                    const { dispMsg, inputType, inputVal } = questionOptions[optionId];
                    const inp = <label
                        htmlFor={optionId}
                        key={`${optionId}Label`}><input
                            type={inputType}
                            id={optionId}
                            key={`${optionId}Option`}
                            {...register(questionName, { required: questionReq })}
                            value={inputVal} />{dispMsg}
                    </label>

                    jsx.push(inp);

                }
            }
        }
    
        return (<div className="submitForm">
            <h2 className="survTitle">{surv.title}</h2>
            <form onSubmit={handleSubmit((data) => {
                // rudimentary data validation again
                // validate all required questions are answered
                // redundancy 

                // when all required questions are answered make sure questions not apart of the survey aren't apart of the user data
                if (!firstValidify(data)) {
                    return;
                }

                if (!secondValidify(data)) {
                    return;
                }
                // rudimentary input validation passed, posting to backend
                // TODO: post
                data["pollId"] = surv.pollId
                const userData = {
                    method: 'POST',
                    headers: { 'Content-type': 'application/json' },
                    body: JSON.stringify({ data })
                };
                setSubmiss(2);
                // change into waiting state
                fetch('/submitSurv', userData)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data["registered"] === true) {
                            setSubmiss(1);
                        }
                        else {
                            setSubmiss(3);
                            setTimeout(() => {
                                setSubmiss(0);
                            }, 3000);

                        }
                    })


            })}>
                {jsx}
                <input type="submit" value="Submit!"/>
            </form>
        </div>)
    } 

    // form only rendered when never submitted
    if (submitStat === 1){
        return submitted();
    }
    else if (submitStat === 2){
        return submitInProg();
    }
    else if (submitStat === 3){
        return wrongSubmit();
    }
    else {
        return noSubmission();
    }

}

export default Survey;