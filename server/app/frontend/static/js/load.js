document.addEventListener('DOMContentLoaded', function () {
    // jQuery is required for this approach
    $('.nav-link').on('click', function (e) {
        e.preventDefault();

        const url = $(this).data('url');
        if (url) {
            // Remove 'active' class from all links
            $('.nav-link').removeClass('active');

            // Add 'active' class to the clicked link
            $(this).addClass('active');

            // Load content via jQuery load() method
            $('#main-content').load(url);
        }
    });

    // Automatically load the dashboard content when the page first loads
    const defaultPageUrl = $('.nav-link.active').data('url');
    if (defaultPageUrl) {
        $('#main-content').load(defaultPageUrl);
    }
});

