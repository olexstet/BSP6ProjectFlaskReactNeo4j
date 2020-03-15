import React from 'react';
import Title from './components/title'; 
import Question1 from './components/question1';
import Question2 from './components/question2';
import ProfileButton from './components/profileButton';
import "./App.css";

function App() {
  const barStyle = {
    backgroundColor: "rgb(30, 144, 255)",
};


  return (
    <div className="App">
      <div style = {barStyle}> 
        <ProfileButton />
      </div>
      <Title/>
      <Question1/>
      <Question2 />
      <div ></div>
    </div>
  );
}

export default App;
