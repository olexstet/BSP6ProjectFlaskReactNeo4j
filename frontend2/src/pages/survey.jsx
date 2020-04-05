import React, { Component } from "react";
import Title from "../components/title";
import Question1 from "../components/question1";
import Question2 from "../components/question2";
import Question3 from "../components/question3";
import SubmitButton from "../components/submitButton";
import ProfileButton from "../components/profileButton";

export default class componentName extends Component {
  render() {
    const barStyle = {
      backgroundColor: "rgb(30, 144, 255)"
    };

    return (
      <div className="App">
        <div style={barStyle}>
          <ProfileButton />
        </div>
        <Title />
        <Question1 />
        <Question2 />
        <Question3 />
        <SubmitButton />
        <div></div>
      </div>
    );
  }
}
