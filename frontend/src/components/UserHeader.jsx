import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import './UserHeader.css';

export const UserHeader = () => {
    const { usuario, cerrarSesion } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await cerrarSesion();
            navigate('/login');
        } catch (err) {
            console.error('Error al logout:', err);
        }
    };

    if (!usuario) return null;

    return (
        <header className="user-header">
            <div className="header-left">
                <h1>🤖 Generador de Declaraciones IA</h1>
            </div>
            <div className="header-right">
                <div className="user-info">
                    <div className="user-avatar">{usuario.nombre?.[0]?.toUpperCase()}</div>
                    <div className="user-details">
                        <p className="user-name">{usuario.nombre} {usuario.apellido}</p>
                        <p className="user-email">{usuario.email}</p>
                    </div>
                </div>
                <button onClick={handleLogout} className="logout-btn">
                    🚪 Cerrar Sesión
                </button>
            </div>
        </header>
    );
};
