import * as d3 from "d3";
import { useRef } from "react";
import '../styleSheets/vbargraph.css';
import useDim from "../hooks/useDim";

export const VBar=(props)=>{
    // props: {head:graph-title
    //         items: [bar-name, bar-value]}
    console.log(`constructing vertical bar graph from ${props.items}`)
    const {gWidth,gHeight}=useDim({xRatio:0.8,yRatio:0.8});
    const graphNode = useRef(null);
    const xPadding = 50;
    const downPadding = 50;
    const upPadding = 100;
    const wid = gWidth;
    const hei = gHeight;
    d3.select("svg").remove();
    const svgCanv = d3.select(graphNode.current)
                        .append("svg")
                        .attr("height",hei)
                        .attr("width",wid);
    
    const graphMax = d3.max(props.items,(d,i)=>parseFloat(d[1]));
    const graphMin = d3.min(props.items, (d,i)=>parseFloat(d[1]));
    console.log(graphMax,graphMin);
    const yScale = d3.scaleLinear()
                        .domain([graphMax, graphMin])
                        .range([downPadding,hei-upPadding]);

    const numDP = props.items.length;

    const bars = svgCanv.selectAll("rect")
                        .data(props.items)
                        .enter()
                        .append("rect")
                        .attr("x", (d,i)=>{
                            // x space allocated per bar
                            const xSpace = (wid-2*xPadding)/numDP;
                            // if xSpace lower than 30 px, no margin between bars
                            if (xSpace < 30){
                                return xPadding+i*xSpace;
                            }
                            else {
                                // 1:5:1 space allocation
                                const padd = xSpace/7;
                                const barWid = xSpace/7*5;
                                
                                // case of max bar width reached
                                if (barWid > 50){
                                    return xPadding + i*xSpace + (xSpace-50)/2;
                                }
                                else {
                                    return xPadding + i*xSpace + padd;
                                }

                            }
                        })
                        .attr("y", (d,i)=>{
                            return hei-downPadding-yScale(d[1]);
                        })
                        .attr("width", ()=>{
                            // x space allocated per bar
                            const xSpace = (wid-2*xPadding)/numDP;
                            // if xSpace lower than 30 px, no margin between bars
                            if (xSpace < 30){
                                return xSpace;
                            }
                            else {
                                // 1:5:1 space allocation
                                // max bar width of 50 px
                                return Math.min(50, xSpace/7*5);
                            }
                        })
                        .attr("height", (d,i)=>{
                            return yScale(d[1]);
                        })
                        .attr("class","bar")
                        
    
    bars.append("title")
        .text((d,i)=>d[1]);

    return(
        <div ref={graphNode}>
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
