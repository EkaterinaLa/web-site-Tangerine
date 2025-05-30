const MenuButton = document.getElementById('MenuButton');
const MenuContent = document.getElementById('MenuContent');
const MenuOverlay = document.getElementById('MenuOverlay');
const CloseMenu = document.getElementById('closeMenu')

MenuButton.addEventListener('click', function() {
    document.body.classList.toggle('menu-open');
    MenuOverlay.style.display = 'block';
})

function closeMenu() {
    document.body.classList.remove('menu-open');
    MenuOverlay.style.display = 'none';
}

MenuOverlay.addEventListener('click', closeMenu);
CloseMenu.addEventListener('click', closeMenu);


const EnterButton = document.getElementById('enter-btn');
const RegisterPanel = document.getElementById('register');
const CloseRegister = document.getElementById('closeRegister');
const RegisterOverlay = document.getElementById('registerOverlay')

EnterButton.addEventListener('click', function() {
    RegisterPanel.classList.add('active');
    RegisterOverlay.style.display = 'block';
})

function closeRegister() {
    RegisterPanel.classList.remove('active');
    RegisterOverlay.style.display = 'none';
}

RegisterOverlay.addEventListener('click', closeRegister);
CloseRegister.addEventListener('click', closeRegister);