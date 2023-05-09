const log = (text, color) => {
  document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

const log2 = (text, color, size) => {
  document.getElementById('log2').innerHTML += `<span style="color: ${color}; font-size: ${size}em">${text}</span><br>`;
};

const log3 = (text, color, size) => {
  document.getElementById('log3').innerHTML += `<span style="color: ${color}; font-size: ${size}em">${text}</span><br>`;
};


const cards = [
  {
    imageSrc: "dblbSvirre.jpg",
    title: "Mørk jordhumle",
    text: "Arten er en de mest almindelige humlebier i Danmark. Humlebierne har et-årige samfund og få overvintrende dronninger fører slægten videre året efter."
  },
  {
    imageSrc: "dblbSvirre.jpg",
    title: "Hullubullu",
    text: "Arten er en efter."
  },
  {
    imageSrc: "dblbSvirre.jpg",
    title: "Halaballa",
    text: "Arten er slægten videre året efter."
  },
  // Add more card objects here
];


const renderCard = (card) => {
  return `
    <div class="card" style="width: 18rem;">
      <img class="card-img-top" src="static/${card.imageSrc}">
      <div class="card-body">
        <h5 class="card-title">${card.title}</h5>
        <p class="card-text">${card.text}</p>
      </div>
    </div>
  `;
};

const renderRandomCards = () => {
  const container = document.getElementById('speciesCards');

  // Clear existing content
  container.innerHTML = '';

  // Select two random cards
  const randomCards = [];
  while (randomCards.length < 3) {
    const randomIndex = Math.floor(Math.random() * cards.length);
    const randomCard = cards[randomIndex];
    if (!randomCards.includes(randomCard)) {
      randomCards.push(randomCard);
    }
  }

  // Render the selected cards
  randomCards.forEach((card) => {
    const cardHtml = renderCard(card);
    container.innerHTML += cardHtml;
  });
};
function reloadImage() {
  const img = document.getElementById('image');
  const newImg = document.createElement('img');
  newImg.style.display = 'none';

  // Preload the new image
  newImg.onload = function() {
    // Replace the old image with the new image
    img.src = newImg.src;
    newImg.remove(); // Remove the hidden img element
    console.log('Image reloaded successfully.');
  };
  newImg.onerror = function() {
    console.log('Failed to load image, retrying in 5 seconds...');
    setTimeout(reloadImage, 500); // Retry after 0.5 seconds
    newImg.remove(); // Remove the hidden img element
  };
  newImg.src = img.src.split('?')[0] + '?rand=' + Math.random(); // Add random query param to force reload

  // Append the hidden img element to the document body
  document.body.appendChild(newImg);
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
  log('<strong>Temperatur:</strong> ' + data.temperature + '&deg;C' + '&nbsp &#183 &nbsp' + '<strong>Luftfugtighed:</strong> ' + data.humidity + '%' + '&nbsp &#183 &nbsp' + '<strong>Lufttryk:</strong> ' + data.pressure + 'hPa' , 'black');

  // log('Temperatur: ' + data.temperature + '&deg;C', 'black');
  // log('Luftfugtighed: ' + data.humidity + '%', 'blue');
  // log('Lufttryk: ' + data.pressure + 'hPa', 'green');
  
  document.getElementById('log2').innerHTML = ''; // Clear existing content
  log2('<strong>Oftest set:</strong> ' + data.seenMostClass + ' (' + data.seenMostNumber + ')', 'black', 1.3)
  log2('<strong>Sjældnest set:</strong> ' + data.seenLeastClass + ' (' + data.seenLeastNumber + ')', 'black', 1.3)

  document.getElementById('log3').innerHTML = ''; // Clear existing content
  log3('<strong>Detektioner i dag:</strong> ' + data.sumToday, 'black', 1.3)
  log3('<strong>Detektioner i alt:</strong> ' + data.sumTotal, 'black', 1.3)


  checkImage();
});

// Call renderRandomCards initially and then every 5 seconds
renderRandomCards();
setInterval(renderRandomCards, 60000);



