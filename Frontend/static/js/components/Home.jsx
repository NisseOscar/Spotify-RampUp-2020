import React, { Component } from 'react';
import Introduction from "./introduction.jsx";
import Form from "./form.jsx"
import Playlists from "./Playlists.jsx"
import Loadingscreen from "./loadingscreen.jsx"
import queryString from 'query-string';
import ErrorScreen from "./ErrorScreen.jsx"

export default class Home extends Component {
  constructor(props) {
    super(props);
    this.viewHandler = this.viewHandler.bind(this);
    let id = props.match.params.id;
    let query = queryString.parse(id)
    this.tkn = query.access_token;
    this.state = {view: (<Introduction onClick={this.viewHandler} />), playlists:[]}
    this.viewID = 0;
  }

  async componentDidMount() {
      try {
        const response = await fetch('/getPlaylists?tkn='+this.tkn);
        if (!response.ok) {
          throw Error(response.statusText);
        }
        const json = await response.json();
        this.setState({playlists: json.playlists})
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
        let value= document.getElementById("moodinput").value;
        if(value.length >0){
          let activeView = <Playlists onClick={this.viewHandler} playlists={this.state.playlists}/>;
          this.setState({view:activeView})
          this.viewID++;
        }
      }
      else if(this.viewID==2){
        let listActive = this.state.playlists.map(playlist => playlist.isActive);
        console.log(listActive);
        if(false){
          let activeView =<Loadingscreen/>;
          this.setState({view:activeView})
          this.viewID++;
        }
      }
  }
  render() {
   return (
     <div>
       {this.state.view}
    </div>
   )
 }
}
