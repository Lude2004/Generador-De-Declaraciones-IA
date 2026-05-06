import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './LoginForm.css';

export const LoginForm = ({ onSuccess }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState('');
    const { iniciarSesion } = useAuth();
    const navigate = useNavigate();

    const manejarSubmit = async (e) => {
        e.preventDefault();
        setCargando(true);
        setError('');

        try {
            await iniciarSesion(email, password);
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
                    <div className="login-icon">🔐</div>
                    <h1>Acceso</h1>
                    <p>Generador de Declaraciones IA</p>
                </div>

                <form onSubmit={manejarSubmit} className="login-form">
                    {error && <div className="error-alert">
                        <span>⚠️</span>
                        <p>{error}</p>
                    </div>}

                    <div className="form-group">
                        <label htmlFor="email">📧 Email</label>
                        <input
                            id="email"
                            type="email"
                            placeholder="tu@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">🔑 Contraseña</label>
                        <input
                            id="password"
                            type="password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" disabled={cargando} className="btn-login">
                        {cargando ? (
                            <>
                                <span className="spinner"></span>
                                Iniciando sesión...
                            </>
                        ) : (
                            '→ Iniciar Sesión'
                        )}
                    </button>
                </form>

                <div className="login-footer">
                    <p>¿No tienes cuenta?</p>
                    <button 
                        type="button" 
                        className="btn-register"
                        onClick={() => navigate('/register')}
                    >
                        Crear cuenta aquí
                    </button>
                </div>
            </div>
        </div>
    );
};