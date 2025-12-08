document.addEventListener('DOMContentLoaded', () => {
    const endpoint = '/products/';
    const filtersForm = {
        sort_by: 'newest',
        page: 1,
        brand: [],
        category: [],
        available: 0,
        featured: 0
    };

    const DOM = {
        productsContainer: document.querySelector('#product-list'),
        paginationWrapper: document.querySelector('#pagination-wrapper'),
        sortButtons: document.querySelectorAll('[data-sort]'),
        categoryCheckboxes: document.querySelectorAll('input[type="checkbox"][name="category"]'),
        brandCheckboxes: document.querySelectorAll('input[type="checkbox"][name="brand"]'),
        availableToggles: [
            document.querySelector('#available-toggle'),
            document.querySelector('#available-toggle5')
        ].filter(Boolean),
        featuredToggles: [
            document.querySelector('#featured-toggle'),
            document.querySelector('#featured-toggle5')
        ].filter(Boolean),
        clearFiltersBtn: document.querySelector('.text-blue-500.cursor-pointer')
    };

    let allowSync = true;

    const showLoading = () => Swal.fire({
        title: 'در حال بارگذاری...',
        didOpen: () => Swal.showLoading(),
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false
    });
    const hideLoading = () => Swal.close();

    const debounce = (fn, delay = 300) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => fn(...args), delay);
        };
    };

    const syncCheckboxGroup = (sourceCheckbox, allCheckboxes) => {
        if (!allowSync) return;
        allowSync = false;
        const checked = sourceCheckbox.checked;
        allCheckboxes.forEach(cb => cb.checked = checked);
        allowSync = true;
    };

    const getSelectedValues = checkboxes =>
        Array.from(checkboxes).filter(cb => cb.checked).map(cb => cb.value);

    const buildQuery = () => {
        const params = new URLSearchParams();
        if (filtersForm.sort_by) params.set('sort_by', filtersForm.sort_by);
        if (filtersForm.page) params.set('page', filtersForm.page);
        if (filtersForm.brand.length) params.set('brand', Array.from(new Set(filtersForm.brand)).join(','));
        if (filtersForm.category.length) params.set('category', Array.from(new Set(filtersForm.category)).join(','));
        if (filtersForm.available) params.set('available', filtersForm.available);
        if (filtersForm.featured) params.set('featured', filtersForm.featured);
        return params.toString();
    };

    const updateURL = () => {
        const query = buildQuery();
        const newUrl = query ? `${endpoint}?${query}` : endpoint;
        history.replaceState(null, '', newUrl);
    };

    const updateProductCount = (doc) => {
        const newCount = doc.querySelector('.product-count')?.textContent;
        if (!newCount) return;
        document.querySelectorAll('.product-count').forEach(el => {
            el.textContent = newCount;
        });
    };


    const fetchProducts = async () => {
        showLoading();
        try {
            const res = await fetch(`${endpoint}?${buildQuery()}`);
            const html = await res.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');

            DOM.productsContainer.innerHTML = doc.querySelector('#product-list')?.innerHTML || '';
            DOM.paginationWrapper.innerHTML = doc.querySelector('#pagination-wrapper')?.innerHTML || '';

            updateProductCount(doc);
            attachPaginationEvents();
            updateURL();
        } finally {
            hideLoading();
        }
    };

    const fetchProductsDebounced = debounce(fetchProducts, 400);

    const attachPaginationEvents = () => {
        const paginationContainer = DOM.paginationWrapper.querySelector('ul');
        if (!paginationContainer) return;

        paginationContainer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', e => {
                e.preventDefault();
                const url = new URL(link.href);
                filtersForm.page = parseInt(url.searchParams.get('page') || 1);
                fetchProductsDebounced();
            });
        });
    };

    const updateSortButtons = () => {
        DOM.sortButtons.forEach(b => {
            if (b.dataset.sort === filtersForm.sort_by) {
                b.classList.replace('text-gray-400', 'text-blue-500');
            } else {
                b.classList.replace('text-blue-500', 'text-gray-400');
            }
        });
    };

    const attachSortEvents = () => {
        DOM.sortButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filtersForm.sort_by = btn.dataset.sort;
                filtersForm.page = 1;
                updateSortButtons();
                fetchProductsDebounced();
            });
        });
    };

    const attachCheckboxEvents = (checkboxes, key) => {
        checkboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                syncCheckboxGroup(cb, checkboxes);
                if (!allowSync) return;
                filtersForm[key] = getSelectedValues(checkboxes);
                filtersForm.page = 1;
                fetchProductsDebounced();
            });
        });
    };

    const attachToggleEvent = () => {
        DOM.availableToggles.forEach(toggle => {
            toggle.addEventListener('change', () => {
                DOM.availableToggles.forEach(t => t.checked = toggle.checked);
                filtersForm.available = toggle.checked ? 1 : 0;
                filtersForm.page = 1;
                fetchProductsDebounced();
            });
        });

        DOM.featuredToggles.forEach(toggle => {
            toggle.addEventListener('change', () => {
                DOM.featuredToggles.forEach(t => t.checked = toggle.checked);
                filtersForm.featured = toggle.checked ? 1 : 0;
                filtersForm.page = 1;
                fetchProductsDebounced();
            });
        });
    };

    const resetFilters = () => {
        filtersForm.sort_by = 'newest';
        filtersForm.page = 1;
        filtersForm.brand = [];
        filtersForm.category = [];
        filtersForm.available = 0;
        filtersForm.featured = 0;

        DOM.categoryCheckboxes.forEach(c => c.checked = false);
        DOM.brandCheckboxes.forEach(c => c.checked = false);
        DOM.availableToggles.forEach(t => t.checked = false);
        DOM.featuredToggles.forEach(t => t.checked = false);
        updateSortButtons();

        fetchProductsDebounced();
    };

    DOM.clearFiltersBtn.addEventListener('click', resetFilters);

    const readFromURL = () => {
        const query = new URLSearchParams(window.location.search);
        filtersForm.sort_by = query.get('sort_by') || 'newest';
        filtersForm.page = parseInt(query.get('page')) || 1;
        filtersForm.brand = query.get('brand') ? query.get('brand').split(',') : [];
        filtersForm.category = query.get('category') ? query.get('category').split(',') : [];
        filtersForm.available = query.get('available') === '1' ? 1 : 0;
        filtersForm.featured = query.get('featured') === '1' ? 1 : 0;

        DOM.categoryCheckboxes.forEach(cb => cb.checked = filtersForm.category.includes(cb.value));
        DOM.brandCheckboxes.forEach(cb => cb.checked = filtersForm.brand.includes(cb.value));
        DOM.availableToggles.forEach(t => t.checked = filtersForm.available === 1);
        DOM.featuredToggles.forEach(t => t.checked = filtersForm.featured === 1);

        updateSortButtons();
    };

    // --- INIT ---
    readFromURL();
    attachSortEvents();
    attachCheckboxEvents(DOM.categoryCheckboxes, 'category');
    attachCheckboxEvents(DOM.brandCheckboxes, 'brand');
    attachToggleEvent();
    fetchProductsDebounced();
});
