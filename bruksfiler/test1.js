// Function to display JSON data
function displayData(data) {
    const displayElement = document.getElementById('data-display'); // Replace 'data-display' with your element's ID
    // Manipulate the data as needed and format it for display
    const htmlContent = `<p>Name: ${data.name}</p><p>Age: ${data.age}</p>`;
    displayElement.innerHTML = htmlContent;
  }
  
  // Fetch and display JSON data
  fetch('./testdata/data.json')
    .then(response => response.json())
    .then(data => {
      displayData(data);
    })
    .catch(error => console.error('Error loading JSON data: ', error));
  