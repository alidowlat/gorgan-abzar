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

document.addEventListener('DOMContentLoaded', () => {
    // همزمان svg ها را با data-is-favorited هماهنگ کن
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        const svg = btn.querySelector('svg');
        const isFav = btn.dataset.isFavorited === "True" || btn.dataset.isFavorited === "true";
        svg.setAttribute('fill', isFav ? 'currentColor' : 'none');
    });
});

document.addEventListener('click', e => {
    const btn = e.target.closest('.favorite-btn');
    if (!btn) return;

    const productId = btn.dataset.productId;
    const svg = btn.querySelector('svg');

    fetch('/products/toggle-favorite', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({product_id: productId})
    })
        .then(res => {
            if (res.status === 403) {
                Swal.fire({
                    icon: 'warning',
                    title: 'برای انجام این عملیات باید وارد حساب شوید.',
                    showCancelButton: true,
                    confirmButtonText: 'ورود',
                    cancelButtonText: 'انصراف',
                    allowOutsideClick: true,
                    allowEscapeKey: true,
                }).then(result => {
                    if (result.isConfirmed) {
                        window.location.href = '/auth/';
                    }
                });
            }
            return res.json();
        })
        .then(data => {
            if (data.status === 'added') {
                svg.setAttribute('fill', 'currentColor');
                btn.dataset.isFavorited = "true";
            } else if (data.status === 'removed') {
                svg.setAttribute('fill', 'none');
                btn.dataset.isFavorited = "false";
            }
        });
});

document.querySelectorAll('.recommendation-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = btn.querySelector('input[type="radio"]');
        if (!input) return;

        const isSelected = input.dataset.selected === "true";

        if (isSelected) {
            // اگر قبلاً انتخاب شده بود، بردار
            input.checked = false;
            input.dataset.selected = "false";
            btn.classList.remove('ring-2', 'dark:ring-green-600', 'dark:ring-[#EF4343]');
        } else {
            // ابتدا همه رو ریست کن
            document.querySelectorAll('.recommendation-btn').forEach(b => {
                const bInput = b.querySelector('input[type="radio"]');
                bInput.checked = false;
                bInput.dataset.selected = "false";
                b.classList.remove('ring-2', 'ring-green-600', 'dark:ring-green-600', 'ring-[#EF4343]', 'dark:ring-[#EF4343]');
            });

            // سپس دکمه انتخاب شده را فعال کن
            input.checked = true;
            input.dataset.selected = "true";
            if (btn.classList.contains('text-green-600')) {
                btn.classList.add('ring-2', 'focus:ring-green-600', 'dark:focus:ring-green-600');
            } else if (btn.classList.contains('text-red-500')) {
                btn.classList.add('ring-2', 'focus:ring-[#EF4343]', 'dark:focus:ring-[#EF4343]');
            }
        }
    });
});


function sendProductReview(productId) {
    const commentEl = document.getElementById('message');
    const titleEl = document.getElementById('subject');
    const reviewTextError = document.getElementById('review-text-error');
    const reviewTitleError = document.getElementById('review-title-error');
    const errorBox = document.getElementById('review-error-box');
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');

    const recommendationInput = document.querySelector('.recommendation-btn input[name="recommendation"]:checked');

    const comment = commentEl ? commentEl.value.trim() : '';
    const title = titleEl ? titleEl.value.trim() : '';
    const csrfToken = csrfInput ? csrfInput.value : '';

    if (!comment) {
        reviewTextError.textContent = 'متن دیدگاه نمی‌تواند خالی باشد.';
        reviewTextError.classList.remove('hidden');
        commentEl.classList.add('placeholder:text-warning', 'border-warning');
        return;
    }
    if (!title) {
        reviewTitleError.textContent = 'عنوان دیدگاه نمی‌تواند خالی باشد.';
        reviewTitleError.classList.remove('hidden');
        titleEl.classList.add('placeholder:text-warning', 'border-warning');
        return;
    }

    reviewTextError.textContent = '';
    reviewTextError.classList.add('hidden');
    commentEl.classList.remove('placeholder:text-warning', 'border-warning');

    reviewTitleError.textContent = '';
    reviewTitleError.classList.add('hidden');
    titleEl.classList.remove('placeholder:text-warning', 'border-warning');

    const formData = new FormData();
    formData.append('text', comment);
    formData.append('title', title);
    formData.append('product_id', productId);
    if (csrfToken) formData.append('csrfmiddlewaretoken', csrfToken);
    if (recommendationInput) formData.append('recommendation', recommendationInput.value);

    const submitBtn = document.querySelector('[onclick^="sendProductReview"]');
    if (submitBtn) submitBtn.disabled = true;

    fetch('/products/add-review', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.html) {
                    const reviewsContainer = document.getElementById('reviews-container');
                    if (reviewsContainer) reviewsContainer.innerHTML = data.html;
                }

                if (data.reviews_count !== undefined) {
                    const countEl = document.getElementById('reviews-count');
                    if (countEl) {
                        countEl.textContent = `(${data.reviews_count} دیدگاه)`;
                    }
                }

                if (commentEl) commentEl.value = '';
                if (titleEl) titleEl.value = '';
                if (recommendationInput) recommendationInput.checked = false;
                document.querySelectorAll('.recommendation-btn')
                    .forEach(b => b.classList.remove('focus:ring-2'));

                Swal.fire({
                    icon: 'success',
                    title: 'دیدگاه شما ثبت شد',
                    text: 'متشکریم.',
                    timer: 3000,
                    showConfirmButton: false,
                    allowOutsideClick: true,
                    timerProgressBar: true
                });
            } else {
                errorBox.textContent = data.error || 'ارسال دیدگاه با خطای نامشخص مواجه شد.';
            }
        })
        .catch(err => {
            console.error(err);
            if (!errorBox.textContent) errorBox.textContent = 'ارسال دیدگاه با خطا مواجه شد.';
        })
        .finally(() => {
            if (submitBtn) submitBtn.disabled = false;
        });
}

function toggleReviewReaction(reviewId, csrfToken, reactionType) {
    const likeBtn = document.querySelector(`#review-${reviewId}-like`);
    const dislikeBtn = document.querySelector(`#review-${reviewId}-dislike`);
    if (!likeBtn || !dislikeBtn) return;

    const likeIcon = likeBtn.querySelector('svg');
    const dislikeIcon = dislikeBtn.querySelector('svg');
    const likeCountSpan = likeBtn.querySelector('.like-count');
    const dislikeCountSpan = dislikeBtn.querySelector('.dislike-count');

    const priorLiked = likeIcon && likeIcon.getAttribute('fill') === 'currentColor';
    const priorDisliked = dislikeIcon && dislikeIcon.getAttribute('fill') === 'currentColor';

    const isTogglingSame = (reactionType === 'like' && priorLiked) || (reactionType === 'dislike' && priorDisliked);

    fetch("/products/toggle-reaction", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            review_id: reviewId,
            reaction: reactionType
        })
    })
        .then(res => {
            if (res.status === 403) {
                Swal.fire({
                    icon: 'warning',
                    title: 'برای انجام این عملیات باید وارد حساب شوید.',
                    showCancelButton: true,
                    confirmButtonText: 'ورود',
                    cancelButtonText: 'انصراف',
                    allowOutsideClick: true,
                    allowEscapeKey: true,
                }).then(result => {
                    if (result.isConfirmed) {
                        window.location.href = '/auth/';
                    }
                });
                throw new Error('Not authenticated');
            }
            if (!res.ok) return res.json().then(j => {
                throw j;
            });
            return res.json();
        })
        .then(data => {
            if (!data) return;

            if (likeCountSpan) likeCountSpan.textContent = data.like_count;
            if (dislikeCountSpan) dislikeCountSpan.textContent = data.dislike_count;

            if (isTogglingSame) {
                if (reactionType === 'like') likeIcon.setAttribute('fill', 'none');
                else dislikeIcon.setAttribute('fill', 'none');
                return;
            }

            if (reactionType === 'like') {
                likeIcon.setAttribute('fill', 'currentColor');
                dislikeIcon.setAttribute('fill', 'none');
            } else {
                dislikeIcon.setAttribute('fill', 'currentColor');
                likeIcon.setAttribute('fill', 'none');
            }
        })
        .catch(e => {
            if (e.message !== 'Not authenticated') {
                Swal.fire({
                    icon: 'error',
                    title: 'خطایی رخ داده است.',
                    text: 'لطفا دوباره تلاش کنید.',
                });
            }
        });
}
