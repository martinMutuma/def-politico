/**
 * Returns a bool depending on whether the value
 * provided matches an email format or not.
 */
const emailValidation = email => {
  const re = /\S+@\S+\.\S+/;
  return re.test(email);
};

/**
 * Returns a boolean depending on whether the two values provided match
 */

const areValuesEqual = (val1, val2) => val1 === val2;

/**
 * Returns a boolean depending on whether the value is empty or just has
 *      blank spaces instead of a concrete string value
 */
const doesFieldContainValidValue = value => /\S/.test(value) && Boolean(value);

/**
 * Validate url links for passportUrl
 */

var urls_reg = new RegExp(
  "^" +
    "(?:(?:(?:https?|ftp):)?\\/\\/)" +
    "(?:\\S+(?::\\S*)?@)?" +
    "(?:" +
    "(?!(?:10|127)(?:\\.\\d{1,3}){3})" +
    "(?!(?:169\\.254|192\\.168)(?:\\.\\d{1,3}){2})" +
    "(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})" +
    "(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])" +
    "(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}" +
    "(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))" +
    "|" +
    "(?:" +
    "(?:" +
    "[a-z0-9\\u00a1-\\uffff]" +
    "[a-z0-9\\u00a1-\\uffff_-]{0,62}" +
    ")?" +
    "[a-z0-9\\u00a1-\\uffff]\\." +
    ")+" +
    "(?:[a-z\\u00a1-\\uffff]{2,}\\.?)" +
    ")" +
    "(?::\\d{2,5})?" +
    "(?:[/?#]\\S*)?" +
    "$",
  "i"
);

// this function checks if the link is valid
const isLinkValid = url => urls_reg.test(url);

// is the phone number valid
const isPhoneNumberValid = phone => /^\d+$/.test(phone);
