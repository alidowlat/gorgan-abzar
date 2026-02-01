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

document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("addToCartBtn");
    const input = document.getElementById("countInput");
    const productId = addBtn.dataset.product;
    const csrf = getCookie("csrftoken");
    addBtn.addEventListener("click", async function () {
        const count = input.value;
        const res = await fetch("/orders/add-to-cart", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product_id: productId,
                count: count
            })
        });
        const data = await res.json();
        Swal.fire({
            icon: data.icon,
            text: data.text,
            confirmButtonText: "مشاهده سبد خرید",
            showCloseButton: true,
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = "/orders/cart";
            }
        });
    });
    document.querySelector(".increment").addEventListener("click", e => {
        e.preventDefault();
        e.stopPropagation();
        input.value = parseInt(input.value) + 1;
    });

    document.querySelector(".decrement").addEventListener("click", e => {
        e.preventDefault();
        e.stopPropagation();
        if (input.value > 1) {
            input.value = parseInt(input.value) - 1;
        }
    });
});