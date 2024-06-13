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

const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
const storedDarkMode = localStorage.getItem('darkMode');

if (storedDarkMode) {
    if (storedDarkMode === 'true') {
        document.body.classList.add('dark-mode-variables');
        darkMode.querySelector('span:nth-child(1)').classList.remove('active');
        darkMode.querySelector('span:nth-child(2)').classList.add('active');
    }
}

darkMode.addEventListener('click', () => {
    if (document.body.classList.contains('dark-mode-variables')) {
        document.body.classList.remove('dark-mode-variables');
        localStorage.setItem('darkMode', 'false');
        darkMode.querySelector('span:nth-child(1)').classList.add('active');
        darkMode.querySelector('span:nth-child(2)').classList.remove('active');
    } else {
        document.body.classList.add('dark-mode-variables');
        localStorage.setItem('darkMode', 'true');
        darkMode.querySelector('span:nth-child(1)').classList.remove('active');
        darkMode.querySelector('span:nth-child(2)').classList.add('active');
    }
});
