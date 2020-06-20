import React, { Component } from "react";
import axios from "axios";
import { Redirect } from "react-router-dom";
import { Button } from "semantic-ui-react";

class authentification extends Component {
  /* State which contains all the attributes fo component */
  state = {
    username: "",
    password: "",
    message: "",
    redirect: false,
  };

  myChangeHandlerUsername = async (event) => { /* react to changes in username for handling th last changes */
    await this.setState({ username: event.target.value });
  };

  myChangeHandlerPassword = async (event) => {/* react to changes in password for handling th last changes */
    await this.setState({ password: event.target.value });
  };

  /* Check if username and password are correct*/
  checkLogin = async () => {
    await axios
      .post("http://127.0.0.1:5000/", { /*send request to back-end */
        dataLogin: {   /* data to send with request */
          username: this.state.username,
          password: this.state.password,
        },
        typeRequest: "Login", /* type of request */
      })
      .then(async (res) => {
        if (res.data === "Not Exists") { /* if wrong data, message update */
          await this.setState({ message: "Login failed" });
        }
        if (res.data === "Exists") {
          await this.setState({ message: "", redirect: true }); /*if data is true, set redirect to next page true */
        }
      });
  };

  render() {
    if (this.state.redirect === true) { /* When redirect true pass to Home page */
      return (
        <Redirect
          to={{ /* pass parameters to next page */
            pathname: "/Home",
            data: this.state.username,
          }}
        />
      );
    }

    /*------------------------Style----------------------------- */
    const squareStyle = {
      marginLeft: "35%",
      marginTop: "10em",
      backgroundColor: "white",
      width: "30%",
      height: "25em",
      border: "solid 1px black",
      borderRadius: "0px 0px 0px 0px",
    };

    const labelStyle = {
      display: "inline-block",
      width: "100px",
      marginRight: "20px",
      verticalAlign: "top",
      textAlign: "right",
    };

    /*-----------------Elements------------------------------ */
    return (
      <div>
        <div id="square" style={squareStyle}>
          <h2 style={{ color: "blue", textAlign: "center" }}>
            Sign in to application
          </h2>

          <div
            style={{
              marginLeft: "5%",
              marginTop: "10%",
              fontSize: "18px",
            }}
          >
            <div style={{ marginBottom: "5%" }}>
              <label style={labelStyle}>
                <b>Username: </b>
              </label>
              <input
                type="text"
                placeholder="Enter Username"
                name="uname"
                style={{ fontSize: "18px" }}
                onChange={this.myChangeHandlerUsername}
                required
              />
            </div>

            <div>
              <label style={labelStyle}>
                <b>Password: </b>
              </label>
              <input
                type="text"
                placeholder="Enter Username"
                name="uname"
                style={{ fontSize: "18px" }}
                onChange={this.myChangeHandlerPassword}
                required
              />
            </div>
            <Button
              id="ToHomePageButton"
              style={{
                backgroundColor: "blue",
                color: "white",
                padding: "14px 20px",
                margin: "20px 0",
                border: "none",
                cursor: "pointer",
                width: "95%",
                fontSize: "16px",
              }}
              onClick={this.checkLogin}
            >
              Sign In
            </Button>
          </div>
          <h5 style={{ color: "red", textAlign: "center" }}>
            {this.state.message}
          </h5>
        </div>
      </div>
    );
  }
}

export default authentification;
