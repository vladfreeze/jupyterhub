import React, { useState } from "react";
import "./table-select.css";
import PropTypes from "prop-types";
import { useSelector, useDispatch } from "react-redux";


const DynamicTable = (props) => {
  
  var [current_propobject, setPropObject] = useState(props.current_propobject),
    //[propobject_state, setPropState] = useState(props.setProp),
    //[propkeys_state, setKeysState] = useState(props.setPropKeys),
    //[propvalues_state, setValuesState] = useState(props.setPropValues),
    [propobject, setProp] = useState(""),
    [message, setMessage] = useState(""),
    [message2, setMessage2] = useState("");
  var { propkeys, propvalues, propobject } = props;
  let current_keys = [];
  let current_values = [];
  console.log("RESTART");
  for (var property in current_propobject) {
      current_keys.push(property);
      current_values.push(current_propobject[property]);
      }
  var [propkeys, setPropKeys] = useState(current_keys),
    [propvalues, setPropValues] = useState(current_values);
  

  var updateMessageKey = (event) => {
    setMessage(event.target.value);
  }
  var updateMessageValue = (event) => {
    setMessage2(event.target.value);
  }

  const handleRefresh = () => {
    var propobject = {};
    propkeys.forEach((key, i) => (propobject[key] = propvalues[i]));
    console.log(propobject);
    console.log("HandleRefresh"+propkeys);
    setPropKeys(propkeys);
    setPropValues(propvalues);
    setProp(propobject);
    setMessage("");
    setMessage2("");
    //setKeysState(propkeys);
    //setValuesState(propvalues);
    //setPropState(propobject);
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
  
    setProp(propobject)
    setPropKeys(propkeys);
    setPropValues(propvalues);
    setMessage("");
    setMessage2("");
  
    console.log("STATE KEYS"+ propkeys);
    console.log("STATE VALUES"+ propvalues);
    console.log("STATE Object"+ propobject);
    console.log("STATE Object"+ Object.keys(propobject));
    console.log("STATE Object"+ Object.values(propobject));
  }
  
  const handleItemDeleted = (i) => {
    propvalues.splice(i, 1);
    propkeys.splice(i, 1);
    setPropKeys(propkeys);
    setPropValues(propvalues);
    handleRefresh();
  }
  const renderKeyRows = () => {

    return propkeys.map(function (o, i) {
      //console.log("KeyRows" +i)
      //console.log("KeyRows" +o)
      return (
        <tr key={"item-" + i}>
          <td>
            <input
              className="form-control"
              type="text"
              value={o}
              id={o + i}
              onChange={(i,o) => {
                if (o != "") {
                  propkeys[i] = o;
                }
                console.log("RENDER "+propkeys);
                //handleRefresh();
                
                handleRefresh();
                setPropKeys(propkeys);
                //setKeysState(propkeys);
              }}
            />
          </td>
        </tr>
      );
    });
  }
  const renderValueRows = (props) => {

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
                //handleRefresh();
                setPropValues(propvalues);
                console.log("1"+propvalues.slice(0, -1))
                console.log(props.propvalues)
                console.log("3"+propvalues)
                //setValuesState(propvalues);

                
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
              onClick={handleItemDeleted.bind(i, o)}
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