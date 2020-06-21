import React, { Component } from "react";
import CheckBox from "./checkboxQ2";
import axios from "axios";

export class question2 extends Component {
  state = {
    word: this.props.term,
    randomWords: [], /* wrong words*/
    correctWords: [],
    numberCorrect: 0,
    arrayWords: [],
    category: "",
  };

  async componentDidMount() {
    await axios
      .post("http://127.0.0.1:5000/", { /* fetch words for question 2 at back-end*/ 
        typeRequest: "Q2",
        username: this.props.username,
      })
      .then((res) => {
        const data = res.data;
        
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
              correctWords.push(value[i]); /* correct words*/ 
              arrayWords.push(value[i]); 
            }
            category = key; /* fetch category*/
          } else {
            for (i = 0; i < value.length; i++) {
              randomWords.push(value[i]); /* push random words*/
              arrayWords.push(value[i]); /* add random words to correct words*/ 
            }
            numberCorrect = correctWords.length;
          }
          arrayWords = shuffle(arrayWords); /* shuffle array with all words*/ 
          
        });
        this.setState({ /* update state*/ 
          word: this.props.term,
          randomWords: randomWords,
          correctWords: correctWords,
          category: category,
          numberCorrect: numberCorrect,
          arrayWords: arrayWords,
        });
      });
  }

  render() {

    /* ----------------------------Styles------------------------*/ 
    const questionStyle = {
      marginLeft: "5%",
      borderStyle: "outset",
      marginRight: "30%",
      paddingLeft: "2%",
      backgroundColor: "white",
      fontFamily: "Georgia",
      fontSize: "14px",
      paddingBottom: "10px",
    };

    var id = 0;

    /*----------------------------Components------------------------*/ 
    return (
      <div style={questionStyle}>
        <h3>Question 2</h3>
        <h5>
          Task : Select the word(s) which belongs to the category of{" "}
          <span style={{ color: "green" }}>{this.state.category}</span>
        </h5>
        <div style={{ columns: "3 auto" }}>
          {this.state.arrayWords.map((w) => (
            <CheckBox key={(id = id + 1)} w={w}></CheckBox>
          ))}
        </div>
      </div>
    );
  }
}

export default question2;

