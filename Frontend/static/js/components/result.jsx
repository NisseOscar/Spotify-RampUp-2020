import React, { Component } from 'react';

const Result =(props) =>{
  let style = {
    position: "relative",
    marginTop: "3%",
    marginBot: "10%",
    left: "10%"};
 return (
   <div>
       <h3>
         {'Aaaaaand Done!'}
       </h3>
       <h3>
         {'Here is your resulting Playlist. It has been added to your library but you can feel free to skim through it here.'}
       </h3>
       <iframe src={'https://open.spotify.com/embed/playlist/'+props.href} style={style} width="80%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>

    <button className="navbutton" onClick={props.onClick}>Try Again</button>
    </div>
 )
}
// <iframe className="playlistPreview"  src={props.href}
// frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
export default Result
