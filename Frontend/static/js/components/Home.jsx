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
        this.playlists = json.playlists;
      }catch(error){
        this.state.view = <ErrorScreen/>
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
          this.moodValid(mood)
        }
      }
      else if(this.viewID==2){
        let listActive = this.playlists.map(playlist => playlist.isActive);
        if(listActive.some(item => item)){
          let activeView =<Loadingscreen/>;
          this.setState({view:(<Result onClick={this.viewHandler} href="https://open.spotify.com/playlist/27xKF3ZFpnIP49wjIOAk4p?si=UD-dlAb8RVOCO8CetEOE8A"/>)});
          this.viewID++;

        }
      }
  }
  moodValid(mood){
    fetch('/CheckMood?tkn='+this.tkn+'&mood='+mood)
        .then((response)=>{
          if (!response.ok) {throw Error(response.statusText);}
          return response.json();
        }).then(res => {
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


  render() {
   return (
     <div>
       {this.state.view}
    </div>
   )
 }
}
