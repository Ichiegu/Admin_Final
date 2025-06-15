// Toggle sidebar on mobile
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const mainContent = document.querySelector('.main-content');

    // Toggle sidebar on mobile
    mobileSidebarToggle.addEventListener('click', function () {
        sidebar.classList.toggle('active');
    });

    // Close sidebar when clicking the close button
    sidebarToggle.addEventListener('click', function () {
        sidebar.classList.remove('active');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (event) {
        if (window.innerWidth <= 992) {
            if (!sidebar.contains(event.target) && !mobileSidebarToggle.contains(event.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
});