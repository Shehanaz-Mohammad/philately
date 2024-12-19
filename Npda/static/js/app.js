document.getElementById('npdaForm').addEventListener('submit', function(event) {
    let valid = true;

    // Check for Aadhaar number length
    const aadhaarInput = document.getElementById('aadhaar');
    if (aadhaarInput.value.length !== 12) {
        valid = false;
        alert('Aadhaar number must be 12 digits.');
    }

    // Check for deposit amount
    const depositInput = document.getElementById('deposit');
    if (parseInt(depositInput.value) < 200) {
        valid = false;
        alert('Initial deposit must be at least ₹200.');
    }

    if (!valid) {
        event.preventDefault();
    }
});
