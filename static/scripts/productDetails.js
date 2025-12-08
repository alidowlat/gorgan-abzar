// CHANGE TAB
document.addEventListener("DOMContentLoaded", () => {
    const buttonsTab = document.querySelectorAll(".tab-btn");
    const contents = document.querySelectorAll(".tab-content");

    buttonsTab.forEach((btn) => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-target");

            buttonsTab.forEach((b) => {
                b.classList.remove("text-blue-500");
                b.classList.add("text-gray-500", "dark:text-gray-300");
            });
            btn.classList.remove("text-gray-500", "dark:text-gray-300");
            btn.classList.add("text-blue-500");

            contents.forEach((content) => {
                if (content.classList.contains(target)) {
                    content.classList.remove("hidden");
                    content.classList.add("block");
                } else {
                    content.classList.remove("block");
                    content.classList.add("hidden");
                }
            });
        });
    });
});


// SHOW MORE COMMENTS
const moreCommentBtn = document.querySelector('.more-comment-btn');
const moreCommentText = document.querySelector('.more-comment-text');
const moreCommentIcon = document.querySelector('.more-comment-icon');
const hiddenCommentItems = document.querySelectorAll('.hidden-comment-item');

if (moreCommentBtn) {
    moreCommentBtn.addEventListener('click', () => {
        hiddenCommentItems.forEach(item => {
            item.classList.toggle('hidden');
            item.classList.toggle('block');
        });

        if (moreCommentText.innerHTML === 'مشاهده بیشتر') {
            moreCommentText.innerHTML = 'مشاهده کمتر';
        } else {
            moreCommentText.innerHTML = 'مشاهده بیشتر';
        }

        moreCommentIcon.classList.toggle('rotate-180');
    });
}


// PRODUCT SLIDER

const openSliderModals = document.querySelectorAll('.open-sliderModal')
const sliderModal = document.querySelector('.slider-modal')
const overlayProductPage = document.querySelector('.overlay')
const closeSliderModal = document.querySelector('.close-sliderModal')

openSliderModals.forEach(el => {
    el.addEventListener('click', () => {
        sliderModal.classList.add('active')
        overlayProductPage.classList.add('active')
    })
})

overlayProductPage.addEventListener('click', () => {
    overlayProductPage.classList.remove('active')
    sliderModal.classList.remove('active')
})

document.addEventListener("DOMContentLoaded", () => {
    if (!closeSliderModal || !sliderModal || !overlayProductPage) return;

    closeSliderModal.addEventListener("click", () => {
        sliderModal.classList.remove("active");
        overlayProductPage.classList.remove("active");
    });
});
