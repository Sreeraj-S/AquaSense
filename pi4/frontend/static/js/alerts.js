let cachedData = null;

sms_alert = document.getElementById('sms-alert-switch');
fetch("/sms_alert/state").then((response) => {
    return response.json();
}).then((data) => {
  sms_alert.checked = data.state === 1;
})


document.addEventListener('DOMContentLoaded', (event) => {
  sms_alert.addEventListener('change', async (event) => {
        const isChecked = sms_alert.checked;
        const data = isChecked ? 'on' : 'off';

        try {
            const response = await fetch(`/sms_alert/${data}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                console.log('Motor data updated successfully.');
            } else {
                throw new Error('Failed to update motor data.');
            }
        } catch (error) {
          sms_alert.checked = !isChecked;
            alert('Error: ' + error.message);
        }
    });
  })

fetchData();

setInterval(fetchData, 1*60*1000);

