import React, { Component } from "react";
import CheckBox from "./checkboxQ2";

export class question2 extends Component {
  state = {
    word: "apple",
    randomWords: [
      "time period",
      "fruit",
      "science",
      "happening",
      "command",
      "concept",
      "cryptography",
      "speech act",
      "spin",
      "infectious agent",
      "dishonesty",
      "edible fruit"
    ],
    correctWords: ["fruit", "edible fruit"],
    numberCorrect: 2
  };

  render() {
    const questionStyle = {
      marginLeft: "5%",
      borderStyle: "outset",
      marginRight: "30%",
      paddingLeft: "2%",
      backgroundColor: "white",
      fontFamily: "Georgia",
      fontSize: "14px",
      paddingBottom: "10px"
    };

    var id = 0;

    return (
      <div style={questionStyle}>
        <h3>Question 2</h3>
        <h5>
          Task : Find {this.state.numberCorrect} related word(s) to word{" "}
          {this.state.word}
        </h5>
        <div style={{ columns: "3 auto" }}>
          {this.state.randomWords.map(w => (
            <CheckBox key={(id = id + 1)} w={w}></CheckBox>
          ))}
        </div>
      </div>
    );
  }
}

export default question2;
