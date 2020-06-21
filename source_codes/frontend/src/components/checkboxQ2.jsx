import React, { Component } from 'react';
import { Checkbox } from 'semantic-ui-react';

export class checkboxQ2 extends Component { /* Checkbox for word of question 2*/
    render() {
        return (
            <div>
                <Checkbox style = {{fontSize: "14px"}} label={this.props.w} />
            </div>
        );
    }
}

export default checkboxQ2;
