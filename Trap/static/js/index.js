const log = (text, color) => {
  document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

// const reloadImage = () => {
//   const img = document.getElementById('image');
//   const timestamp = new Date().getTime();
//   img.src = img.src.split('?')[0] + '?' + timestamp;
// };


function reloadImage() {
  const img = document.getElementById('image');
  img.onerror = function() {
    console.log('Failed to load image, retrying in 5 seconds...');
    setTimeout(reloadImage, 5000); // retry after 5 seconds
  }
  img.onload = function() {
    console.log('Image reloaded successfully.');
  }
  img.src = img.src + '?rand=' + Math.random(); // add random query param to force reload
}

const socket = new WebSocket('ws://' + location.host + '/echo');
socket.addEventListener('message', ev => {
  const data = JSON.parse(ev.data);
  document.getElementById('log').innerHTML = ''; // Clear existing content
  log('Temperature: ' + data.temperature + '&deg;C', 'black');
  log('Humidity: ' + data.humidity + '%', 'blue');
  log('Pressure: ' + data.pressure + 'hPa', 'green');
  reloadImage();
});




