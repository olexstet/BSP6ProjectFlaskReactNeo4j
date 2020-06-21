import React, { Component } from "react";
/*import { Link } from "react-router-dom";*/
import { Button } from "semantic-ui-react";
import axios from "axios";
import { Redirect } from "react-router-dom";

export default class termSearch extends Component {
  state = {
    currentTerm: "",
    username: "",
    redirect: false, 
    message: ""
  };

  myChangeHandler = (event) => { /* Handle changes when a user write a term */
    this.setState({ currentTerm: event.target.value });
  };

  checkTerm = async () => { /* Check if term exists in WordNet at back-end */
    await axios
      .post("http://127.0.0.1:5000/", {
        dataCheck: {
          term: this.state.currentTerm
        },
        typeRequest: "Check_Term",
      })
      .then(async (res) => {
        if (res.data === "Not Exists") {
          await this.setState({ message: "Sorry, it is an incorrect word" }); /* update message */
        }
        if (res.data === "Exists") {
          await this.setState({ message: "", redirect: true });
        }
      });
  };


  render() {
    if (this.state.username === "") {
      if (sessionStorage.getItem("usernameState") === null) { /* if the username is not yet declared in storage */
        const data = this.props.location.data;
        sessionStorage.setItem("usernameState", data); /* store username in storage */
        this.setState({ username: sessionStorage.getItem("usernameState") });
      } else {
        this.setState({ username: sessionStorage.getItem("usernameState") }); /* if exists already, get username*/
      }
    }

    if (this.state.redirect === true) {
      sessionStorage.setItem("term", this.state.currentTerm); /* Load the term in session storage */
      return (
        <Redirect
          to={{
            pathname: "/Loading",
            data: this.state,
          }}
        />
      );
    } 
    
    /*-------------------------Styles----------------------- */
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

    
    /* ---------------- Components-----------------*/
    return (
      <>
        <div style={divElement}>
          <input
            onChange={this.myChangeHandler}
            type="text"
            placeholder="Search for Term"
            style={searchStyle}
          ></input>
          <Button style={buttonStyle}  onClick={this.checkTerm}>
            <text style={{ color: "white", textDecoration: "none" }}>
              Do Quiz
            </text>
          </Button>
          <h5 style={{ color: "red", textAlign: "center" }}>
            {this.state.message}
          </h5>
        </div>
      </>
    );
  }
}

