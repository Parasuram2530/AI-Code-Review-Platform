function getToken() {
    return localStorage.getItem('auth_token');
}

function setToken(token) {
    localStorage.setItem('auth_token', token);
}

function removeToken() {
    localStorage.removeItem('auth_token');
}

function redirectIfNoAuth() {
    if (!getToken()) {
        window.location.href = 'index.html';
    }
}

function logout() {
    removeToken();
    window.location.href = 'index.html';
}

async function fetchCurrentUser() {
    const token = getToken();
    if (!token) return null;
    
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (res.ok) {
            return await res.json();
        } else {
            logout();
        }
    } catch (e) {
        console.error("Auth fetch failed", e);
        return null;
    }
}
