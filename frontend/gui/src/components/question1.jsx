import React, { Component } from "react";
import CheckBox from "./checkboxQ1";
import axios from "axios";

export class question1 extends Component {
  state = {
    word: "apple",
    definitions: []
  };

  componentDidMount() {
    axios.get("http://127.0.0.1:5000/api/").then(res => {
      const data = res.data;
      console.log(data);
      const definitions = [
        data[0]
        //data[0].definitionOther1,
        //data[0].definitionOther2,
        //data[0].definitionOther3,
        //data[0].definitionOther4
      ];
      console.log(definitions);
      //this.setState({ word: data[0].word, definitions });
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
      marginBottom: "5px"
    };

    var id = 0;

    return (
      <div style={questionStyle}>
        <h3>Question 1</h3>
        <h5>Task : Find the right definition of word {this.state.word}</h5>
        <div>
          {this.state.definitions.map(wDef => (
            <CheckBox key={(id = id + 1)} WDefintion={wDef}></CheckBox>
          ))}
        </div>
      </div>
    );
  }
}

export default question1;
