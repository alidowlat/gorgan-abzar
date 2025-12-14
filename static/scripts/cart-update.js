document.addEventListener("DOMContentLoaded", () => {
    const cartContainer = document.getElementById("cartContainer");

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(c => {
                c = c.trim();
                if (c.startsWith(name + "=")) cookieValue = decodeURIComponent(c.substring(name.length + 1));
            });
        }
        return cookieValue;
    }

    const csrf = getCookie("csrftoken");
    let locked = false;

    cartContainer.addEventListener("click", async (e) => {
        const btn = e.target.closest(".plus, .minus")
        if (!btn || locked) return

        const input = btn.closest(".cart-item").querySelector("input[name='countInput']")
        if (!input) return

        let count = parseInt(input.value) || 1
        const max = parseInt(input.getAttribute("max")) || 1

        if (btn.classList.contains("plus")) {
            if (count >= max) {
                Swal.fire({
                    icon: "warning",
                    text: `حداکثر ظرفیت این محصول ${max} عدد است`
                })
                return
            }
            count += 1
        } else {
            count = Math.max(count - 1, 1)
        }

        input.value = count
        locked = true

        const itemId = input.dataset.item

        const res = await fetch("/orders/cart-update", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({item_id: itemId, count})
        });

        const data = await res.json()

        if (data.status === "ok") {
            if (data.corrected_count !== undefined)
                input.value = data.corrected_count

            if (data.item_total !== undefined)
                document.querySelector(`#item-${itemId}-total`).textContent =
                    data.item_total.toLocaleString()

            if (data.item_raw !== undefined)
                document.querySelector(`#item-${itemId}-raw`).textContent =
                    data.item_raw.toLocaleString()

            if (data.final_price !== undefined)
                document.querySelector("#cart-final-price").textContent =
                    data.final_price.toLocaleString() + " تومان"

            if (data.total_profit !== undefined)
                document.querySelector("#cart-total-profit").textContent =
                    data.total_profit.toLocaleString() + " تومان"

            if (data.total_before_discount !== undefined)
                document.querySelector("#cart-total-before-discount").textContent =
                    data.total_before_discount.toLocaleString() + " تومان"
        }

        if (data.status === "removed") {
            Swal.fire({
                icon: "error",
                text: data.message
            }).then(() => {
                location.reload()
            })
        }

        locked = false
    });

    document.getElementById("cartContainer").addEventListener("click", async (e) => {

        const removeBtn = e.target.closest(".remove-item");
        const clearBtn = e.target.closest(".clear-cart");

        if (!removeBtn && !clearBtn) return;

        e.preventDefault();
        e.stopPropagation();

        let url = "";
        let payload = {};

        if (removeBtn) {
            const itemId = removeBtn.dataset.id;
            url = "/orders/cart-remove";
            payload = {item_id: itemId};
        }

        if (clearBtn) {
            url = "/orders/cart-clear";
            payload = {};
        }

        const res = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (data.status === "ok") {
            document.getElementById("cartContainer").innerHTML = data.body;
        }
    });
});

