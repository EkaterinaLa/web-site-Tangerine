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