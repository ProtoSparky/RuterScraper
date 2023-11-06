// Function to display JSON data in a table
function displayData(data) {
    const displayElement = document.getElementById('data-display2');
    let tableContent = `
        <table style="margin: 0 auto; font-family: 'Segoe UI', sans-serif;">
            <tr>
                <th>Bus Route</th>
                <th>Time</th>
            </tr>
    `;

    for (const key in data) {
        const time = data[key][0];
        tableContent += `
            <tr>
                <td>${key}</td>
                <td>${time}</td>
            </tr>
        `;
    }

    tableContent += `</table>`;
    displayElement.innerHTML = tableContent;
}

// Fetch and display JSON data from data2.json
fetch('./testdata/data2.json')
    .then((response) => response.json())
    .then((data) => {
        displayData(data);
    })
    .catch((error) => console.error('Error loading JSON data: ', error));
