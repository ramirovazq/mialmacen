class ItemSelect extends React.Component {
    constructor(props) {
      super(props); 
    } 
    render() {
      return (
        <option value={this.props.values[0]}>{this.props.values[1]}</option>
      );
    }
  }
  
  class GenericSelect extends React.Component {
    constructor(props) {
      super(props);
      this.handleChange = this.handleChange.bind(this);
    }
  
    handleChange(event) {
      this.props.handleChange(event.target.value);
    }
  
    render() {
      const values = this.props.values;
      //console.log(this.props.values);
      // const values = "[['9', 'T16'], ['10', 'T14'], ['14', 'T27'], ['20', 'J32']]";
      let values_replace = values.replace(/\'/g, '"'); // replace simple ' by "
      let values_obj =  JSON.parse(values_replace);
  
      const valuesOptions = values_obj.map(
        (values) => <ItemSelect values={values}/>);
      return (
        <div>
          <label>
            <select onChange={this.handleChange}>
            {valuesOptions}
            </select>
          </label>
          </div>
      );
    }
  }
  
  
  class RequestPositionButton extends React.Component {
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
        body: JSON.stringify({'product': this.props.product,
        "profileposition": this.props.profileposition, 
        "origen": this.props.origen, 
        "destino": this.props.destino,
        "unidad": this.props.unidad, 
        "quantity": this.props.quantity})
      };
  
      fetch("/api/v0/profileposition/init/", requestOptions)
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
  } // RequestPositioButton
  
  
  
  class ConteoForm extends React.Component {
    constructor(props) {
      super(props);
      
      this.state = { 
        quantity: 0,
        profileposition: "?",
        product: "?",
        msg: "",
        msg_error: "",
      };
      this.handleValueChange = this.handleValueChange.bind(this);
      //this.handleSave = this.handleSave.bind(this);
      this.changeProfilePositions = this.changeProfilePositions.bind(this);
      this.changeProducts = this.changeProducts.bind(this);
      this.clearData = this.clearData.bind(this);
      this.sendError = this.sendError.bind(this);
    }
  
    componentDidMount(){
    }

    changeProfilePositions(idProfileposition){
      this.setState({profileposition: idProfileposition});
    }
    changeProducts(idProduct){
      this.setState({product: idProduct});
    }

    
    handleValueChange(event){
      const valor = event.target.value;
      this.setState({quantity: valor});
  
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

    clearData() {
      this.setState({
        quantity: 0,
        profileposition: "?",
        product: "?",
        msg:"Enviado exitósamente",
        msg_error: ""
      });
    }
    sendError(cadena) {
      this.setState({
        msg_error: cadena
      });
    }
    render() {
      const renderAction = this.state.quantity > 0 && this.state.profileposition !== "?" && this.state.product !== "?";
      return (
          <div className="container">

            <div className="row">
              <div className="col">

                  {
                    this.state.msg ? (
                      <div className="alert alert-success" role="alert">
                        {this.state.msg}
                      </div>
                      ) : (<div></div>)
                  }
                  {
                    this.state.msg_error ? (
                      <div className="alert alert-danger" role="alert">
                        {this.state.msg_error}
                        <button type="button" className="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      ) : (<div></div>)
                  }

              </div>
            </div>


            <div className="row">
              <div className="col">

                <div>
                  <h2>Posicion: {this.state.profileposition}</h2>
                  <GenericSelect values={this.props.profilepositions} 
                    handleChange={this.changeProfilePositions} />
                </div>


                </div>
                <div className="col">
    
                  <div>
                  <h2>Producto: {this.state.product}</h2>
                      <GenericSelect values={this.props.productos} 
                        handleChange={this.changeProducts} />
                  </div>
                
                </div>
            </div>


            <div className="row">
  
              <div className="col">
              <h2>Cantidad: {this.state.quantity}</h2>  
                    <div>
                      <input type="text" 
                        value={this.state.quantity} 
                        placeholder="Cantidad contabilizada" 
                        onChange={this.handleValueChange} 
                      />
                    </div>
              </div>

              <div className="col">
              {renderAction ? (
              <RequestPositionButton token={this.props.token} 
                    quantity={this.state.quantity}
                    profileposition={this.state.profileposition}
                    product={this.state.product}
                    clearData={this.clearData} 
                    sendError={this.sendError}
                    origen={this.props.origen}
                    destino={this.props.destino}
                    unidad={this.props.unidad}
                    />
                ): (<div> </div> ) }
              </div>
            </div>

          </div>
      );
    }
  } // CodeReader