import React, { useState } from "react";
import "./table-select.css";







const DynamicTable = (state) => {


  var [message, setMessage] = useState(""),
    [message2, setMessage2] = useState(""),
    [propkeys, setPropKeys] = useState(current_keys),
    [propvalues, setPropValues] = useState(current_values);
  for (var property in current_propobject) {
      current_keys.push(property);
      current_values.push(current_propobject[property]);
    }

  updateMessageKey( (key) => {
      setMessage(key)
    });

  handleKeyChanged(i, event) {
    var propkeys = this.state.propkeys;
  
    if (value != "") {
      propkeys[i] = value;
    }
    console.log(value);
  
    if (event.target.value == "") {
      this.handleItemDeleted(i);
    }
    this.handleRefresh(i);
    this.setPropKeys(propkeys);
    this.setState({
      propkeys: propkeys,
    });
  }

  setPropKeys(value)
  renderKeyRows(() => {
      var context = this;
      return propkeys.map(function (o, i) {
        return (
          <tr key={"item-" + i}>
            <td>
              <input
                className="form-control"
                type="text"
                value={o}
                id={o + i}
                onChange={setPropKeys.bind(context, i)}
              />
            </td>
          </tr>
        );
      });
  });
  renderValueRows(() => {
    var context = this;
  
    return propvalues.map(function (o, i) {
      return (
        <tr key={"item-" + i}>
          <td>
            <input
              className="form-control"
              type="text"
              value={o}
              onChange={context.handleValueChanged.bind(context, i)}
            />
          </td>
        </tr>
      );
    });
  });

  renderDelete(() => {
    var context = this;
  
    return propvalues.map(function (o, i) {
      return (
        <tr key={"item-" + i}>
          <td>
            <button
              className="btn btn-default"
              onClick={context.handleItemDeleted.bind(context, i)}
            >
              Delete
            </button>
          </td>
        </tr>
      );
    });
  });
  return (
    <div>
      <table className="">
        <thead>
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{renderKeyRows()}</td>
            <td>{renderValueRows()}</td>
            <td>{renderDelete()}</td>
          </tr>
        </tbody>
      </table>
      <form>
        <tr>
          <td>
            <input
              className="form-control"
              type="text"
              value={message}
              onChange={updateMessageKey.bind(this)}
            />
          </td>
          <td>
            <input
              className="form-control"
              type="text"
              value={message2}
              onChange={updateMessageValue.bind(this)}
            />
          </td>
          <td>
            <button
              id="add-item"
              data-testid="add-item"
              className="btn btn-default"
              type="button"
              onClick={handleClick.bind(this)}
            >
              Add Item
            </button>
          </td>
        </tr>
      </form>
      <hr />
    </div>
  );

}

    

    
updateMessageValue(event) {
  this.setState({
    message2: event.target.value,
  });
}
handleRefresh(i) {
  var propkeys = this.state.propkeys;
  var propvalues = this.state.propvalues;
  var propobject = {};
  propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));

  console.log(propobject);
  this.setProp(propobject);
  this.setPropKeys(propkeys);
  this.setPropValues(propvalues);


  this.setState({
    propkeys: propkeys,
    propvalues: propvalues,
    message: "",
    message2: "",
    propobject: propobject,
  });
}
handleClick() {
  var propkeys = this.state.propkeys;
  var propvalues = this.state.propvalues;
  if (this.state.message != "") {
    if (this.state.message2 != "") {
      propkeys.push(this.state.message);
      propvalues.push(this.state.message2);
    } else {
      console.log("Value not valid");
    }
  } else {
    console.log("Value not valid");
  }

  var propobject = {};
  propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
  console.log(propobject);
  this.setProp(propobject);
  this.setPropKeys(propkeys);
  this.setPropValues(propvalues);
  this.setState({
    propkeys: propkeys,
    propvalues: propvalues,
    message: "",
    message2: "",
    propobject: propobject,
  });
}

handleValueChanged(i, event) {
  var propvalues = this.state.propvalues;
  var propkeys = this.state.propkeys;
  propvalues[i] = event.target.value;

  this.handleRefresh();
  this.setPropKeys(propkeys);
  this.setPropValues(propvalues);
  this.setState({
    propvalues: propvalues,
  });
}


handleItemDeleted(i) {
  var propvalues = this.state.propvalues;
  var propkeys = this.state.propkeys;

  propvalues.splice(i, 1);
  propkeys.splice(i, 1);
  this.setPropKeys(propkeys);
  this.setPropValues(propvalues);
  this.handleRefresh(i);
  this.setState({
    propvalues: propvalues,
    propkeys: propkeys,
  });
}


renderValueRows() {
  var context = this;

  return this.state.propvalues.map(function (o, i) {
    return (
      <tr key={"item-" + i}>
        <td>
          <input
            className="form-control"
            type="text"
            value={o}
            onChange={context.handleValueChanged.bind(context, i)}
          />
        </td>
      </tr>
    );
  });
}
renderDelete() {
  var context = this;

  return this.state.propvalues.map(function (o, i) {
    return (
      <tr key={"item-" + i}>
        <td>
          <button
            className="btn btn-default"
            onClick={context.handleItemDeleted.bind(context, i)}
          >
            Delete
          </button>
        </td>
      </tr>
    );
  });
}
    

  


