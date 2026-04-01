/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const emailInput = document.getElementById('email');
            const emailValue = emailInput.value;
            const passwordInput = document.getElementById('password');
            const passwordValue = passwordInput.value;
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = '';
            const token = await loginUser(emailValue, passwordValue);
            if (token) {
                document.cookie = `token=${token}; path=/`;
                window.location.href = '/';
            } else {
                errorMessage.textContent = 'Login failed';
            }
        });
    }
});

async function loginUser(email, password) {
    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        return data.access_token;
    } else {
        return false;
    }
}
