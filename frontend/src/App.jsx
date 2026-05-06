import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { ProtectedRoute } from './components/ProtectedRoute';
import { UserHeader } from './components/UserHeader';
import DeclarationStructure from './pages/DeclarationStructure';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    <Route path="/login" element={<LoginForm onSuccess={() => window.location.href = '/'} />} />
                    <Route path="/register" element={<RegisterForm onSuccess={() => window.location.href = '/login'} />} />
                    
                    <Route 
                        path="/" 
                        element={
                            <ProtectedRoute>
                                <>
                                    <UserHeader />
                                    <DeclarationStructure />
                                </>
                            </ProtectedRoute>
                        } 
                    />
                    
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;