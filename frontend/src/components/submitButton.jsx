import React, { Component } from "react";

class submitButton extends Component {
  render() {
    const buttonStyle = {
      display: "inline-block",
      padding: "0.35em 1.2em",
      border: "0.1em solid #FFFFFF",
      margin: "0 0.3em 0.3em 0",
      borderRadius: "0.12em",
      boxSizing: "border-box",
      textDecoration: "none",
      fontFamily: "'Roboto',sans-serif",
      fontWeight: "300",
      color: "white",
      textAlign: "center",
      transition: " all 0.2s",
      backgroundColor: "blue",
      marginLeft: "5%",
      marginTop: "10px"
    };

    return (
      <div>
        <button style={buttonStyle}>Submit</button>
      </div>
    );
  }
}

export default submitButton;
