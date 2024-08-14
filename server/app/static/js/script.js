document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the default form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    // Reset the error message display
    errorMessage.style.display = 'none';
    errorMessage.innerText = '';

    // Basic validation
    if (username.trim() === "" || password.trim() === "") {
        errorMessage.style.display = 'block';
        errorMessage.innerText = 'Please fill in both fields.';
        return;
    }

    // Simulate a server-side validation (replace with actual AJAX request)
    if (username !== "admin" || password !== "password123") {
        errorMessage.style.display = 'block';
        errorMessage.innerText = 'Invalid username or password.';
        return;
    }

    // If validation is successful, submit the form or redirect
    alert("Login successful! Redirecting to dashboard...");
    window.location.href = "/dashboard";  // Replace with actual redirect
});
