function openOrderModal() {
    document.getElementById('orderModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('orderModal').style.display = 'none';
}

function submitOrder() {
    return true;
}

window.onclick = function(event) {
    const modal = document.getElementById('orderModal');
    if (event.target == modal) {
        closeModal();
    }
}