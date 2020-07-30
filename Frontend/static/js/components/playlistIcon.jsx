import React, { Component } from 'react';
import Truncate from 'react-truncate';

class Playlistbtn extends Component {
  constructor(props) {
    super(props);
    this.state = {active: false};
    this.imageSrc = props.imageSrc;
    this.imageName = props.imageName;
    this.onClick = this.onClick.bind(this);
    this.toggle = props.toggle;
    this.index = props.index;
  }

  onClick(){
    this.setState({ active: !this.state.active});
    this.toggle(this.index);
  }


  render(){
    let btn_class = this.state.active ? "playlistButton green" : "playlistButton black";

    return (
     <button className = {btn_class} onClick={this.onClick.bind(this)}>
       <div className="imagecont">
        <img src={this.imageSrc} alt={this.imageName}></img>
      </div>
       <h4>
         <br></br>
       <Truncate trimWhitespace={true}>
           {this.imageName}
       </Truncate>
       </h4>
     </button>
    )
  }

}

export default Playlistbtn
