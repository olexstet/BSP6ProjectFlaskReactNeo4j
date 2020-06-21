import React from "react";
import "./App.css";
import AuthentificationPage from "./pages/authentification";
import pageMCQ from "./pages/survey";
import pageSearch from "./pages/termSearch";
import pageLoad from "./pages/loading";
import NotFoundPage from "./pages/wrongPage";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={AuthentificationPage} />
        <Route exact path="/Home" component={pageSearch} />
        <Route exact path="/Loading" component={pageLoad} />
        <Route exact path="/Survey" component={pageMCQ} />
        <Route exact path="/404" component={NotFoundPage} />
        <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;

