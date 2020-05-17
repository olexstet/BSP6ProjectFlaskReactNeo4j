import React, { Component } from 'react';

export class profileButton extends Component {
    render() {

        const stylePB = {
            height: "35px",
        }

        return (
            <div style = {stylePB}>
                <button> Button</button>
            </div>
        );
    }
}

export default profileButton;
