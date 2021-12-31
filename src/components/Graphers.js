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

    // where to attach svg
    const graphNode = useRef(null);

    // **   graph paddings   **
    const paddings={left:50,up:100,right:50,down:50};

    // first clear any svg present in the page
    d3.select("svg").remove();

    // attach svg to graphNode
    const svgCanv = d3.select(graphNode.current)
                        .append("svg")
                        .attr("height",hei)
                        .attr("width",wid);
    
    // **   y scale items   **                 
    // find max values of the given dataset
    const graphMax = d3.max(props.items,(d,i)=>parseFloat(d[1]));

    // make a 0-graphmax yscale that plots 0 to (hei-paddings.down) and graphmax to (paddings.up)
    const yScale = d3.scaleLinear()
                        .domain([0, graphMax])
                        .range([hei-paddings.down,paddings.up]);

    // **   x scale items   **
    // ordinal graph tick labels
    const xAxisLabels=props.items.map((item)=>item[0]);
    // ordinal graph scale with band (TODO: make padding conditional on how big each band would be)
    const xScale = d3.scaleBand()
                    .domain(xAxisLabels)
                    .range([paddings.left,wid-paddings.right])
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
                            return hei-paddings.down-yScale(d[1]);
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
            .attr("transform",`translate(0,${hei-paddings.down})`)
            .call(xAxis);

    // **   y axis  **
    // make axis according to the y linear scale
    const yAxis = d3.axisLeft()
                    .scale(yScale)
                    .ticks(6);
                    
    // translate right to origin
    svgCanv.append("g")
            .attr("transform", `translate(${paddings.left},0)`)
            .call(yAxis);

    // **   graph title   **
    svgCanv.append("text")
            .attr("x",wid/2)
            .attr("y",paddings.up/2)
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
                        .tickSize((-wid+paddings.left+paddings.right),0,0)
                        .tickFormat("");
    
    svgCanv.append("g")
            .attr("class","grid")
            .call(gridLineBase)
            .attr("transform",`translate(${paddings.left},0)`);

    return(
        <div className="vBar" ref={graphNode}>
        </div>
    )
}

export const HBar=(props)=>{


    return(
        <div>
        </div>
    )
}
