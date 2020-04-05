import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";
import axios from "axios";

export default class componentName extends Component {
  state = {
    currentTerm: "",
  };

  constructor(props) {
    super(props);
    this.onClickSearch = this.onClickSearch.bind(this);
  }

  myChangeHandler = (event) => {
    this.setState({ currentTerm: event.target.value });
  };

  async onClickSearch() {
    console.log(this.state.currentTerm);

    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/",
      data: { d: this.state.currentTerm },
    });
  }

  render() {
    const searchStyle = {
      width: "85%",
      paddingTop: "2%",
      paddingBottom: "2%",
      border: "solid 2px blue",
      borderRadius: "20px 0px 0px 20px",
      textAlign: "center",
      outline: "none",
      fontSize: "20px",
    };

    const divElement = {
      margin: "auto",
      width: "60%",
      marginTop: "47vh",
    };

    const buttonStyle = {
      width: "14%",
      paddingTop: "2%",
      paddingBottom: "2%",
      border: "solid 2px blue",
      backgroundColor: "blue",
      fontSize: "20px",
    };

    return (
      <>
        <div style={divElement}>
          <input
            onChange={this.myChangeHandler}
            type="text"
            placeholder="Search for Term"
            style={searchStyle}
          ></input>
          <Button style={buttonStyle} onClick={this.onClickSearch}>
            <Link to="/Load" style={{ color: "white", textDecoration: "none" }}>
              Search
            </Link>
          </Button>
        </div>
      </>
    );
  }
}
