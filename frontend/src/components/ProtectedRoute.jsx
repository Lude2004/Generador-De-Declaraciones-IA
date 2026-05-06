import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export const ProtectedRoute = ({ children }) => {
    const { autenticado, cargando } = useAuth();

    if (cargando) {
        return <div>Cargando...</div>;
    }

    if (!autenticado) {
        return <Navigate to="/login" replace />;
    }

    return children;
};