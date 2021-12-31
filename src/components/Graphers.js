import * as d3 from "d3";
import { useRef } from "react";
import '../styleSheets/vbargraph.scss';
import useDim from "../hooks/useDim";

export const VBar=(props)=>{
    // props: {head:graph-title
    //         items: [bar-name, bar-value]}

    // max graph size is 80% of viewport width/height (TODO: ADJUST TO MAX/MIN )
    const {gWidth,gHeight}=useDim({xRatio:0.4,yRatio:0.4,xMax:800,yMax:600,xMin:400,yMin:300});
    const wid = gWidth;
    const hei = gHeight;
    console.log("graphing vertical bar graph")
    console.log("received",props.items)
    // where to attach svg
    const graphNode = useRef(null);

    // **   graph paddings   **
    // padding on both left and right side of graph
    const xPadding = 50;
    // padding on bottom of graph
    const downPadding = 50;
    // padding on top of graph
    const upPadding = 100;

    // first clear any svg present in the page
    d3.select("svg").remove();

    // attach svg to graphNode
    const svgCanv = d3.select(graphNode.current)
                        .append("svg")
                        .attr("height",hei)
                        .attr("width",wid);
    
    // **   y scale items   **                 
    // find max/min values of the given dataset
    const graphMax = d3.max(props.items,(d,i)=>parseFloat(d[1]));
    const graphMin = d3.min(props.items, (d,i)=>parseFloat(d[1]));
    // make a 0-graphmax yscale that plots 0 to (hei-downpadding) and graphmax to (uppadding)
    const yScale = d3.scaleLinear()
                        .domain([0, graphMax])
                        .range([hei-downPadding,upPadding]);

    // **   x scale items   **
    // ordinal graph tick labels
    const xAxisLabels=props.items.map((item)=>item[0]);
    // ordinal graph scale with band (TODO: make padding conditional on how big each band would be)
    const xScale = d3.scaleBand()
                    .domain(xAxisLabels)
                    .range([xPadding,wid-xPadding])
                    .paddingOuter([0.1])
                    .paddingInner([0.2]);

    // graph bars (TODO: better style, color?)
    const bars = svgCanv.selectAll("rect")
                        .data(props.items)
                        .enter()
                        .append("rect")
                        .attr("x", (d,i)=>xScale(d[0]))
                        .attr("y", (d,i)=>{
                            return yScale(d[1]);
                        })
                        .attr("width", ()=>xScale.bandwidth())
                        .attr("height", (d,i)=>{
                            return hei-downPadding-yScale(d[1]);
                        })
                        .attr("class","bar")
                        .attr("fill",(d,i)=>d[2])
                        
    // bar tooltip (TODO: style)
    bars.append("title")
        .text((d,i)=>d[1]);
    
    // **   x axis   **
    // make axis according to x ordinal scale
    const xAxis = d3.axisBottom()
                    .scale(xScale);
    // translate down to origin
    svgCanv.append("g")
            .attr("transform",`translate(0,${hei-downPadding})`)
            .call(xAxis);

    // **   y axis  **
    // make axis according to the y linear scale
    const yAxis = d3.axisLeft()
                    .scale(yScale)
                    .ticks(6);
                    
    // translate right to origin
    svgCanv.append("g")
            .attr("transform", `translate(${xPadding},0)`)
            .call(yAxis);

    // **   graph title   **
    svgCanv.append("text")
            .attr("x",wid/2)
            .attr("y",upPadding/2)
            .attr("text-anchor","middle")
            .style("font-size","24px")
            .style("text-decoration","underline")
            .text(props.head);
    
    // additional grid lines for clarity
    // made from extruded tick lines from an overlayed axis 
    // how many ticks are appropriate?
    const gridLineBase=d3.axisLeft()
                        .scale(yScale)
                        .ticks(2)
                        .tickSize((-wid+2*xPadding),0,0)
                        .tickFormat("");
    
    svgCanv.append("g")
            .attr("class","grid")
            .call(gridLineBase)
            .attr("transform",`translate(${xPadding},0)`);

    console.log("finish graph")
    return(
        <div className="vBar" ref={graphNode}>
        </div>
    )
}

export const HBar=(props)=>{


    return(
        <div>
            jinga
        </div>
    )
}
