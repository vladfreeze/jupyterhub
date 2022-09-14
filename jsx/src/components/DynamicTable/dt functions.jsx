const handleClick = () => {
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
const handleValueChanged = (i, e) => {
  var propvalues = propvalues;
  var propkeys = propkeys;
  propvalues[i] = e.target.value;

  this.handleRefresh();
  this.setPropKeys(propkeys);
  this.setPropValues(propvalues);
  this.setState({
    propvalues: propvalues,
  });
}
const handleKeyChanged = (i, e) => {
  var propkeys = this.state.propkeys;

  if (event.target.value != "") {
    propkeys[i] = event.target.value;
  }
  console.log(event.target.value);

  if (event.target.value == "") {
    this.handleItemDeleted(i);
  }
  this.handleRefresh(i);
  this.setPropKeys(propkeys);
  this.setState({
    propkeys: propkeys,
  });
}
const handleItemDeleted = (i) => {
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