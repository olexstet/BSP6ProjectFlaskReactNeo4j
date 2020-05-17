import React, { Component } from "react";
import CheckBox from "./checkboxQ1";
import axios from "axios";

export class question1 extends Component {
  state = {
    word: "apple",
    definitions: [],
  };

  async componentDidMount() {
    await axios
      .post("http://127.0.0.1:5000/", {
        typeRequest: "Q1",
        username: this.props.username,
      })
      .then((res) => {
        const data = res.data;

        console.log(data);

        /* NOT NEEDED, TO BE ERAISE
        function shuffle(array) {
          for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
          }
          return array;
        }*/

        var definitions = [];
        Object.entries(data).forEach(([key,value]) => {
          definitions.push(value);
        });
        this.setState({ word: "apple", definitions });
      });
  }

  render() {
    const questionStyle = {
      marginLeft: "5%",
      borderStyle: "outset",
      marginRight: "30%",
      paddingLeft: "2%",
      backgroundColor: "white",
      fontFamily: "Georgia",
      fontSize: "14px",
      paddingBottom: "10px",
      marginBottom: "5px",
    };

    var id = 0;

    return (
      <div style={questionStyle}>
        <h3>Question 1</h3>
        <h5>
          Task : Select the right definition of word{" "}
          <span style={{ color: "red" }}>{this.state.word}</span>
        </h5>
        <div>
          {this.state.definitions.map((wDef) => (
            <CheckBox key={(id = id + 1)} WDefintion={wDef}></CheckBox>
          ))}
        </div>
      </div>
    );
  }
}

export default question1;
