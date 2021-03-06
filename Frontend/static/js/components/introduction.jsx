import React, { Component } from 'react';
import Typing from 'react-typing-animation';
import Cursor from "./cursor.jsx"

class Introduction extends Component {
  constructor(props) {
    super(props);
    this.viewChange = props.onClick;
    this.onClick = this.onClick.bind(this);
    this.state = {
      view:(<h2>
        <Typing speed={5}  cursor= {<Cursor />} hideCurso>
           Hi!
           <Typing.Delay ms={500}></Typing.Delay>
           <br></br>
           Do you have way too long and way too many unsorted Spotify playlists?
           <br></br>
           <Typing.Delay ms={500}></Typing.Delay>
           Do you find it really annoying sorting through all the playlists trying to find songs that fit the mood?
           <br></br>
           <br></br>
           <Typing.Delay ms={1500}></Typing.Delay>
           Well, let us help. Filterfy filters your playlist/playlists based on a mood, feeling or occasion.
           <br></br>
           <br></br>
           <Typing.Delay ms={500}/>
           All you need to do is specify the mood and choose which playlists you want to pick songs from and then we do the rest.
           <br></br>
           <br></br>
           <Typing.Delay ms={1000}></Typing.Delay>
           Got it?
           <Typing.Speed ms={0} />
           <br></br>
           <br></br>
            <button className="navbutton" onClick={this.viewChange}>{"Got it!"}</button>
        </Typing>
      </h2>)};
  }

  onClick(){
    this.setState({
      view:(<h2>
           Hi!
           <br></br>
           Do you have way too long and way too many unsorted Spotify playlists?
           <br></br>
           Do you find it really annoying sorting through all the playlists trying to find songs that fit the mood?
           <br></br>
           <br></br>
           Well, let us help. Filterfy filters your playlist/playlists based on a mood, feeling or occasion.
           <br></br>
           <br></br>
           All you need to do is specify the mood and choose which playlists you want to pick songs from and then we do the rest.
           <br></br>
           <br></br>
           Got it?
           <br></br>
           <br></br>
           <button className="navbutton" onClick={this.viewChange}>Got it!</button>
          </h2>
    )});
  }
  render(){
   return (
     <div onClick={this.onClick} style={{height: "70%"}}>
       {this.state.view}
    </div>
    )
  }
 }


export default Introduction
