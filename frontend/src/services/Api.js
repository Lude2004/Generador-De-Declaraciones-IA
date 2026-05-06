const API_URL = "http://127.0.0.1:8000/api";

// MÉTODOS DE AUTENTICACIÓN CON JWT
export const register = async (email, password, nombre, apellido) => {
    const res = await fetch(`${API_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, nombre, apellido })
    });
    
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.error || 'Error al registrar');
    }
    const data = await res.json();
    // Guardar tokens en localStorage
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    return data;
};

export const login = async (email, password) => {
    const res = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.error || 'Error al iniciar sesión');
    }
    const data = await res.json();
    // Guardar tokens en localStorage
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    return data;
};

export const getCurrentUser = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    
    const res = await fetch(`${API_URL}/auth/me/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (!res.ok) return null;
    return await res.json();
};

export const logout = async () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

// MÉTODOS EXISTENTES
export const getListaMetodologias = async () => {
    const res = await fetch(`${API_URL}/lista-metodologias/`);
    if (!res.ok) throw new Error("Error cargando lista");
    return await res.json();
};

export const getDetalleMetodologia = async (nombre) => {
    const res = await fetch(`${API_URL}/metodologia/${nombre}`);
    if (!res.ok) throw new Error("Error cargando detalles");
    return await res.json();
};