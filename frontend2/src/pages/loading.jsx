import React, { Component } from "react";
import loadImage from "../loadImage.png";
import "./loadingImage.css";
import axios from "axios";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

class loading extends Component {
  state = {
    username: this.props.location.data.username,
    myComponent: (
      <div>
        <img
          id="loading"
          src={loadImage}
          alt="Loading"
          style={{
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
            marginTop: "20em",
            width: "50%",
            maxWidth: "5%",
            height: "auto",
          }}
        ></img>
        <h4 style={{ textAlign: "center" }}>Waiting for quiz generation :)</h4>
      </div>
    ),
  };

  async componentDidMount() {
    axios
      .post("http://127.0.0.1:5000/", {
        d: this.props.location.data,
        typeRequest: "create_quiz",
      })
      .then((res) => {
        const comp = (
          <div>
            <Button
              style={{
                backgroundColor: "blue",
                fontSize: "20px",
                paddingTop: "1%",
                paddingBottom: "1%",
                border: "solid 2px blue",
                marginLeft: "42.5%",
                width: "15%",
                marginTop: "15em",
                borderRadius: "20px 20px 20px 20px",
              }}
            >
              <Link
                to={{
                  pathname: "/Survey",
                  data: this.state.username,
                }}
                style={{ color: "white", textDecoration: "none" }}
              >
                Ready!
              </Link>
            </Button>
          </div>
        );
        this.setState({ myComponent: comp });
      });
  }

  render() {
    return <div>{this.state.myComponent}</div>;
  }
}

export default loading;
