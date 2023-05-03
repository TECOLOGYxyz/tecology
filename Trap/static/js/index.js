const log = (text, color) => {
  document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

const log2 = (text, color) => {
  document.getElementById('log2').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};


function reloadImage() {
  const img = document.getElementById('image');
  const newImg = new Image();
  newImg.onload = function() {
    // Replace the old image with the new image
    img.src = newImg.src;
    console.log('Image reloaded successfully.');
  }
  newImg.onerror = function() {
    console.log('Failed to load image, retrying in 0.5 seconds...');
    setTimeout(reloadImage, 500); // retry after 0.5 seconds
  }
  newImg.src = img.src.split('?')[0] + '?rand=' + Math.random(); // add random query param to force reload
}

function checkImage() {
  const img = document.getElementById('image');
  const xhr = new XMLHttpRequest();
  xhr.open('HEAD', img.src);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === xhr.DONE) {
      if (xhr.status === 200) {
        console.log('Image loaded successfully.');
        reloadImage();
      } else {
        console.log('Failed to load image, retrying in 5 seconds...');
        setTimeout(checkImage, 500); // retry after 5 seconds
      }
    }
  }
  xhr.send();
}

const socket = new WebSocket('ws://' + location.host + '/echo');
socket.addEventListener('message', ev => {
  const data = JSON.parse(ev.data);
  document.getElementById('log').innerHTML = ''; // Clear existing content
  log('Temperatur: ' + data.temperature + '&deg;C', 'black');
  log('Luftfugtighed: ' + data.humidity + '%', 'blue');
  log('Lufttryk: ' + data.pressure + 'hPa', 'green');
  
  document.getElementById('log2').innerHTML = ''; // Clear existing content
  log2('Detektioner i dag: ' + data.temperature + '     Detektioner i alt: ' + data.temperature, 'black');
  log2('Ofest set: ' + data.temperature + '     Sjældnest set: ' + data.temperature, 'black');
  checkImage();
});


// const log = (text, color) => {
//   document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
// };

// // const reloadImage = () => {
// //   const img = document.getElementById('image');
// //   const timestamp = new Date().getTime();
// //   img.src = img.src.split('?')[0] + '?' + timestamp;
// // };


// function reloadImage() {
//   const img = document.getElementById('image');
//   img.onerror = function() {
//     console.log('Failed to load image, retrying in 5 seconds...');
//     setTimeout(reloadImage, 500); // retry after 0.5 seconds
//   }
//   img.onload = function() {
//     console.log('Image reloaded successfully.');
//   }
//   img.src = img.src + '?rand=' + Math.random(); // add random query param to force reload
// }

// const socket = new WebSocket('ws://' + location.host + '/echo');
// socket.addEventListener('message', ev => {
//   const data = JSON.parse(ev.data);
//   document.getElementById('log').innerHTML = ''; // Clear existing content
//   log('Temperature: ' + data.temperature + '&deg;C', 'black');
//   log('Humidity: ' + data.humidity + '%', 'blue');
//   log('Pressure: ' + data.pressure + 'hPa', 'green');
//   reloadImage();
// });




