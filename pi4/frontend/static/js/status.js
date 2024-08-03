

let cachedData = null;

function fetchData() {
  fetch('/data')
    .then(response => response.json())
    .then(data => {
      cachedData = data;
      console.log("cachedData=>",cachedData);
      console.log("data=>", data);
      updateUI();
    });
}

function updateUI() {
  if (cachedData) {
    const topFill = cachedData['esp32/top/fill'];
    const bottomFill = cachedData['esp32/bottom/fill'];
    const motorState = cachedData['esp32/motor'];
    const availData = cachedData['esp32/avail'];

    const topDataElement = document.getElementById('top_data');
    topDataElement.innerText = topFill !== undefined ? topFill + "%" : "--";
    topDataElement.innerText = topFill !== undefined ? topFill + "%" : "--";


    const bottomDataElement = document.getElementById('bottom_data');
    bottomDataElement.innerText = bottomFill !== undefined ? bottomFill + "%" : "--";

    const motorDataElement = document.getElementById('motor_data');
    motorDataElement.innerText = motorState === 1 ? "ON" : motorState === 0 ? "OFF" : "--";

    const availDataElement = document.getElementById('avail_data');
    availDataElement.style.backgroundColor = availData === 1 ? 'green' : 'red';

    const topTank = document.getElementById('top-tank');
    topTank.style.height = topFill !== undefined ? `${topFill}%` : '--';

    const bottomTank = document.getElementById('bottom-tank');
    bottomTank.style.height = bottomFill !== undefined ? `${bottomFill}%` : '--';
  }
}


fetchData();

setInterval(fetchData, 1*60*1000);

