import { createContext, useState, useEffect } from 'react';
import * as api from '../services/Api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [usuario, setUsuario] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);

    // Verificar si hay token guardado al cargar
    useEffect(() => {
        verificarSesion();
    }, []);

    const verificarSesion = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setCargando(false);
            return;
        }

        try {
            const data = await api.getCurrentUser();
            if (data?.usuario) {
                setUsuario(data.usuario);
            }
        } catch (err) {
            console.log('Token inválido o expirado');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        } finally {
            setCargando(false);
        }
    };

    const registrarse = async (email, password, nombre, apellido) => {
        try {
            setError(null);
            const data = await api.register(email, password, nombre, apellido);
            setUsuario(data.usuario);
            return data;
        } catch (err) {
            setError(err.message);
            throw err;
        }
    };

    const iniciarSesion = async (email, password) => {
        try {
            setError(null);
            const data = await api.login(email, password);
            setUsuario(data.usuario);
            return data;
        } catch (err) {
            setError(err.message);
            throw err;
        }
    };

    const cerrarSesion = async () => {
        try {
            setError(null);
            await api.logout();
            setUsuario(null);
        } catch (err) {
            setError(err.message);
            throw err;
        }
    };

    return (
        <AuthContext.Provider value={{
            usuario,
            cargando,
            error,
            registrarse,
            iniciarSesion,
            cerrarSesion,
            autenticado: !!usuario
        }}>
            {children}
        </AuthContext.Provider>
    );
};