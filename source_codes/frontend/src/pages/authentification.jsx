import React, { Component } from "react";
import axios from "axios";
import { Redirect } from "react-router-dom";
import { Button } from "semantic-ui-react";

class authentification extends Component {
  state = {
    username: "",
    password: "",
    message: "",
    redirect: false,
  };

  myChangeHandlerUsername = async (event) => {
    await this.setState({ username: event.target.value });
  };

  myChangeHandlerPassword = async (event) => {
    await this.setState({ password: event.target.value });
  };

  checkLogin = async () => {
    await axios
      .post("http://127.0.0.1:5000/", {
        dataLogin: {
          username: this.state.username,
          password: this.state.password,
        },
        typeRequest: "Login",
      })
      .then(async (res) => {
        console.log(res);
        if (res.data === "Not Exists") {
          await this.setState({ message: "Login failed" });
        }
        if (res.data === "Exists") {
          await this.setState({ message: "", redirect: true });
        }
        console.log(this.state.message);
      });
  };

  render() {
    if (this.state.redirect === true) {
      return (
        <Redirect
          to={{
            pathname: "/Home",
            data: this.state.username,
          }}
        />
      );
    }

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
