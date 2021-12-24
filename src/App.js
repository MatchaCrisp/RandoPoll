import React, { useState, useEffect } from 'react';
import Graph from './components/Graph';
import Survey from './components/Survey';
/* 
  Wrapper that encapsulates 2 functional components
  receives current poll JSON and renders header, <graph />, <survey />, footer
*/
const App =()=> {
  const [poll,setPoll] = useState({"title":"", "res":{}})
  const [surv,setSurv] = useState({"title":"", "ops":[]})
  useEffect(() => {
    fetch('/poll').then(res => res.json()).then(data => {
      setPoll(data.poll);
      setSurv({
        "title":data.poll.title,
        "ops":Object.keys(data.poll.res)
      });
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