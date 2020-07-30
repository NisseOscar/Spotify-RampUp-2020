import React, { Component } from 'react';
import Typing from 'react-typing-animation';
import Cursor from "./cursor.jsx"

class Form extends Component {
   constructor(props){
     super(props);
     this.onClick = props.onClick;
     this.text = props.text;
   }

   render(){
     return (
       <div>
           <h3>
             What is the occation?
             <br></br>
             <br></br>
           </h3>
             <input id="moodinput" type="text" placeholder="Roadtrip, party, study etc.." maxLength="20">
             </input>

        <button className="navbutton" onClick={this.onClick}>Continue</button>
        </div>
     )
   }
 }


export default Form
