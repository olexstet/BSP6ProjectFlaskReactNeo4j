import React, { Component } from "react";
import CheckBox from "./checkboxQ2";
import axios from "axios";

export class question2 extends Component {
  state = {
    word: "apple",
    randomWords: [],
    correctWords: [],
    numberCorrect: 0,
    arrayWords: [],
    category: ""
  };

  async componentDidMount() {
    await axios.get("http://127.0.0.1:5000/Q2").then(res => {
      const data = res.data;

      console.log(data);
      var correctWords = [];
      var randomWords = [];
      var numberCorrect = 0;
      var category = "";
      var arrayWords = [];

      function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
      }

      Object.entries(data).forEach(([key, value]) => {
        if (key !== "random") {
          for (var i = 0; i < value.length; i++) {
            correctWords.push(value[i]);
            arrayWords.push(value[i]);
          }
          category = key;
        } else {
          for (i = 0; i < value.length; i++) {
            randomWords.push(value[i]);
            arrayWords.push(value[i]);
          }
          numberCorrect = correctWords.length;
        }
        arrayWords = shuffle(arrayWords);
        console.log(arrayWords);
      });
      this.setState({
        word: "apple",
        randomWords: randomWords,
        correctWords: correctWords,
        category: category,
        numberCorrect: numberCorrect,
        arrayWords: arrayWords
      });
    });
  }

  render() {
    const questionStyle = {
      marginLeft: "5%",
      borderStyle: "outset",
      marginRight: "30%",
      paddingLeft: "2%",
      backgroundColor: "white",
      fontFamily: "Georgia",
      fontSize: "14px",
      paddingBottom: "10px"
    };

    var id = 0;

    return (
      <div style={questionStyle}>
        <h3>Question 2</h3>
        <h5>
          Task : What are/is the word(s) which belongs to the category of{" "}
          {this.state.category}
        </h5>
        <div style={{ columns: "3 auto" }}>
          {this.state.arrayWords.map(w => (
            <CheckBox key={(id = id + 1)} w={w}></CheckBox>
          ))}
        </div>
      </div>
    );
  }
}

export default question2;
