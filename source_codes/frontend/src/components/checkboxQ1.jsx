import React, { Component } from "react";
import { Checkbox } from "semantic-ui-react";

export class checkboxQ1 extends Component { /* One checkbox for question one with a definition */
  render() {
    return (
      <div style={{ marginBottom: "5px" }}>
        <Checkbox
          color="green"
          style={{ fontSize: "14px" }}
          label={this.props.WDefintion}
        />
      </div>
    );
  }
}

export default checkboxQ1;

