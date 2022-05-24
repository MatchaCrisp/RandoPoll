// external
// react
import React from "react";
// internal
// components
import {VBar, HBar} from "./Graphers";
// stylesheet
import '../styleSheets/Graph.scss';
// renders the correct graph based on type passed in by JSON
const Graph =(props)=>{
    const graphs={
        vbar:VBar,
        hbar:HBar
    }
    
    // create proper graph based on required poll type dynamically
    let graph;
    if (!props.poll.type){
        graph = <img src="https://raw.githubusercontent.com/MatchaCrisp/RandoPoll/main/src/img/loading.gif" alt="loading" className="loading"/>
    }
    else {
        // graph header
        const head = props.poll.title;

        // graph option and votes pair
        const items=[];
        for (const key in props.poll.res){
            items.push([key,props.poll.res[key],props.poll.colors[key]]);
        }

        graph = React.createElement(
            graphs[props.poll.type],
            {head:head,items:items});
    }
    
    return (
        <div className="graphContainer">
            {graph}
        </div>
        
    )
}

export default Graph;