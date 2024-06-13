let cachedData = null;

function fetchData() {
  fetch('/data/ai')
    .then(response => response.json())
    .then(data => {
      cachedData = data;
      updateUI();
    });
}

function updateUI() {
  if (cachedData) {
    try{
    const predict_avail = cachedData['esp32/predict_avail'];
    const smart_pump = cachedData['esp32/smart_pump'];

    console.log("predict_avail=>", predict_avail);
    const predictLastRunDate = document.getElementById('predict-last-run-date');
    const predictResultData = document.getElementById('predict-result-data');
    const smartPumpLastRunDate = document.getElementById('smart-pump-last-run-date');
    const smartPumpResultData = document.getElementById('smart-pump-result-data');

    if (predict_avail) {
        const lastPrediction = predict_avail;
        predictLastRunDate.textContent = lastPrediction.timestamp;
        predictResultData.textContent = lastPrediction.result;
    } else {
        predictLastRunDate.textContent = 'No data available';
        predictResultData.textContent = 'No data available';
    }
    if (smart_pump) {
        const lastPrediction = smart_pump;
        smartPumpLastRunDate.textContent = lastPrediction.timestamp;
        smartPumpResultData.textContent = lastPrediction.result;
    } else {
        smartPumpLastRunDate.textContent = 'No data available';
        smartPumpResultData.textContent = 'No data available';
    }
    } catch (error) {
        console.error('Error fetching AI data:', error);
        predictLastRunDate.textContent = 'Error fetching data';
        predictResultData.textContent = 'Error fetching data';
    }
  }
}


fetchData();

setInterval(fetchData, 1*60*1000);

