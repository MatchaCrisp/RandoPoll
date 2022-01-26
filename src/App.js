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

      const newPoll = {};
      newPoll.pollId=poll.pollId;
      newPoll.title=poll.title;
      newPoll.colors=poll.colors;
      const newRes={}
      for (const resKey in poll.glossary){
        newRes[poll.glossary[resKey]]=(resKey in poll.res)?poll.res[resKey]:0;
      }
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

        const newPoll = {};
        newPoll.pollId = poll.pollId;
        newPoll.title = poll.title;
        newPoll.colors = poll.colors;
        const newRes = {}
        for (const resKey in poll.glossary){
          newRes[poll.glossary[resKey]]=(resKey in poll.res)?poll.res[resKey]:0;
        }

        newPoll.res = newRes;
        newPoll.type = poll.type;
        setPoll(newPoll);
      });
    }

  },[submiss]);

  const renderGraph=()=>{
    if (!poll){
      return <p>Oops! No graph data were found.</p>
    }
    return <Graph poll={poll} />
  }

  const renderSurvey=()=>{
    if (!surv){
      return <p>Oops! No survey questions were found</p>
    }
    return <Survey surv={surv} setSubmiss={setSubmiss} submitStat={submiss}/>
  }
  return (
    <div className="poll">
      <header className="header">
        <h1>RandoPoll</h1>
        <a href="https://github.com/MatchaCrisp/RandoPoll" target="_blank" rel="noreferrer"><i className="fab fa-github"></i></a>
      </header>
      {renderGraph()}
      {renderSurvey()}
      <footer className="footer">

      </footer>
    </div>
  );
}

export default App;