// Function to calculate the average of all numbers
function calculateAverage(data) {
  const times = data["Sun-2023-11-05"];
  if (times) {
      const totalSeconds = times.reduce((acc, time) => {
          const [hours, minutes, seconds] = time.split(':').map(Number);
          return acc + hours * 3600 + minutes * 60 + seconds;
      }, 0);

      const averageSeconds = totalSeconds / times.length;
      const averageTime = new Date(averageSeconds * 1000).toISOString().substr(11, 8);

      const displayElement = document.getElementById('data-display');
      displayElement.innerHTML = `
          <div style="text-align: center;">
              <h2 style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Gjennomsnitt hele datasettet alle busser</h2>
              <p style="font-size: 24px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">${averageTime}</p>
          </div>`;
  } else {
      const displayElement = document.getElementById('data-display');
      displayElement.innerHTML = '<h2>Data not found for Sun-2023-11-05</h2>';
  }
}

// Fetch and calculate the average from JSON data
fetch('./testdata/data3.json')
  .then((response) => response.json())
  .then((data) => {
      calculateAverage(data);
  })
  .catch((error) => console.error('Error loading JSON data: ', error));