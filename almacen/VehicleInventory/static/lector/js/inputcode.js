class Economico extends React.Component {
  constructor(props) {
    super(props); 
  } 
  render() {
    return (
      <option value={this.props.economico[0]}>{this.props.economico[1]}</option>
    );
  }
} // Economico


class EconomicoSelect extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.changeEconomico(event.target.value);
  }

  render() {
    const economicos = this.props.economicos;
    // const economicos = "[['9', 'T16'], ['10', 'T14'], ['14', 'T27'], ['20', 'J32']]";
    let economicos_replace = economicos.replace(/\'/g, '"'); // replace simple ' by "
    let economicos_obj =  JSON.parse(economicos_replace);

    const economicosOptions = economicos_obj.map(
      (economico) => <Economico economico={economico}/>);
    return (
      <div>
        <label>
          <select onChange={this.handleChange}>
          {economicosOptions}
          </select>
        </label>
        </div>
    );
  }
}


class RequestButton extends React.Component {
  constructor(props) {
    super(props); 
    this.state = {
      token: this.props.token,
      error: "",
      isLoaded: false,
    };  
    this.sendData = this.sendData.bind(this);
  } 
  sendData(){
    /*
    console.log("send data ....WITH TOKEN");
    console.log(this.state.token);
    console.log(this.props.codeslist);
    console.log(this.props.origen);
    */
    const requestOptions = {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.state.token}`},
      body: JSON.stringify({'profile_position_ids': this.props.codeslist,
      "origen": this.props.origen, 
      "destino": this.props.economico})
    };

    fetch("/api/v0/profileposition/lector/", requestOptions)
      .then(response => response.json())
      .then(
        (data) => {
          if ('error' in data) {
            this.setState({
              error: JSON.stringify(data.error),
            });
          console.log("DATA");
          console.log(data);
          }


        },
        // Nota: es importante manejar errores aquí y no en 
        // un bloque catch() para que no interceptemos errores
        // de errores reales en los componentes.
        (error) => {
          console.log("ERROR!!");
          console.log(error);
          this.setState({
            isLoaded: true,
            error: "Error en post"
          });
        } // error
      )
  }
  render() {
    return (
      <div>
        <button onClick={this.sendData} type="button" className="btn btn-primary btn-lg"
          type='button'>Enviar</button>
        <p> {this.state.error} </p>
      </div>
    );
  }
} // RequestButton


class SimpleItem extends React.Component {
  constructor(props) {
    super(props); 
    this.removeTrack = this.removeTrack.bind(this);
  } 
  removeTrack(){
    this.props.onRemove(this.props.number);
    console.log("-----inicio");
    console.log(this.props.number);
    console.log("-----fin");

  }
  render() {
    return (
      <li>
        <div>{this.props.number} <a className="simple-item" onClick={this.removeTrack}> - </a> </div>
      </li>
    );
  }
}


class NumberCodes extends React.Component {
  constructor(props) {
    super(props); 
    this.onRemove = this.onRemove.bind(this);
  }
  
  onRemove(codigo){
    console.log("---------- inicio numbercodes");
    console.log(codigo);
    this.props.onRemove(codigo);
    console.log("---------- fin numbercodes");
  } 
  render() {
    const numbers = this.props.codes;
    // const listItems = numbers.map((number) => <li key={number}>{number}</li>);
    const listItems = numbers.map((number, indice) => <SimpleItem key={indice.toString()} number={number} onRemove={this.onRemove} />);
    return (
      <div>
        <h2>Registrados:</h2>
        <ul>{listItems}</ul>
      </div>
    );
  }
} // NumberCodes

class CodeReader extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
    this.state = { 
      barcode: "",
      codeslist: [],
      economico: "?"
    };
    this.handleValueChange = this.handleValueChange.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.removeCode = this.removeCode.bind(this);
    this.changeEconomico = this.changeEconomico.bind(this);
  }

  componentDidMount(){
    this.nameInput.focus();
  }
  removeCode(codigo){
    console.log(codigo);
  }
  changeEconomico(idEconomico){
    this.setState({economico: idEconomico});
  }
  handleValueChange(event){
    const valor = event.target.value;
    this.setState({barcode: valor});
    if( valor[valor.length - 1] === 'A' ) {
        this.handleSave(event)
    }

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
  } //handlesave
  handleKeyDown(event) {
    if (event.key === 'Enter') {
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
        <NumberCodes codes={this.state.codeslist} 
          onRemove={this.removeCode} />
        <h2>Económico: {this.state.economico}</h2>
        <EconomicoSelect economicos={this.props.profiles_destino} 
          changeEconomico={this.changeEconomico} />
        <RequestButton token={this.props.token} 
          codeslist={this.state.codeslist} 
          economico={this.state.economico}
          origen={this.props.origen}  />
      </div>
    );
  }
} // CodeReader