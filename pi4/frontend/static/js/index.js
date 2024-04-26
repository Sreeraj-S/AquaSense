const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');

const darkMode = document.querySelector('.dark-mode');
const topTank = document.getElementById('topTank');
const bottomTank = document.getElementById('bottomTank');




var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('mqtt_message', function(msg) {
            var topic = msg.topic;
            var data = msg.data;
            console.log(topic);
            console.log(data);
            if (topic === 'esp32/top/fill') {
                document.getElementById('top_data').innerText = data+"%";
                document.getElementById('top_pect').innerText = data+"%";
                topTank.style.height = data+'%';
            } else if (topic === 'esp32/bottom/fill') {
                document.getElementById('bottom_pect').innerText = data+"%";
                document.getElementById('bottom_data').innerText = data+"%";
                bottomTank.style.height = data+'%';

            } 
            else if (topic === 'esp32/motor') {
                document.getElementById('motor_data').innerText = data;
            } 
        });


menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})


Orders.forEach(order => {
    const tr = document.createElement('tr');
    const trContent = `
        <td>${order.productName}</td>
        <td>${order.productNumber}</td>
        <td>${order.paymentStatus}</td>
        <td class="${order.status === 'Declined' ? 'danger' : order.status === 'Pending' ? 'warning' : 'primary'}">${order.status}</td>
        <td class="primary">Details</td>
    `;
    tr.innerHTML = trContent;
    document.querySelector('table tbody').appendChild(tr);
});


  