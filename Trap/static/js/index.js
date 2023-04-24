const log = (text, color) => {
  document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

const socket = new WebSocket('ws://' + location.host + '/echo');
socket.addEventListener('message', ev => {
  const data = JSON.parse(ev.data);
  document.getElementById('log').innerHTML = ''; // Clear existing content
  log('Temperature: ' + data.temperature + '&deg;C', 'black');
  log('Humidity: ' + data.humidity + '%', 'blue');
  log('Pressure: ' + data.pressure + 'hPa', 'green');
});

// const log = (text, color) => {
//   document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
// };

// const socket = new WebSocket('ws://' + location.host + '/echo');
// socket.addEventListener('message', ev => {
//   const data = JSON.parse(ev.data);
//   log('Temperature: ' + data.temperature + '&deg;C', 'black');
//   log('Humidity: ' + data.humidity + '%', 'blue');
//   log('Pressure: ' + data.pressure + 'hPa', 'green');
// });







//const log = (text, color) => {
 //   document.getElementById('temperature').innerHTML = `<span style="color: ${color}">${text}</span><br>`;
 // };
 // const socket = new WebSocket('ws://' + location.host + '/echo');
 // socket.addEventListener('message', ev => {
  //  log('Temperatur: ' + ev.data + "&deg;" + "C", 'black');
  //});

  // const log2 = (text, color) => {
  //   document.getElementById('log2').innerHTML = `<span style="color: ${color}">${text}</span><br>`;
  // };
  // const socket2 = new WebSocket('ws://' + location.host + '/echo');
  // socket2.addEventListener('message', ev => {
  //   log2(ev.data + "c", 'blue');
  // });