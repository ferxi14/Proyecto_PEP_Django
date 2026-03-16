// GameVault — scripts principales

// Auto-cerrar mensajes depues de 5 segundos
document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease';
            setTimeout(function () { msg.remove(); }, 500);
        }, 5000);
    });
});
