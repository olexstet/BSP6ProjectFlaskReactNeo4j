import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export default class termSearch extends Component {
  state = {
    currentTerm: "",
    username: "",
  };

  myChangeHandler = (event) => {
    this.setState({ currentTerm: event.target.value });
  };

  render() {
    if (this.state.username === "") {
      if (sessionStorage.getItem("usernameState") === null) {
        const data = this.props.location.data;
        sessionStorage.setItem("usernameState", data);
        this.setState({ username: sessionStorage.getItem("usernameState") });
      } else {
        this.setState({ username: sessionStorage.getItem("usernameState") });
      }
    }

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
          <Button style={buttonStyle}>
            <Link
              to={{
                pathname: "/Loading",
                data: this.state,
              }}
              style={{ color: "white", textDecoration: "none" }}
            >
              Do Quiz
            </Link>
          </Button>
        </div>
      </>
    );
  }
}
