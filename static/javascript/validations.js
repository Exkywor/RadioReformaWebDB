function validate(action, field, value, programs = {}, schedule = {}, id ="") {
  switch(field) {
    case "Name":
      let programNames = Object.keys(programs).map(program => programs[program].name) // Retrieve all the program names
      if (isEmpty(value)) // Check if the name is empty
        return displayInputValidation("edit", false, "Name", "Debes añadir un nombre para el programa");
      else if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
        return displayInputValidation("edit", false, "Name", `El nombre no puede contener solo caracteres especiales`);
      else if (programNames.includes(value.trim())) // Check if the name already exists
        if (action === "edit")
          if (programs[id].name !== value.trim()) // In case it's a non-modification for the same program
            return displayInputValidation("edit", false, "Name", `El nombre ${value} ya está asignado a otro programa`);
          else return displayInputValidation("edit", true, field);
        else return displayInputValidation("edit", false, "Name", `El nombre ${value} ya está asignado a otro programa`);
      else
        return displayInputValidation("edit", true, "Name");
    case "Length":
      if (value < 1) // Check if the length is less than 1 (this is impossible due to the limit in the input, but still)
        return displayInputValidation("edit", false, "Length", "La duración debe ser mayor a 0");
      else
        return displayInputValidation("edit", true, "Length");
    case "Topics":
      if (isEmpty(value)) // Check if the topics are empty
        return displayInputValidation("edit", false, "Topics", "Debes añadir al menos un tema para el programa");
      else if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
        return displayInputValidation("edit", false, "Topics", `Los temas no pueden contener solo caracteres especiales`);
      let topics = value.trim()
      for (let i = 0; i < topics.length; i++) {
        if (topics[i] === ",") { // The program finds a ,
          if (i === topics.length-1) // Is it the last character?
            return displayInputValidation("edit", false, "Topics", "Quita las comas al final de los temas");
          else if (topics[i+1] !== " ") // Is it followed by a space?
            return displayInputValidation("edit", false, "Topics", "Separa los temas con una coma seguida de un espacio");
        };
      };
      return displayInputValidation("edit", true, "Topics");
    case "Presenters":
      let presenters = value.trim()
      if (presenters.length > 0) {// Proceed if presenters is not empty, ignore and consider as valid otherwise
        if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
          return displayInputValidation("edit", false, "Presenters", `Los presentadores no pueden contener solo caracteres especiales`);
        for (let i = 0; i < presenters.length; i++) {
          if (presenters[i] === ",") { // The program finds a ,
            if (i === presenters.length-1) // Is it the last character?
              return displayInputValidation("edit", false, "Presenters", "Quita las comas al final de los presentadores");
            else if (presenters[i+1] !== " ") // Is it followed by a space?
              return displayInputValidation("edit", false, "Presenters", "Separa los presentadores con una coma seguida de un espacio");
          };
        };
        return displayInputValidation("edit", true, "Presenters");
      }
      else
        return displayInputValidation("edit", true, "Presenters");
    case "Author":
      if (isEmpty(value)) // Check if the author is empty
        return displayInputValidation("edit", false, "Author", "Debes añadir el productor del programa");
      else if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
        return displayInputValidation("edit", false, "Author", `El productor no puede contener solo caracteres especiales`);
      else
        return displayInputValidation("edit", true, "Author");
    case "DescriptionShort":
      if (isEmpty(value)) // Check if the descriptionShort is empty
        return displayInputValidation("edit", false, "DescriptionShort", "Debes añadir una descripción corta (sinopsis) del programa");
      else if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
        return displayInputValidation("edit", false, "DescriptionShort", `La descripción corta (sinopsis) no puede contener solo caracteres especiales`);
      else if (value.length > 250)
        return displayInputValidation("edit", false, "DescriptionShort", "La descripción corta (sinopsis) contiene más de 250 caracteres");
      else
        return displayInputValidation("edit", true, "DescriptionShort");
    case "DescriptionLong":
      if (isEmpty(value)) // Check if the descriptionLong is empty
        return displayInputValidation("edit", false, "DescriptionLong", "Debes añadir una descripción del programa");
      else if (!isAlphaNumeric(value)) // Check if it's not alphanumeric
        return displayInputValidation("edit", false, "DescriptionLong", `La descripción no puede contener solo caracteres especiales`);
      else
        return displayInputValidation("edit", true, "DescriptionLong");
    case "StreamID":
      let streamIDs = Object.keys(programs).map(ID => programs[program].streamID) // Retrieve all the streamIDs
      if (isEmpty(value)) // Check if the descriptionLong is empty
        return displayInputValidation("edit", false, "StreamID", "Debes asignar un identificador del programa para el stream de audio");
      else if (streamIDs.includes(value.trim())) // Check if the streamID already exists
        return displayInputValidation("edit", false, "StreamID", `El streamID ${value} ya está asignado a otro programa`);
      else
        return displayInputValidation("edit", true, "StreamID");
    // Schedule cases
    case "sunday":
    case "saturday":
    case "friday":
    case "thursday":
    case "wednesday":
    case "tuesday":
    case "monday":
      if (isEmpty(value)) // Is it empty?
        return displayInputValidation("edit", true, field);

      let ogTime = value.trim();
      let times = ogTime.split(", ");
      let validCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ",", " "]
      for (let i = 0; i < ogTime.length; i++) {
        if (!validCharacters.includes(ogTime[i])) // Check if the time contains invalid characters
          return displayInputValidation("edit", false, field, `La hora para el ${field.toUpperCase()} contiene caracteres inválidos: ${ogTime[i]}`);
        // Check that the times are separated by ", "
        if (ogTime[i] === ",") { // The program finds a ,
          if (i === ogTime.length-1) // Is it the last character?
            return displayInputValidation("edit", false, field, `Quita las comas al final de las horas para el ${field.toUpperCase()}`);
          else if (ogTime[i+1] !== " ") // Is it followed by a space?
            return displayInputValidation("edit", false, field, `Separa las horas para el ${field.toUpperCase()} con una coma seguida de un espacio`);
        };
      };
      
      // Check if a time was input
      if (times[0] === ",")
        return displayInputValidation("edit", false, field, `El ${field.toUpperCase()} no puede contener solo una coma`);

      for (const time of times) {
        let split = time.split(":");

        if (split.length <= 1)
          return displayInputValidation("edit", false, field, `La hora para el ${field.toUpperCase()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm`);

        // Check if the time is formatted properly
        // Avoid 05:5
        if (split[1].length < 2)
          return displayInputValidation("edit", false, field, `La hora para el ${field.toUpperCase()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm`);
        // Avoid 050:00 or 05:000
        for (const i in split) {
          if ((split[i].length > 2) || split[i].length === 0)
            return displayInputValidation("edit", false, field, `La hora para el ${field.toUpperCase()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm`);
        };

        // Check that the time doesn't exist already for other programs, in other words, that it's unique
        let timeIndex = ((parseInt(split[0] * 60, 10)) + parseInt(split[1])).toString();
        
        if (Object.keys(schedule[field]).includes(timeIndex)) {
          if (action === "edit")
            // If the timeIndex already exists, check that it belongs to a different program
            // This handles if you add a time to an existing day of a program,
            // because it will try to validate the already existing time
            if (id != schedule[field][timeIndex])
              return displayInputValidation("edit", false, field, `La hora ${time} para el ${field.toUpperCase()} ya está asignada para el programa con ID ${schedule[field][timeIndex]}`);
            else return displayInputValidation("edit", true, field);
          else
            return displayInputValidation("edit", false, field, `La hora ${time} para el ${field.toUpperCase()} ya está asignada para el programa con ID ${schedule[field][timeIndex]}`);
        }
      };
      return displayInputValidation("edit", true, field);
    default:
      return displayInputValidation("edit", true, field);
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

// Check if a string is empty or only whitespaces
function isEmpty(string) {
  if (!string.replace(/\s/g, '').length)
    return true;
  else
    return false;
};

// Based on https://lowrey.me/test-if-a-string-is-alphanumeric-in-javascript/
const isAlphaNumeric = string => {
  // Return whether there are alphanumeric characters in the string
	return string.search(/[a-z\d]/i) >= 0;
};