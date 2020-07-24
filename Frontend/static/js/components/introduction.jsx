import React, { Component } from 'react';
import Typing from 'react-typing-animation';
import Cursor from "./cursor.jsx"

const Introduction = () => {
   return (
       <h2>
         <Typing speed={5}  cursor= {<Cursor />} hideCurso>
            Hi!
            <Typing.Delay ms={500}></Typing.Delay>
            <br></br>
            Do you have way to long and way to many unsorted Spotify playlists?
            <br></br>
            <Typing.Delay ms={500}></Typing.Delay>
            Do you find it really annoying sorting through all the playlists trying to find songs that fit the mood?
            <br></br>
            <br></br>
            <Typing.Delay ms={1500}></Typing.Delay>
            Well, let us help. Filterfy filters your playlist/playlists based on a mood, feeling or occation.
            <br></br>
            <br></br>
            <Typing.Delay ms={500}></Typing.Delay>
            All you need to do is specify the mood and choose which playlists you want to pick songs from and then we do the rest.
            <br></br>
            <br></br>
            <Typing.Delay ms={1000}></Typing.Delay>
            Got it?
         </Typing>
       </h2>
   )
 }


export default Introduction
