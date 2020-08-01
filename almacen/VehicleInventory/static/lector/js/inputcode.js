class NumberCodes extends React.Component {
  constructor(props) {
    super(props); 
  } 
  render() {
    const numbers = this.props.codes;
    const listItems = numbers.map((number) => <li key={number}>{number}</li>);
    return (
      <div>
        <h2>Registrados:</h2>
        <ul>{listItems}</ul>
      </div>
    );
  }
}

class CodeReader extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
    this.state = { 
      barcode: "",
      codeslist: [] 
    };
    this.handleValueChange = this.handleValueChange.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
  }

  componentDidMount(){
    this.nameInput.focus();
  }
  handleValueChange(e){
    const x = e.target.value;
    this.setState({barcode: x});
  }//handelValueChange
  handleSave(event){
    let barcode = this.state.barcode;
    let arraycodes = this.state.codeslist;    
    arraycodes.push(barcode);
    this.setState({
      barcode: "",
      codeslist: arraycodes
    });
    event.preventDefault();
    console.log(this.state.codeslist);
  } //handlesave
  handleKeyDown(event) {
    if (event.key === 'Enter') {
      console.log('do validate');
      this.handleSave(event)
    } else {
      console.log('otro');
    }
  }//handelKeyDown

  render() {
    return (
      <div className="InputCodes">
        <h1>{this.state.barcode}</h1>
          <div>
            <input type="text" 
              ref={(input) => { this.nameInput = input; }} 
              value={this.state.barcode} 
              placeholder="Teclea el codigo + Enter" 
              onChange={this.handleValueChange} 
              onKeyDown={this.handleKeyDown} />
          </div>
          <br/>
        <NumberCodes codes={this.state.codeslist} />
      </div>
    );
  }
}
ReactDOM.render(<CodeReader />, document.getElementById('codecontainer'));