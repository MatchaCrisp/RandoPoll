import React, {useState} from 'react';
import {useForm} from "react-hook-form";

// TODO: integrate react-hook-form with dynamic form creation
// form validation and POST back to flask backend
const Survey=({surv})=>{
    const [submitStat, setSubmitStat]=useState(false);
    // surv = {title:title,  
    //          questions:[{inputName:
    //                  {opId:{
    //                          dispMsg:display-msg,    
    //                          inputType:input-type,
    //                          inputVal:input-value
    //                          }
    //                   },
    //             ...]
    const { register, handleSubmit} = useForm();
    console.log("received survey data")
    console.log(surv)
    const jsx = [];
    // process only when data fetched 
    if (surv.questions){
        // questions is an array containing question objects
        // {questionName:name,
        //  questionOptions:{op1_id:{dispMsg,inputType,inputVal},
        // questionReq:bool}
        // for each question object, destructure into each key
        for (const {questionName, questionOptions, questionReq} of surv.questions){
            for (const optionId in questionOptions){
                // destructure each question id 
                const {dispMsg,inputType,inputVal} = questionOptions[optionId];
                const inp = <input
                    type={inputType}
                    id={optionId}
                    key={`${optionId}Option`}
                    {...register(questionName, { required: questionReq})}
                    value={inputVal} />
                const lab = <label
                    htmlFor={optionId}
                    key={`${optionId}Label`}>
                    {dispMsg}
                </label>
                jsx.push(inp);
                jsx.push(lab);
            }
        }
    }

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
    const submittedJsx=<p>Thank you for your submission</p>

    // form 
    const noSubmission = <div>
        {surv.title}
        <form onSubmit={handleSubmit((data) => {
            // rudimentary data validation again
            console.log("user input: ", data);
            // validate all required questions are answered
            // redundancy 

            // when all required questions are answered make sure questions not apart of the survey aren't apart of the user data
            if (!firstValidify(data)) {
                return;
            }
            console.log("pass first check");

            if (!secondValidify(data)) {
                return;
            }
            console.log("pass second check")
            // rudimentary input validation passed, posting to backend
            // TODO: post
            const userData = {
                method: 'POST',
                headers: { 'Content-type':'application/json'},
                body: JSON.stringify(data)
            };
            // change into waiting state
            fetch('/poll', userData)
                .then(response=>response.json())
                .then(data=>{
                    console.log(data);
                    setSubmitStat(true);
                })

            
        })}>
            {jsx}
            <input type="submit" />
        </form>
    </div>
    // form only rendered when never submitted
    if (submitStat){
        return submittedJsx;
    }
    else {
        return noSubmission;
    }

}

export default Survey;