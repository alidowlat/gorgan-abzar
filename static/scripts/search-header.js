let debounceTimer;

function searchHandler(query) {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
        const containerDesktop = document.getElementById('searchResult');
        const wrapperDesktop = document.getElementById('desktopSearchResult');
        const queryTextDesktop = wrapperDesktop?.querySelector('.search-query-text');

        const containerMobile = document.getElementById('searchResultMobile');
        const wrapperMobile = document.getElementById('mobileSearchResultsWrapper');
        const queryTextMobile = wrapperMobile?.querySelector('.search-query-text');

        if (containerDesktop && query.length >= 2) {
            fetch(`/search/?search=${encodeURIComponent(query)}`)
                .then(res => res.text())
                .then(html => {
                    containerDesktop.innerHTML = html;
                    wrapperDesktop.classList.remove('hidden');
                    if (queryTextDesktop) queryTextDesktop.textContent = query;
                })
                .catch(() => {
                    containerDesktop.innerHTML = '';
                    if (queryTextDesktop) queryTextDesktop.textContent = '';
                });
        } else if (containerDesktop) {
            containerDesktop.innerHTML = '';
            if (queryTextDesktop) queryTextDesktop.textContent = '';
        }

        if (containerMobile && query.length >= 2) {
            fetch(`/search/?search=${encodeURIComponent(query)}`)
                .then(res => res.text())
                .then(html => {
                    containerMobile.innerHTML = html;
                    wrapperMobile.classList.remove('hidden');
                    if (queryTextMobile) queryTextMobile.textContent = query;
                })
                .catch(() => {
                    containerMobile.innerHTML = '';
                    if (queryTextMobile) queryTextMobile.textContent = '';
                });
        } else if (containerMobile) {
            containerMobile.innerHTML = '';
            if (queryTextMobile) queryTextMobile.textContent = '';
        }
    }, 300);
}

document.querySelectorAll('[data-search-input]').forEach(input => {
    input.addEventListener('input', e => {
        searchHandler(e.target.value.trim());
    });
});

document.querySelectorAll('.popular-search-item').forEach(el => {
    el.addEventListener('click', e => {
        e.preventDefault();

        const desktopInput = document.querySelector('[data-search-input][data-desktop]');
        const mobileInput = document.querySelector('[data-search-input][data-mobile]');
        const text = e.currentTarget.textContent.replace(/^#/, '').trim();

        if (desktopInput) desktopInput.value = text;
        if (mobileInput) mobileInput.value = text;

        searchHandler(text);
    });
});

