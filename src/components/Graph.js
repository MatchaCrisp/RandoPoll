import React from "react";
import {VBar, HBar} from "./Graphers";

const Graph =(props)=>{
    const graphs={
        vbar:VBar,
        hbar:HBar
    }
    console.log("received:",props)
    // graph header
    const head = props.poll.title;

    // graph option and votes pair
    const items=[];
    for (const key in props.poll.res){
        items.push([key,props.poll.res[key]]);
    }
    // create proper graph based on required poll type dynamically
    console.log(props.poll.type)
    let graph;
    if (!props.poll.type){
        graph = <div>Loading</div>
    }
    else {
        graph = React.createElement(
            graphs[props.poll.type],
            {head:head,items:items});
    }
    
    return (
        <div>
            {graph}
        </div>
        
    )
}

export default Graph;