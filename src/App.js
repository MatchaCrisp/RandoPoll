import React, { useState, useEffect } from 'react';
import Graph from './components/Graph';
import Survey from './components/Survey';
import './styleSheets/App.scss';
/* 
  Wrapper that encapsulates 2 functional components
  receives current poll JSON and renders header, <graph />, <survey />, footer
*/
const App =()=> {
  // where data to the graph display is stored
  const [poll,setPoll] = useState({"title":"", "type":"", "res":{}})
  // where data to the survey form is stored
  const [surv,setSurv] = useState({"title":"", "questions":[]})
  // form submission status
  const [submiss,setSubmiss]=useState(0);

  // const submissionStates={0:"no submissions", 1:"submission success", 2:"submission in progress", 3:"wrong form input"};
  useEffect(() => {
    // fetch poll data
    fetch('/poll').then(res => res.json()).then(({poll}) => {
      console.log(poll)
      const newPoll = {};
      newPoll.pollId=poll.pollId;
      newPoll.title=poll.title;
      newPoll.colors=poll.colors;
      const newRes={}
      for (const resKey in poll.res){
        console.log(resKey)
        console.log(poll.glossary[resKey],poll.res[resKey])
        newRes[poll.glossary[resKey]]=poll.res[resKey];
      }
      console.log(newRes)
      newPoll.res=newRes;
      newPoll.type=poll.type;
      setPoll(newPoll);
    });
    
  }, []);

  useEffect(()=>{
    // case of no submission AKA display survey form
    if (submiss === 0) {
      //fetch surv questions
      // TODO: when login/cookie implemented, only fetch when user never submitted before
      fetch('/surv').then(res => res.json()).then(({ surv }) => {
        const newSurv = {};
        newSurv.pollId = surv.pollId;
        newSurv.title = surv.title;
        newSurv.questions = surv.questions;
        setSurv(newSurv);
      });
    }
    // case of successful submission AKA refetch poll results
    else if (submiss === 1) {
      fetch('/poll').then(res => res.json()).then(({ poll }) => {
        console.log(poll)
        const newPoll = {};
        newPoll.pollId = poll.pollId;
        newPoll.title = poll.title;
        newPoll.colors = poll.colors;
        const newRes = {}
        for (const resKey in poll.res) {
          console.log(resKey)
          console.log(poll.glossary[resKey], poll.res[resKey])
          newRes[poll.glossary[resKey]] = poll.res[resKey];
        }
        console.log(newRes)
        newPoll.res = newRes;
        newPoll.type = poll.type;
        setPoll(newPoll);
      });
    }

  },[submiss]);
  return (
    <div className="poll">
      <header className="header">
        <h1>RandoPoll</h1>
        <a href="https://www.github.com"><i className="fab fa-github"></i></a>
      </header>
      <Graph poll={poll} />
      <Survey surv={surv} setSubmiss={setSubmiss} submitStat={submiss}/>
      <footer className="footer">

      </footer>
    </div>
  );
}

export default App;