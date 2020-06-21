import React, { Component } from "react";
import CheckBox from "./checkboxQ1";
import axios from "axios";

export class question1 extends Component {
  state = {
    word: this.props.term,
    definitions: [],
  };

  async componentDidMount() {
    await axios
      .post("http://127.0.0.1:5000/", { /* Send request for fetching the data for question 1 */
        typeRequest: "Q1",
        username: this.props.username,
      })
      .then((res) => {
        const data = res.data;

        var definitions = [];
        Object.entries(data).forEach(([key,value]) => { /* fetch result*/
          definitions.push(value); /* add definitions to an array*/ 
        });
        this.setState({ word: this.props.term, definitions });
      });
  }

  render() {

    /*-------------------Styles-------------------------*/
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

    /*-----------------------Components------------------------*/
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
