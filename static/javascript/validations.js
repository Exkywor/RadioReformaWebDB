function validate(action, field, value, programs = {}, schedule = {}) {
  switch(field) {
    case "name":
      if (value === "Alimento") displayInputValidation("edit", true, "Name");
      else displayInputValidation("edit", false, "Name", "Nombre inválido");
      break;
  }

};

// Handles input's class management
function displayInputValidation(action, valid, field, message = null) {
  // Changes the validation class of the input
  if (valid) {
    if ($(`#${action}${field}`).hasClass("is-invalid")) {
      $(`#${action}${field}`).removeClass("is-invalid")
      $(`#${action}${field}`).addClass("is-valid")
    }
    else $(`#${action}${field}`).addClass("is-valid")
  } else {
    if ($(`#${action}${field}`).hasClass("is-valid")) {
      $(`#${action}${field}`).removeClass("is-valid")
      $(`#${action}${field}`).addClass("is-invalid")
    }
    else $(`#${action}${field}`).addClass("is-invalid")
  };
  
  // Changes the validation class of the tooltip
  $(`#${action}${field}Feedback`).attr("class", valid ? "valid-feedback" : "invalid-feedback")

  if (valid) $(`#${action}${field}Feedback`).empty() // Clears the tooltip
  else $(`#${action}${field}Feedback`).text(message) // Displays an invalid message
};