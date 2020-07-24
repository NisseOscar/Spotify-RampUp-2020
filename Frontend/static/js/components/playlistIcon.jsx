import React, { Component } from 'react';


class Playlistbtn extends Component {
  constructor(props) {
    super(props);
    this.state = {active: false, background:"#797676"};
    this.imageSrc = props.imageSrc;
    this.imageName = props.imageName;
  }

  onClick(){
    let toggle = !this.state.active
    let newbackground = toggle ? "#797676":"#919191";
    this.setState = { active:!toggle, background:newbackground};

    console.log(this.state.active);
    console.log(toggle)
  }

  render(){
    return (
     <button className = "playlistButton" onClick={this.onClick.bind(this)}>
       <img src={this.imageSrc} alt={this.imageName} style={{backgroundColor:this.state.background}}></img>
       <h4>
         <br></br>
         {this.imageName}
       </h4>
     </button>
    )
  }

}

export default Playlistbtn
