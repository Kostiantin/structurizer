// Main React app for the demo UI
// Keeping it minimal to reduce S3 storage needs
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
//import DemoForm from './DemoForm';
import DemoForm from './components/DemoForm';

// Simple app with one route for the demo form
function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={DemoForm} />
      </Switch>
    </Router>
  );
}

export default App;