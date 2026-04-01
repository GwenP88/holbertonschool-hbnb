/* ------ Login / Logout ------ */

/* Wait until the HTML document is fully loaded */
document.addEventListener('DOMContentLoaded', async () => {
    const loginForm = document.getElementById('login-form');

    /* Handle login form submission if the form exists */
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            /* Get the email and password entered by the user */
            const emailInput = document.getElementById('email');
            const emailValue = emailInput.value;
            const passwordInput = document.getElementById('password');
            const passwordValue = passwordInput.value;

            /* Get the element used to display login errors */
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = '';

            /* Send login request and store the returned token */
            const token = await loginUser(emailValue, passwordValue);

            /* Save the token and redirect to the home page if login succeeds */
            if (token) {
                document.cookie = `token=${token}; path=/; max-age=7200`;
                window.location.href = '/';
            } else {
                /* Display an error message if login fails */
                errorMessage.textContent = 'Login failed';
            }
        });
    }

    /* Get the login/logout link element */
    const loginLink = document.getElementById('login-link');

    /* Change the link to logout if a token is found */
    if (loginLink) {
        if (getCookie('token')){
            loginLink.textContent = 'Logout';

            /* Remove the token and redirect to home when logout is clicked */
            loginLink.addEventListener('click', (event) => {
            event.preventDefault();
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
            window.location.href = '/';
        }); 
    }}

    /* Display a welcome message if the user is authenticated */
    const welcomeMessage = document.getElementById('welcome-message');

    if (welcomeMessage) {
        const user = await getCurrentUser();

        /* Show the user's first name if user data is available */
        if (user) {
            welcomeMessage.textContent = `Bonjour ${user.first_name} !`;
        }
    }
});

/* Send login credentials to the API and return the access token */
async function loginUser(email, password) {
    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    /* Return the token if the request succeeds */
    if (response.ok) {
        const data = await response.json();
        return data.access_token;
    } else {
        /* Return false if login fails */
        return false;
    }
}

/* Retrieve the value of a specific cookie by its name */
function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();

        /* Return the cookie value if the name matches */
        if (trimmedCookie.startsWith(name + '=')) {
            return trimmedCookie.substring((name + '=').length);
        }
    }
    /* Return null if the cookie does not exist */
    return null;
}

/* Fetch the currently authenticated user's data from the API */
async function getCurrentUser() {
    const token = getCookie('token');

    /* Stop if no token is found */
    if (!token) {
        return null;
    }

    const response = await fetch('/api/v1/users/me', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    /* Return user data if the request succeeds */
    if (response.ok) {
        return await response.json();
    }
    
    /* Return null if the request fails */
    return null;
}

/* ------ index ------ */