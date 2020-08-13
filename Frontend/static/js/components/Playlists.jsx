import React, { Component } from 'react';
import Playlistbtn from "./playlistIcon.jsx"


class Playlists extends Component {
  constructor(props) {
    super(props);
    this.playlists = props.playlists;
    this.viewChange = props.onClick;
    this.togglePlaylist = this.togglePlaylist.bind(this);
    this.playlistsBtns = this.playlists.map((playlist,index) => (
      <Playlistbtn key={playlist.id} index={index} toggle={this.togglePlaylist} imageSrc={playlist.image_url} imageName={playlist.name}/>
    ));
  }

  togglePlaylist(index){
    this.playlists[index].isActive = !this.playlists[index].isActive;
  }

  render(){
    return (
      <div>
        <h3>
          Which playlists would you like to select songs from?
        </h3>
      <button className="navbutton" onClick={this.viewChange}>I'm done!</button>
      <div>
        {this.playlistsBtns}
      </div>
      </div>

    )
  }

}

export default Playlists
