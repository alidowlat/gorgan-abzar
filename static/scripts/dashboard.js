document.addEventListener("DOMContentLoaded", () => {
    const userMenu = document.querySelector('.user-menu');
    const openUserMenu = document.querySelector('.open-user-menu');
    const closeUserMenu = document.querySelector('.close-user-menu');
    const overlayDashboard = document.querySelector('.search-overlay');

    if (!openUserMenu || !userMenu || !overlayDashboard) return;

    openUserMenu.addEventListener("click", () => {
        userMenu.classList.add("active");
        overlayDashboard.classList.add("active");
    });
    overlayDashboard.addEventListener('click', () => {
        userMenu.classList.remove('active')
        overlayDashboard.classList.remove('active')
    });
    closeUserMenu.addEventListener('click', () => {
        userMenu.classList.remove('active')
        overlayDashboard.classList.remove('active')
    });
});


