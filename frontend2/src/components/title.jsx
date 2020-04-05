import React, { Component } from 'react'

export default class title extends Component {
  state = {
    word: "apple"
  }

  render() {
    const titleStyle = {
        color: "black",
        marginLeft: "5%",
        marginTop: "20px",
        fontFamily:  "Georgia, serif",
        fontWeight: "bold",
        fontSize: "20px",
        //textDecoration: "underline"
    };

    return (
        <div style = {titleStyle}>
            <h3>Quiz on word: {this.state.word}</h3>
        </div> // replace after the text 
    )
  }
}
