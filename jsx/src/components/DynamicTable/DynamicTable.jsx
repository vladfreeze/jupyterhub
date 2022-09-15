import React, { useState } from "react";
import "./table-select.css";
import PropTypes from "prop-types";
import { useSelector, useDispatch } from "react-redux";


const DynamicTable = (props) => {
  
  var [message, setMessage] = useState(""),
    [message2, setMessage2] = useState("");
  var {current_propobject} = props;
  
  var propobject = current_propobject;

  var [propkeys, setOwnKeys] = useState(Object.keys(current_propobject));
  var [propvalues, setOwnValues] = useState(Object.values(current_propobject));
  var updateMessageKey = (event) => {
    setMessage(event.target.value);
  }
  var updateMessageValue = (event) => {
    setMessage2(event.target.value);
  }
  const handleRefresh = () => {
    //var propobject = {};
    //propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
    //console.log(propobject);
    //console.log("HandleRefresh"+propkeys);
    //props.setPropKeys(propkeys);
    //props.setPropValues(propvalues);
    //props.setProp(propobject);

    var propobject = {};
    propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
    props.setProp(propobject);

    setMessage("");
    setMessage2("");

  }
  
  const handleClick = () => {
    if (message != "") {
      if (message2 != "") {
        propkeys.push(message);
        propvalues.push(message2);
      } else {
        console.log("Value not valid");
      }
    } else {
      console.log("Value not valid");
    }
    var propobject = {};
    propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
    props.setProp(propobject);
    props.setPropKeys(propkeys);
    setOwnKeys(propkeys);
    props.setPropValues(propvalues);
    setOwnValues(propvalues);
    setMessage("");
    setMessage2("");
    console.log(propkeys);
    console.log(propvalues);
    console.log(propobject);
  }
  
  const handleItemDeleted = (i) => {
    propvalues.splice(i, 1);
    propkeys.splice(i, 1);
    props.setPropKeys(propkeys);
    props.setPropValues(propvalues);
    handleRefresh();
  }
  const handleKeyChanged = (i, event) => {
    console.log(i);
    console.log(event);
    console.log(event.target);
    console.log("value "+ event.target.value);
    if (event.target.value != "") {
      propkeys[i] = event.target.value ;
    }
    console.log("i "+ i)
    console.log("RENDER "+propkeys[i]);

    console.log("RENDER "+propkeys);
    //handleRefresh();
    setOwnKeys(propkeys);
    props.setPropKeys(propkeys);

  }
  const renderKeyRows = () => {
    var context = this
    return propkeys.map(function (o, i) {
      return (
        <tr key={"item-" + i}>
          <td>
            <input
              className="form-control"
              type="text"
              value={propkeys[i]}
              id={o}
              onChange= {handleKeyChanged.bind(context,i)}
            />
          </td>
        </tr>
      );
    });
  }
  const renderValueRows = () => {

    return propvalues.map(function (o, i) {
      //console.log("ValRows" +i)
      //console.log("ValRows" +o)
      return (
        <tr key={"item-" + i}>
          <td>
            <input
              className="form-control"
              type="text"
              value={o}
              onChange={(i,o) => {
                propvalues[i] = o;
                props.setPropValues(propvalues);
                setOwnValues(propvalues);
    
                
              }}
            />
          </td>
        </tr>
      );
    });
  }
  const renderDelete = () => {

    return propvalues.map(function (o, i) {
      return (
        <tr key={"item-" + i}>
          <td>
            <button
              className="btn btn-default"
              onClick={(i) => {
                console.log("delete");
                console.log(o);
                console.log(o,i);
                console.log(propkeys.splice(o, 1));
                console.log(propvalues.splice(o, 1));
                console.log(propkeys);
                console.log(propvalues);
                console.log("delete");
                propvalues.splice(o, 1);
                propkeys.splice(o, 1);
                var propobject = {};
                propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
                props.setProp(propobject);
                props.setPropKeys(propkeys);
                props.setPropValues(propvalues);
                setOwnValues(propvalues);
                setOwnKeys(propkeys);
              }}
            >
              Delete
            </button>
          </td>
        </tr>
      );
    });
  }



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
              onChange={(e) => updateMessageKey(e)}
            />
          </td>
          <td>
              <input
                className="form-control"
                type="text"
                value={message2}
                onChange={(e) => updateMessageValue(e)}
              />
            </td>
          <td>
            <button
              id="add-item"
              data-testid="add-item"
              className="btn btn-default"
              type="button"
              onClick={() => handleClick()}
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
DynamicTable.propTypes = {
  current_keys: PropTypes.array,
  current_values: PropTypes.array,
  setPropKeys: PropTypes.array,
  setPropValues: PropTypes.array,
  setProp: PropTypes.func,
};
export default DynamicTable;