import React, { Component } from 'react';

const Result =(props) =>{
 return (
   <div>
       <h3>
         {'Aaaaaand Done!'}
       </h3>
       <h3>
         {'Here is your resulting Playlist. It has been added to your library but you can scim through it here also.'}
       </h3>
       <iframe className="playlistPreview" src="https://open.spotify.com/playlist/7xB5RIoWhp2RHVCT43GwWg" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>

    <button className="navbutton" onClick={props.onClick}>Try Again</button>
    </div>
 )
}
//        <iframe className='playlistPreview' src={props.newPlaylistID} frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
export default Result