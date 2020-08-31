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
      msg: "",
      isLoaded: false,
    };  
    this.sendData = this.sendData.bind(this);
  } 
  sendData(){
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
              msg: ""
            });
          console.log("ERROR");
          console.log(data);
          this.props.sendError(JSON.stringify(data.error));
          }

          if ('exito' in data) {
            this.setState({
              error: "",
              msg: "Éxito"
            });
            this.props.clearData();
          }

          console.log("MSG");
          console.log(data);


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
    const economico = this.props.economico;
    return (
      <div>
      { economico === "?" || this.state.error ?
        <button onClick={this.sendData} type="button" className="btn btn-secondary btn-lg"
          type='button' disabled>Enviar</button>
      :
      <button onClick={this.sendData} type="button" className="btn btn-primary btn-lg"
        type='button'>Enviar</button>
      }
    </div>
    );
  }
} // RequestButton


class ListItem extends React.Component {
  constructor(props) {
    super(props); 
    this.removeTrack = this.removeTrack.bind(this);
  } 
  removeTrack(){
    this.props.onRemove(this.props.listId);
  }
  render() {
    return (
      <li>
        <div>{this.props.number} <a className="simple-item" onClick={this.removeTrack}> X </a> </div>
      </li>
    );
  }
}


class NumberCodes extends React.Component {
  constructor(props) {
    super(props); 
    this.onRemove = this.onRemove.bind(this);
  }
  
  onRemove(listId){
    this.props.onRemove(listId);
  } 
  render() {
    const numbers = this.props.codes;
    const listItems = numbers.map((number, indice) => <ListItem listId={indice} key={indice.toString()} number={number} onRemove={this.onRemove} />);
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
      economico: "?",
      msg: "",
      msg_error: "",
    };
    this.handleValueChange = this.handleValueChange.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.removeCode = this.removeCode.bind(this);
    this.changeEconomico = this.changeEconomico.bind(this);
    this.clearData = this.clearData.bind(this);
    this.sendError = this.sendError.bind(this);
  }

  componentDidMount(){
    this.nameInput.focus();
  }
  removeCode(listId){
    let codeslist = this.state.codeslist;
    let removed = codeslist.splice(listId, 1);
    this.setState({codeslist: codeslist});

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
  clearData() {
    this.setState({
      barcode: "",
      codeslist: [],
      economico: "?",
      msg:"Enviado exitósamente"
    });
  }
  sendError(cadena) {
    this.setState({
      msg_error: cadena
    });
  }
  render() {
    const renderAction = this.state.codeslist.length > 0;
    return (
        <div class="container">
          <div className="row">
            <div className="col">
                <h1>{this.state.barcode}</h1>
                {
                  this.state.msg ? (
                    <div class="alert alert-success" role="alert">
                      {this.state.msg}
                    </div>
                    ) : (<div></div>)
                }
                {
                  this.state.msg_error ? (
                    <div class="alert alert-danger" role="alert">
                      {this.state.msg_error}
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    ) : (<div></div>)
                }

                  <div>
                    <input type="text" 
                      ref={(input) => { this.nameInput = input; }} 
                      value={this.state.barcode} 
                      placeholder="Teclea el codigo + Enter" 
                      onChange={this.handleValueChange} 
                      onKeyDown={this.handleKeyDown} />
                  </div>
            </div>
            <div className="col">
              <NumberCodes codes={this.state.codeslist} 
                    onRemove={this.removeCode} />
            </div>
          </div>
          <div className="row">
            <div className="col">
            </div>
            <div className="col">
            {renderAction ? (
              <div>
              <h2>Económico:</h2>
                  <EconomicoSelect economicos={this.props.profiles_destino} 
                    changeEconomico={this.changeEconomico} />
                  <RequestButton token={this.props.token} 
                    codeslist={this.state.codeslist} 
                    economico={this.state.economico}
                    origen={this.props.origen}  
                    clearData={this.clearData} 
                    sendError={this.sendError}
                    />
              </div>
             ): (<div> </div> ) }

            </div>
          </div>
        </div>
    );
  }
} // CodeReader