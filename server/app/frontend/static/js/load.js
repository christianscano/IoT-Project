function loadContent(page) {
    // Set the active class on the clicked nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[onclick="loadContent('${page}')"]`).classList.add('active');

    // Load the content based on the page requested
    $('#main-content').load(`${page}`);
}