import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';
import Home from './components/Home';
// import more components
export default (
    <HashRouter history={hashHistory}>
      <Route path='/:id' component={Home} />
    </HashRouter>
);
