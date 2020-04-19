import React, { Component } from "react";
import Title from "../components/title";
import Question1 from "../components/question1";
import Question2 from "../components/question2";
import Question3 from "../components/question3";
import SubmitButton from "../components/submitButton";
import { Redirect } from "react-router-dom";

export default class componentName extends Component {
  componentDidMount() {
    window.addEventListener("popstate", (event) => {
      return <Redirect to="/Home" />;
    });
  }

  render() {
    const barStyle = {
      backgroundColor: "rgb(30, 144, 255)",
    };

    return (
      <div className="App">
        <div style={barStyle}></div>
        <Title />
        <Question1 username={sessionStorage.getItem("usernameState")} />
        <Question2 username={sessionStorage.getItem("usernameState")} />
        <Question3 username={sessionStorage.getItem("usernameState")} />
        <SubmitButton />
        <div></div>
      </div>
    );
  }
}
