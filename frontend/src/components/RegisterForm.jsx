import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './LoginForm.css';

export const RegisterForm = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        nombre: '',
        apellido: ''
    });
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState('');
    const { registrarse } = useAuth();
    const navigate = useNavigate();

    const manejarChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const manejarSubmit = async (e) => {
        e.preventDefault();
        setCargando(true);
        setError('');

        try {
            await registrarse(
                formData.email,
                formData.password,
                formData.nombre,
                formData.apellido
            );
            onSuccess?.();
        } catch (err) {
            setError(err.message);
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-wrapper">
                <div className="login-header">
                    <div className="login-icon">✨</div>
                    <h1>Crear Cuenta</h1>
                    <p>Únete al Generador de Declaraciones</p>
                </div>

                <form onSubmit={manejarSubmit} className="login-form">
                    {error && <div className="error-alert">
                        <span>⚠️</span>
                        <p>{error}</p>
                    </div>}

                    <div className="form-group">
                        <label htmlFor="nombre">👤 Nombre</label>
                        <input
                            id="nombre"
                            name="nombre"
                            type="text"
                            placeholder="Juan"
                            value={formData.nombre}
                            onChange={manejarChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="apellido">👤 Apellido</label>
                        <input
                            id="apellido"
                            name="apellido"
                            type="text"
                            placeholder="Pérez"
                            value={formData.apellido}
                            onChange={manejarChange}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">📧 Email</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="tu@email.com"
                            value={formData.email}
                            onChange={manejarChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">🔑 Contraseña</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            placeholder="••••••••"
                            value={formData.password}
                            onChange={manejarChange}
                            required
                        />
                    </div>

                    <button type="submit" disabled={cargando} className="btn-login">
                        {cargando ? (
                            <>
                                <span className="spinner"></span>
                                Creando cuenta...
                            </>
                        ) : (
                            '→ Registrarse'
                        )}
                    </button>
                </form>

                <div className="login-footer">
                    <p>¿Ya tienes cuenta?</p>
                    <button 
                        type="button" 
                        className="btn-register"
                        onClick={() => navigate('/login')}
                    >
                        Inicia sesión aquí
                    </button>
                </div>
            </div>
        </div>
    );
};