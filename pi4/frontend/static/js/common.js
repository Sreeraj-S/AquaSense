const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkMode = document.querySelector('.dark-mode');



menuBtn.addEventListener('click', () => {
    sideMenu.style.animation = 'showMenu 0.4s ease forwards';
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.animation = 'hideMenu 0.4s ease forwards';
    setTimeout(() => {
        sideMenu.style.display = 'none';
    }, 400); // Match the duration of the animation
});

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
});
