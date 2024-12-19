// form-animation.js

document.querySelectorAll('.form-group input').forEach(input => {
    input.addEventListener('focus', function () {
        this.style.backgroundColor = '#f0f8ff';
    });

    input.addEventListener('blur', function () {
        this.style.backgroundColor = '#fff';
    });
});
