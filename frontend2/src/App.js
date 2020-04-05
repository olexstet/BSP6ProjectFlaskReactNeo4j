import React from "react";
import "./App.css";
import pageMCQ from "./pages/survey";
import pageSearch from "./pages/termSearch";
import pageHome from "./pages/home";
import pageLoad from "./pages/loading";
import NotFoundPage from "./pages/wrongPage";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Link,
  redirect,
  Redirect,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={pageSearch} />
        <Route exact path="/Loading" component={pageLoad} />
        <Route exact path="/Survey" component={pageMCQ} />
        <Route exact path="/404" component={NotFoundPage} />
        <Redirect to="/404" />
      </Switch>
    </Router>
  );
}

export default App;

// <Route exact path="/" component={pageHome} />
