import React, { Component } from 'react';
import Introduction from "./introduction.jsx";
import Form from "./form.jsx"
import Playlists from "./Playlists.jsx"
import Loadingscreen from "./loadingscreen.jsx"
import queryString from 'query-string';
import ErrorScreen from "./ErrorScreen.jsx"
import Result from "./Result.jsx"

export default class Home extends Component {
  constructor(props) {
    super(props);
    this.viewHandler = this.viewHandler.bind(this);
    let id = props.match.params.id;
    let query = queryString.parse(id)
    this.tkn = query.access_token;
    this.state = {view:<Introduction onClick={this.viewHandler} />};
    this.playlists = [];
    this.mood = "";
    this.viewID = 0;
  }

  async componentDidMount() {
      try {
        const response = await fetch('/getPlaylists?tkn='+this.tkn);
        if (!response.ok) {
          throw Error(response.statusText);
        }
        const json = await response.json();
        if(!json.ok){throw Error(json.message);}
        this.playlists = json.playlists;
      }catch(error){
        this.setState({view: <ErrorScreen/>});
      }
  }

  viewHandler() {
      if(this.viewID==0){
        let activeView = <Form onClick={this.viewHandler}/>;
        this.setState({view:activeView})
        this.viewID++;
      }
      else if(this.viewID==1){
        this.setState({view:<Loadingscreen/>});
        let mood= document.getElementById("moodinput").value;
        if(mood.length >0){
          this.setMood(mood)
        }
        else{
          this.setState({view:<Form onClick={this.viewHandler}/>});
        }
      }
      else if(this.viewID==2){
        let selctdPlaylsts = this.playlists.filter(playlist => playlist.isActive);
        // this is total tracks to make sure the user does not make to large of an request, might implement later.
        let totTracks =  selctdPlaylsts.reduce((totTracks, playlist) => totTracks + playlist.tracks, 0);
        if(selctdPlaylsts.length>0){
          this.setState({view:<Loadingscreen/>});
          let selctdPlaylstsIDs = selctdPlaylsts.map(playlist => playlist.id);
          this.createPlaylist(selctdPlaylstsIDs)
        }
      }
      else if(this.viewID==3){
        let activeView = <Form onClick={this.viewHandler}/>;
        this.setState({view:activeView})
        this.viewID=1;
      }
  }

  setMood(mood){
    fetch('/CheckMood?tkn='+this.tkn+'&mood='+mood)
        .then((response)=>{
          if (!response.ok) {throw Error(response.statusText);}
          return response.json();
        })
        .then(res => {
          if(!res.ok){{throw Error("A server Error has occured");}}
          if(res.valid){
            this.mood = mood;
            let activeView = <Playlists onClick={this.viewHandler} playlists={this.playlists}/>;
            this.setState({view:activeView});
            this.viewID++;
          }
          else{
            let activeView = (<div><Form onClick={this.viewHandler}/>
                              <h3>{'Sorry, that mood was not very specific, try an other mood.'}</h3></div>);
            this.setState({view:activeView})
          }
          })
        .catch((error) =>{this.setState({view:<ErrorScreen/>});});
    }

  createPlaylist(playlistIDs){
    let playlistsIDsUrlParse = playlistIDs.join(',')
    let url = '/createPlaylist?tkn='+this.tkn+'&mood='+this.mood+'&playlistIDs='+playlistsIDsUrlParse;
    fetch(url)
      .then((response)=>{
        if (!response.ok) {throw Error(response.statusText);}
        return response.json();
      })
      .then(res => {
        if(!res.ok){{throw Error("A server Error has occured");}}
        this.setState({view:(<Result onClick={this.viewHandler} href={res.newPlaylistID}/>)});
        this.viewID++;
      })
      .catch(error => {this.setState({view:<ErrorScreen/>}); console.log(error);});
  }

  render() {
   let view = this.state.view;
   return view
 }
}
