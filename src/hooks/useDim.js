import {useState, useEffect} from 'react';

//hook for tracking viewport size & calculate bar width and separation width

//props: len: length of dataset
//       max: max of dataset
//       xRatio: percentage of viewport width taken up by graph
//       yRatio: percentage of viewport height taken up by graph

//returns object
//return order: gWidth:graphWidth, gHeight:graphHeight, barW:barWidth, barSep:barSeparator, barH:barHeightMult
const useDim=({xRatio,yRatio,xMax,yMax,xMin,yMin})=>{
    //grab dimensions of viewport
    const getDim=(xRat,yRat,xMax=-1,yMax=-1,xMin=-1,yMin=-1)=>{
      console.log(xRat,yRat,xMax)
      const {innerWidth:windW,innerHeight:windH}=window;
      let gW=Math.round(windW*xRat);
      let gH=Math.round(windH*yRat);
      if (xMax !== -1 && xMax < gW){
        gW=xMax;
      }
      if (xMin !== -1 && xMin > gW){
        gW=xMin;
      }
      if (yMax !== -1 && yMax < gH){
        gH=yMax;
      }
      if (yMin !== -1 && yMin > gH){
        gH=yMin;
      }
      console.log(gW,gH);
      return {gWidth:gW,gHeight:gH};
    }


    const handleResize=()=>{
      setDim(getDim(xRatio,yRatio,xMax,yMax,xMin,yMin));
    }


    //initialize to viewport size on open
    const [dim,setDim]=useState(getDim(xRatio,yRatio));
    //add listener for resize on mount/remove on unmount
    useEffect(()=>{
      window.addEventListener('resize',handleResize);
      return ()=>window.removeEventListener('resize',handleResize);
    });
  
    //return order: graphWidth, graphHeight, barWidth, barSeparator, barHeightMult
    return dim;
  }
  
  export default useDim;