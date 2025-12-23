function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('click', function (e) {
    const btn = e.target.closest('.remove-address-btn');
    if (!btn) return;

    const addressId = btn.dataset.addressId;

    Swal.fire({
        title: 'از آدرس های شما حذف شود حذف شود؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'حذف',
        cancelButtonText: 'لغو'
    }).then(result => {
        if (!result.isConfirmed) return;

        fetch("/address/delete", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({address_id: addressId})
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    const item = document.querySelector(`.address-item[data-address-id="${addressId}"]`);
                    if (item) item.remove();

                    if (!document.querySelector('.address-item')) {
                        reloadAddressList();
                    }
                }
            });
    });
});

function reloadAddressList() {
    fetch(location.href, {
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    })
        .then(res => res.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContainer = doc.querySelector('#address-container');
            const container = document.querySelector('#address-container');

            if (newContainer && container) {
                container.innerHTML = newContainer.innerHTML;
            }
        });
}

document.addEventListener('click', function(e){
    const btn = e.target.closest('.set-default-btn');
    if(!btn) return;

    const addressId = btn.dataset.id;

    fetch(`/dashboard/address/set-default/${addressId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success'){
            // تمام دکمه‌ها و badge های فعال قبلی رو غیرفعال کن
            document.querySelectorAll('.set-default-btn, .default-badge').forEach(el => {
                el.classList.remove('bg-green-500', 'text-white');
                el.classList.add('bg-amber-400', 'text-white');
                // innerHTML همه رو غیرفعال کن
                if(el.tagName === 'DIV'){
                    el.innerHTML = `<p>غیرفعال</p>
                                    <svg class="size-5">
                                        <use href="#x-mark"></use>
                                    </svg>`;
                    el.classList.add('set-default-btn');
                    el.dataset.id = el.dataset.id || el.getAttribute('data-id');
                } else if(el.tagName === 'BUTTON'){
                    el.querySelector('p').innerText = 'غیرفعال';
                }
            });

            // دکمه انتخاب شده رو فعال کن
            btn.classList.remove('bg-amber-400');
            btn.classList.add('bg-green-500', 'text-white');
            btn.innerHTML = `<p>فعال</p>
                             <svg class="size-6">
                                 <use href="#check-badge"></use>
                             </svg>`;
        }
    });
});
