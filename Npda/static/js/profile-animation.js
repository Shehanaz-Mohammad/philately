document.addEventListener('DOMContentLoaded', () => {
    const btnRecharge = document.querySelector('.btn-recharge');

    if (btnRecharge) {
        btnRecharge.addEventListener('mouseover', () => {
            btnRecharge.style.transform = 'scale(1.05)';
            btnRecharge.style.transition = 'transform 0.3s ease';
        });

        btnRecharge.addEventListener('mouseout', () => {
            btnRecharge.style.transform = 'scale(1)';
        });
    }
});
