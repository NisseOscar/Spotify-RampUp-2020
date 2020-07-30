import React, { Component } from 'react';
import Playlistbtn from "./playlistIcon.jsx"


class Playlists extends Component {
  constructor(props) {
    super(props);
    this.state = {playlists:props.playlists};
    this.viewChange = props.onClick;
    this.togglePlaylist = this.togglePlaylist.bind(this);
    this.playlistsBtns = this.state.playlists.map((playlist,index) => (
      <Playlistbtn key={playlist.id} index={index} toggle={this.togglePlaylist} imageSrc={playlist.image_ref} imageName={playlist.name}/>
    ));
  }

  togglePlaylist(index){
    console.log(index)
    this.playlists[id].isActive = !this.playlists[id].isActive
    console.log(this.playlists[id])
  }

  render(){
    return (
      <div>
      <div>
        <h3>
          Which playlists would you like to select songs from?
        </h3>
      <button className="navbutton" onClick={this.viewChange}>I'm done!</button>
      </div>
      <div>
        {this.playlistsBtns}
      </div>
      </div>

    )
  }

}

export default Playlists
