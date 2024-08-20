$(document).ready(function() {
    $('.nav-link').on('click', function (e) {
        e.preventDefault();

        const url = $(this).data('url');
        if (url) {
            $('.nav-link').removeClass('active');

            $(this).addClass('active');

            $('#main-content').load(url);
        }
    });

    const defaultPageUrl = $('.nav-link.active').data('url');
    if (defaultPageUrl) {
        $('#main-content').load(defaultPageUrl);
    }
});

