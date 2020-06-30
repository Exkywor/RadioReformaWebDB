function validate(type, field, value, programs = {}, schedule = {}) {
  if (field === "name") {
    if (value === "Alimento") displayInputValidation("edit", true, "Name")
    else displayInputValidation("edit", false, "Name", "Nombre inválido")
  };
};

// Handles input's class management
function displayInputValidation(type, valid, field, message = null) {
  // Changes the validation class of the input
  if (valid) {
    if ($(`#${type}${field}`).hasClass("is-invalid")) {
      $(`#${type}${field}`).removeClass("is-invalid")
      $(`#${type}${field}`).addClass("is-valid")
    }
    else $(`#${type}${field}`).addClass("is-valid")
  } else {
    if ($(`#${type}${field}`).hasClass("is-valid")) {
      $(`#${type}${field}`).removeClass("is-valid")
      $(`#${type}${field}`).addClass("is-invalid")
    }
    else $(`#${type}${field}`).addClass("is-invalid")
  };
  
  // Changes the validation class of the tooltip
  $(`#${type}${field}Feedback`).attr("class", valid ? "valid-feedback" : "invalid-feedback")

  if (valid) $(`#${type}${field}Feedback`).empty() // Clears the tooltip
  else $(`#${type}${field}Feedback`).text(message) // Displays an invalid message
};