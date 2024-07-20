
function ButtonRouter() {
  /*
    This class manages the click on the button,
    making a post request to the http specified in the href tag
    It loads attributes depending on the data-* tag
  */
  
  function constructor() {
    /*
          Constructor of the class
    */
    this.url = "";
    this.barcode = "";
    this.user = "";
    this.method = "";
  }

  this.MakeAction = function (element) {
    /* 
      This method handles the click of the button,
      gets the attributes from data-* tag and calls the method to perform HTTP request
    */
    this.user = element.getAttribute("data-user");
    // this.url = element.getAttribute("href");
    this.url = element.href;
    this.barcode = element.getAttribute("data-barcode");
    this.method = element.getAttribute("data-method");
    this.MakeRequest();
    this.PrintSuccess();
    this.PrintError();
  }

  this.MakeRequest = function () {
    /*
      This method implements the HTTP request call
      The method is forced to post since buttons are used only for post request
      For get request the html a href is enough
    */
    try {
      console.log(
        "Making a " + this.method +
        " call to " + this.url +
        " with user " + this.user +
        " and barcode " + this.barcode
      );
      
      fetch(this.url, {
        method: this.method,
        body: JSON.stringify({
          "username": this.user,
          "barcode": this.barcode
        }),
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (err) {
      console.error(`Error: ${err}`);
    }
  }
    
  this.PrintError = function () {
    var error_msg = '@Session["error_msg"]';
    // document.getElementById("error-msg-div").textContent = error_msg;
    // console.log("Error msg: " + error_msg);
  }
    
  this.PrintSuccess = function () {
    var success_msg = '<%=Session["sucess_msg"]%>';
    // document.getElementById("success-msg-div").textContent = success_msg;
    // console.log("Success msg: " + success_msg);
  }
}


// load of the class
classInstance = new ButtonRouter();