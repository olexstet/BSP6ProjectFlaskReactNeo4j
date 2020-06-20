import React, { Component } from "react";
import Title from "../components/title";
import Question1 from "../components/question1";
import Question2 from "../components/question2";
import Question3 from "../components/question3";
import SubmitButton from "../components/submitButton";
import { Redirect } from "react-router-dom";

export default class componentName extends Component {
  componentDidMount() { /* when click on button come back go to Home in order to avoid loading page */
    window.addEventListener("popstate", (event) => {
      return <Redirect to="/Home" />;
    });
  }

  render() {
    const barStyle = {
      backgroundColor: "rgb(30, 144, 255)",
    };

    /* Questions components*/ 
    return (
      <div className="App">
        <div style={barStyle}></div>
        <Title />
         
        <Question1 username={sessionStorage.getItem("usernameState")} term = {sessionStorage.getItem("term")} /> 
        <Question2 username={sessionStorage.getItem("usernameState")} term = {sessionStorage.getItem("term")} />
        <Question3 username={sessionStorage.getItem("usernameState")} term = {sessionStorage.getItem("term")} />
        <SubmitButton />
        <div></div>
      </div>
    );
  }
}
