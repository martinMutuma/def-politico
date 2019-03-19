let loginbutton = document.getElementById("login-button");
let login_email,
  login_password = "";

// add the login event handlers

// login_email event handler
document.getElementById("login_email").oninput = function(event) {
  login_email = event.target.value;
  validateLogin();
};

// login_password event handler
document.getElementById("login_password").oninput = function(event) {
  login_password = event.target.value;
  validateLogin();
};
// this function disables the login button
const disableloginbutton = () => loginbutton.setAttribute("disabled", true);

// validate login function
const validateLogin = () => {
  // checking if both emptyness of values
  if (
    !doesFieldContainValidValue(login_email) &&
    !doesFieldContainValidValue(login_password)
  ) {
    disableloginbutton();
    loginbutton.setAttribute("value", "ENTER BOTH EMAIL & PASSWORD TO LOGIN");
  } // checks if email is the only blank field
  else if (!doesFieldContainValidValue(login_email)) {
    disableloginbutton();
    loginbutton.setAttribute("value", "ENTER EMAIL TO LOGIN");
  } // checks if the password field is the only blank field
  else if (!doesFieldContainValidValue(login_password)) {
    disableloginbutton();
    loginbutton.setAttribute("value", "ENTER PASSWORD TO LOGIN");
  } // check if the email is in the right format
  else if (!emailValidation(login_email)) {
    disableloginbutton();
    loginbutton.setAttribute("value", "ENTER A VALID EMAIL TO LOGIN");
  } // if the password is less than 6 chars , dont validate
  else if (login_password.length < 6) {
    disableloginbutton();
    loginbutton.setAttribute(
      "value",
      "THE PASSWORD MUST BE LONGER THAN 6 CHARACTERS"
    );
  } else {
    loginbutton.setAttribute("value", "LOGIN");
    loginbutton.removeAttribute("disabled");
  }
};

validateLogin();

// signup validation
let registerbutton = document.getElementById("register-button");
let firstname,
  lastname,
  othername,
  phoneNumber,
  passportUrl,
  email,
  password,
  confirm = "";

document.getElementById("firstname").oninput = function(event) {
  firstname = event.target.value;
  validateSignup();
};

document.getElementById("lastname").oninput = function(event) {
  lastname = event.target.value;
  validateSignup();
};

document.getElementById("othername").oninput = function(event) {
  othername = event.target.value;
  validateSignup();
};

document.getElementById("phoneNumber").oninput = function(event) {
  phoneNumber = event.target.value;
  validateSignup();
};

document.getElementById("passportUrl").oninput = function(event) {
  passportUrl = event.target.value;
  validateSignup();
};

document.getElementById("email").oninput = function(event) {
  email = event.target.value;
  validateSignup();
};

document.getElementById("password").oninput = function(event) {
  password = event.target.value;
  validateSignup();
};

document.getElementById("confirm").oninput = function(event) {
  confirm = event.target.value;
  validateSignup();
};

const disableSignUp = () => registerbutton.setAttribute("disabled", true);

const validateSignup = () => {
  if (
    !doesFieldContainValidValue(firstname) ||
    !doesFieldContainValidValue(lastname) ||
    !doesFieldContainValidValue(othername)
  ) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "ALL NAME FIELDS NEED TO BE FILLED TO REGISTER"
    );
  } else if (!doesFieldContainValidValue(phoneNumber)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "PHONE NUMBER HAS TO BE SET TO REGISTER"
    );
  } else if (!doesFieldContainValidValue(passportUrl)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "PASSPORT URL HAS TO BE SET IN ORDER TO REGISTER"
    );
  } else if (!doesFieldContainValidValue(email)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "EMAIL HAS TO BE SET IN ORDER TO REGISTER"
    );
  } else if (!doesFieldContainValidValue(password)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "PASSWORD HAS TO BE SET IN ORDER TO REGISTER"
    );
  } // we do not need to check for the confirm if its empty.
  // we can just check if it matches with the password
  else if (!areValuesEqual(password, confirm)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "THE PASSWORDS NEED TO MATCH TO REGISTER"
    );
  } else if (password.length < 6) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "THE PASSWORD NEEDS TO BE LONGER THAN 6 CHARACTERS TO REGISTER"
    );
  } else if (!isLinkValid(passportUrl)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "THE URL NEEDS TO BE A VALID LINK TO REGISTER"
    );
  } else if (!isPhoneNumberValid(phoneNumber)) {
    disableSignUp();
    registerbutton.setAttribute(
      "value",
      "THE PHONE NUMBER NEEDS TO HAVE ONLY DIGITS TO REGISTER"
    );
  } else {
    registerbutton.removeAttribute("disabled");
    registerbutton.setAttribute("value", "REGISTER");
  }
};

validateSignup();
