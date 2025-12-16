const form = document.getElementById('address-form');
const numericFields = ['plaque', 'postal_code', 'phone_number'];
form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearErrors();

    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: formData
    })
        .then(res => {
            if (!res.ok) return res.json().then(err => Promise.reject(err));
            return res.json();
        })
        .then(data => {
            Swal.fire({
                icon: 'success',
                text: data.message,
                timer: 3500,
                showConfirmButton: false,
                timerProgressBar: true,
                allowOutsideClick: true,
            }).then(result => {
                window.location.href = '/dashboard/address';
            });
        })
        .catch(err => {
            if (err.errors) {
                renderErrors(err.errors);
            }
        });
});

function clearErrors() {
    document.querySelectorAll('[class^="error-"]').forEach(el => {
        el.innerText = '';
    });
}

function renderErrors(errors) {
    for (const field in errors) {
        const el = document.querySelector(`.error-${field}`);
        if (el) el.innerText = errors[field][0];
    }
}

document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('input', function () {
        const errorEl = document.querySelector(`.error-${this.name}`);
        if (errorEl) errorEl.innerText = '';
    });
});

function normalizeToEnglishDigits(value) {
    const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
    return value.replace(/[۰-۹]/g, d => persianDigits.indexOf(d));
}

numericFields.forEach(name => {
    const field = document.querySelector(`[name="${name}"]`);
    if (!field) return;
    field.addEventListener('input', function () {
        let value = normalizeToEnglishDigits(this.value);
        value = value.replace(/[^0-9]/g, '');
        this.value = value;
    });
});
