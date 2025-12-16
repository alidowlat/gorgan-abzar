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
    const btn = e.target.closest('.remove-favorite-btn');
    if (!btn) return;

    const productId = btn.dataset.productId;

    Swal.fire({
        title: 'از محصولات مورد علاقه شما حذف شود؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'حذف',
        cancelButtonText: 'لغو'
    }).then(result => {
        if (!result.isConfirmed) return;

        fetch("/favorites/delete", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({product_id: productId})
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    const item = document.querySelector(`.favorite-item[data-product-id="${productId}"]`);
                    if (item) item.remove();

                    if (!document.querySelector('.favorite-item')) {
                        reloadFavorites();
                    }
                }
            });
    });
});

document.getElementById('delete-all-favorites')?.addEventListener('click', function () {
    Swal.fire({
        title: 'تمام محصولات موجود در علاقه مندی ها حذف شوند؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'لغو'
    }).then(result => {
        if (!result.isConfirmed) return;

        fetch("/favorites/delete/all", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    reloadFavorites();
                }
            });
    });
});

function reloadFavorites() {
    fetch(location.href, {
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    })
        .then(res => res.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContainer = doc.querySelector('#favorites-container');
            const container = document.querySelector('#favorites-container');

            if (newContainer && container) {
                container.innerHTML = newContainer.innerHTML;
            }
        });
}
