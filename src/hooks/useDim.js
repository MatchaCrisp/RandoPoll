import {useState, useEffect} from 'react';

//hook for tracking viewport size & calculate bar width and separation width

//props: len: length of dataset
//       max: max of dataset
//       xRatio: percentage of viewport width taken up by graph
//       yRatio: percentage of viewport height taken up by graph

//returns object
//return order: gWidth:graphWidth, gHeight:graphHeight, barW:barWidth, barSep:barSeparator, barH:barHeightMult
const useDim=({xRatio,yRatio})=>{
    //grab dimensions of viewport
    const getDim=(xRat,yRat)=>{
      const {innerWidth:windW,innerHeight:windH}=window;
      const gW=Math.round(windW*xRat);
      const gH=Math.round(windH*yRat);

      return {gWidth:gW<600?600:gW,gHeight:gH<400?400:gH};
    }


    const handleResize=()=>{
      setDim(getDim(xRatio,yRatio));
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