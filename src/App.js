import React, { useState, useEffect } from 'react';
import Graph from './components/Graph';
import Survey from './components/Survey';
/* 
  Wrapper that encapsulates 2 functional components
  receives current poll JSON and renders header, <graph />, <survey />, footer
*/
const App =()=> {
  // where data to the graph display is stored
  const [poll,setPoll] = useState({"title":"", "type":"", "res":{}})
  // where data to the survey form is stored
  const [surv,setSurv] = useState({"title":"", "questions":[]})
  useEffect(() => {
    // fetch poll data
    fetch('/poll').then(res => res.json()).then(data => {
      const newPoll = {};
      newPoll.title=data.poll.title;
      newPoll.res=data.poll.res;
      newPoll.type=data.poll.type;
      setPoll(newPoll);
      const newSurv={};
      newSurv.title=data.poll.title;
      newSurv.questions=data.poll.questions;
      setSurv(newSurv);
    });
  }, []);

  return (
    <div className="poll">
      <header className="header">
        poll every day
      </header>
      <Graph poll={poll} />
      <Survey surv={surv} />
      <footer className="footer">
        footer
      </footer>
    </div>
  );
}

export default App;