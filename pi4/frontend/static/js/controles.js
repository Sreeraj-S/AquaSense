
motorSwitch = document.getElementById('motor-switch');
smartPumpBtn = document.getElementById('smart-pump-button')
predictAvailBtn=document.getElementById('predict-avail-button')
fetch("/switch/state").then((response) => {
    return response.json();
}).then((data) => {
    motorSwitch.checked = data.state === 1;
})


document.addEventListener('DOMContentLoaded', (event) => {
    motorSwitch.addEventListener('change', async (event) => {
        const isChecked = motorSwitch.checked;
        const data = isChecked ? 'on' : 'off';

        try {
            const response = await fetch(`/motor/${data}`, {
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
            motorSwitch.checked = !isChecked;
            alert('Error: ' + error.message);
        }
    });
    smartPumpBtn.addEventListener('click', async (event) => {
        try {
            const response = await fetch('/run/smart-pump', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Ai Called successfully.');
                location.reload();
            } else {
                const errorData = await response.json();
                throw new Error('Failed to Call Ai: ' + errorData.error);
            }
        } catch (error) {
            alert(error.message);
        }
    });
    predictAvailBtn.addEventListener('click', async (event) => {
        try {
            const response = await fetch('/run/predict-avail', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Ai Called successfully.');
            } else {
                const errorData = await response.json();
                throw new Error('Failed to Call Ai: ' + errorData.error);
            }
        } catch (error) {
            alert(error.message);
        }
    });
});
