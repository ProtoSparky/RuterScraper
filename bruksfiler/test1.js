// Function to display JSON data
function displayData(data) {
    const displayElement = document.getElementById('data-display'); // Replace 'data-display' with your element's ID
  
    // Iterate through the data and create HTML elements
    let htmlContent = '<h2>Data</h2><ul>';
    for (const key in data) {
      htmlContent += `<li>${key}:</li><ul>`;
      data[key].forEach((time, index) => {
        htmlContent += `<li>Time ${index + 1}: ${time}</li>`;
      });
      htmlContent += '</ul>';
    }
    htmlContent += '</ul>';
  
    displayElement.innerHTML = htmlContent;
  }
  
  // Fetch and display JSON data
  fetch('./testdata/data2.json') // Updated the file path to data2.json
    .then((response) => response.json())
    .then((data) => {
      displayData(data);
    })
    .catch((error) => console.error('Error loading JSON data: ', error));
  