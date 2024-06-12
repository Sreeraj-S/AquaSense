
motorSwitch = document.getElementById('motor-switch');
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
});


