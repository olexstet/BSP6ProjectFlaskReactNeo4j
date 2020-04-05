import React, { Component } from "react";
import loadImage from "../loadImage.png";

class loading extends Component {
  render() {
    const style = {
      display: "block",
      marginLeft: "auto",
      marginRight: "auto",
      width: "50%",
      animation: "rotation 2s infinite linear",
    };

    return (
      <div>
        <img id="loading" src={loadImage} style={style}></img>
      </div>
    );
  }
}

export default loading;
