// Sorts two elements
function sortBy(a, b, by) {
  let c = programs[a][by];
  let d = programs[b][by];

  if (c < d) return -1;
  if (c > d) return 1;
  else {
    if (by === "name") return 0;
    else return sortBy(a, b, "name"); // If they have similar length switch to sorting by name 
  }
}

// Change the sorting of the programs
function changeSorting(method) {
  // Only change if the sorting method is different from the previous one
  if (method !== currentSorting) {
    let translations = {ID: "ID", name: "Nombre", length: "Duración", author: "Productor", topics: "Temas"};

    if (method === "ID") sortedIDs = Object.keys(programs);
    else sortedIDs = sortedIDs.sort((a, b) => sortBy(a, b, method));

    $("#sortingDropdown").text(translations[method]);

    // Reverse the order if the selected direction is descending
    if (currentDirection === "descending") sortedIDs.reverse();

    // Rebuild the table
    $("tbody").empty();
    buildTable();

    // Change the buttons classes
    if (currentSorting != null) // Check that a sorting is set. At launch it will be null
      document.getElementById(`sort${currentSorting}`).classList.replace("btn-secondary", "btn-outline-secondary");
    document.getElementById(`sort${method}`).classList.replace("btn-outline-secondary", "btn-secondary");
    
    if (currentSorting != null) // Check that a sorting is set. At launch it will be null
      $(`#sort${currentSorting}`).removeClass("active");
    $(`#sort${method}`).addClass("active");
    
    currentSorting = method; // Store the new sorting

    hideHidden();
  }
}

// Make the programs ascending or descending
function changeDirection(method) {
  // Only change if the direction is different from the previous one
  if (method !== currentDirection) {
    sortedIDs = sortedIDs.reverse(); // Reverse the array
    currentDirection = method; // Store the new direction

    // Rebuild the table
    $("tbody").empty();
    buildTable();

    // Change the buttons classes
    if (method === "ascending") {
      document.getElementById("directionDescending").classList.replace("btn-dark", "btn-outline-dark");
      document.getElementById("directionAscending").classList.replace("btn-outline-dark", "btn-dark");
    } else {
      document.getElementById("directionAscending").classList.replace("btn-dark", "btn-outline-dark");
      document.getElementById("directionDescending").classList.replace("btn-outline-dark", "btn-dark");
    }

    hideHidden();
  }
}

function hideHidden() {
  // Hide the columns that should be hidden
  for (const column of Object.keys(visibleColumns)) {
    if (!visibleColumns[column]) $(`.${column}`).hide();
  }
}

// Replace accents and some special characters
// Function thanks to marcelo-ribeiro
// https://gist.github.com/marcelo-ribeiro/abd651b889e4a20e0bab558a05d38d77
function slugify(str) {
  let map = {
      '-' : ' ',
      '-' : '_',
      ""  : ',',
      'a' : 'á|à|ã|â|À|Á|Ã|Â',
      'e' : 'é|è|ê|É|È|Ê',
      'i' : 'í|ì|î|Í|Ì|Î',
      'o' : 'ó|ò|ô|õ|Ó|Ò|Ô|Õ',
      'u' : 'ú|ù|û|ü|Ú|Ù|Û|Ü',
      'c' : 'ç|Ç',
      'n' : 'ñ|Ñ'
  };
  
  str = str.toLowerCase();
  
  for (let pattern in map) {
      str = str.replace(new RegExp(map[pattern], 'g'), pattern);
  };

  return str;
};