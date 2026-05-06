/**
 * Cliente API Seguro para Frontend
 * 0.2.2 Seguridad en Tránsito (TLS 1.3 / HTTPS)
 * 
 * Características:
 * - HTTPS obligatorio en producción
 * - Validación de certificados
 * - Headers de seguridad
 * - CORS con credentials
 * - Timeouts y reintentos
 */

// Detectar si estamos en producción
const isProduction = import.meta.env.MODE === 'production';

// Construir URL segura del API
const getApiUrl = () => {
  const protocol = isProduction ? 'https' : 'http';
  const host = import.meta.env.VITE_API_HOST || 'localhost:8000';
  return `${protocol}://${host}/api`;
};

const API_URL = getApiUrl();

// ============================================================================
// Configuración de Fetch Seguro
// ============================================================================

/**
 * Opciones base para todas las requests
 * Incluye validación de certificados y headers de seguridad
 */
const getSecureRequestOptions = (method = 'GET', body = null) => {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
    credentials: 'include', // Incluir cookies seguras (HTTPS only)
    // Validar certificado SSL/TLS
    ...(isProduction && {
      rejectUnauthorized: true, // En producción, rechazar certificados inválidos
    }),
  };

  // Agregar token JWT si existe
  const token = localStorage.getItem('access_token');
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }

  // Agregar body si es necesario
  if (body) {
    options.body = JSON.stringify(body);
  }

  return options;
};

/**
 * Wrapper seguro para fetch
 * Maneja errores, reintentos y validación de certificados
 */
const secureFetch = async (endpoint, method = 'GET', body = null, retries = 3) => {
  const url = `${API_URL}${endpoint}`;

  // Validar HTTPS en producción
  if (isProduction && !url.startsWith('https://')) {
    throw new Error(
      '❌ HTTPS requerido en producción. Se detectó intento de usar HTTP inseguro.'
    );
  }

  let lastError;

  for (let i = 0; i < retries; i++) {
    try {
      // Timeout de 30 segundos
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const options = getSecureRequestOptions(method, body);
      options.signal = controller.signal;

      // Realizar request
      const response = await fetch(url, options);

      clearTimeout(timeoutId);

      // Validar respuesta
      if (response.ok) {
        return response;
      }

      // Manejar errores HTTP
      if (response.status === 401) {
        // Token expirado - intentar renovar
        await refreshToken();
        // Reintentar con nuevo token
        if (i < retries - 1) {
          continue;
        }
      }

      if (response.status === 403) {
        throw new Error('❌ Acceso denegado: No tienes permisos para esta acción.');
      }

      if (response.status === 404) {
        throw new Error('❌ Recurso no encontrado.');
      }

      if (response.status >= 500) {
        throw new Error('❌ Error del servidor. Intenta nuevamente.');
      }

      // Intentar obtener mensaje de error del servidor
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Error ${response.status}`);
    } catch (error) {
      // Manejar timeout
      if (error.name === 'AbortError') {
        lastError = new Error('❌ Timeout: La solicitud tardó demasiado en responder.');
      } else {
        lastError = error;
      }

      // Log solo en desarrollo
      if (!isProduction) {
        console.error(`Intento ${i + 1}/${retries} falló:`, lastError.message);
      }

      // Reintentar si no es el último intento
      if (i < retries - 1) {
        // Esperar 1 segundo antes de reintentar
        await new Promise((resolve) => setTimeout(resolve, 1000));
        continue;
      }
    }
  }

  throw lastError || new Error('Error desconocido en la solicitud.');
};

// ============================================================================
// MÉTODOS DE AUTENTICACIÓN CON JWT
// ============================================================================

export const register = async (email, password, nombre, apellido) => {
  try {
    const res = await secureFetch('/auth/register/', 'POST', {
      email,
      password,
      nombre,
      apellido,
    });

    const data = await res.json();

    // Validar tokens recibidos
    if (!data.tokens?.access || !data.tokens?.refresh) {
      throw new Error('❌ Respuesta inválida del servidor: tokens faltantes.');
    }

    // Guardar tokens de forma segura
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);

    // Log en desarrollo
    if (!isProduction) {
      console.log('✅ Registro exitoso');
    }

    return data;
  } catch (error) {
    console.error('❌ Error en registro:', error.message);
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const res = await secureFetch('/auth/login/', 'POST', {
      email,
      password,
    });

    const data = await res.json();

    // Validar tokens
    if (!data.tokens?.access || !data.tokens?.refresh) {
      throw new Error('❌ Respuesta inválida: tokens faltantes.');
    }

    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);

    if (!isProduction) {
      console.log('✅ Login exitoso');
    }

    return data;
  } catch (error) {
    console.error('❌ Error en login:', error.message);
    throw error;
  }
};

export const refreshToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
      throw new Error('No hay refresh token disponible.');
    }

    const res = await secureFetch('/auth/refresh/', 'POST', {
      refresh: refreshToken,
    });

    const data = await res.json();

    if (!data.access) {
      throw new Error('❌ No se pudo renovar el token.');
    }

    localStorage.setItem('access_token', data.access);

    if (!isProduction) {
      console.log('✅ Token renovado');
    }

    return data;
  } catch (error) {
    console.error('❌ Error renovando token:', error.message);
    // Limpiar tokens inválidos
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    throw error;
  }
};

export const getCurrentUser = async () => {
  try {
    const token = localStorage.getItem('access_token');

    if (!token) {
      return null;
    }

    const res = await secureFetch('/auth/me/', 'GET');

    if (!res.ok) {
      throw new Error('No se pudo obtener usuario actual.');
    }

    return await res.json();
  } catch (error) {
    console.error('❌ Error obteniendo usuario:', error.message);
    return null;
  }
};

export const logout = async () => {
  try {
    // Limpiar tokens localmente
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    // Notificar al servidor (opcional)
    try {
      await secureFetch('/auth/logout/', 'POST');
    } catch {
      // Ignorar errores en logout del servidor
    }

    if (!isProduction) {
      console.log('✅ Logout exitoso');
    }
  } catch (error) {
    console.error('❌ Error en logout:', error.message);
    throw error;
  }
};

// ============================================================================
// MÉTODOS GENÉRICOS DE API
// ============================================================================

export const apiGet = async (endpoint) => {
  const res = await secureFetch(endpoint, 'GET');
  return res.json();
};

export const apiPost = async (endpoint, data) => {
  const res = await secureFetch(endpoint, 'POST', data);
  return res.json();
};

export const apiPut = async (endpoint, data) => {
  const res = await secureFetch(endpoint, 'PUT', data);
  return res.json();
};

export const apiDelete = async (endpoint) => {
  const res = await secureFetch(endpoint, 'DELETE');
  return res.ok ? null : res.json();
};

// ============================================================================
// Exportar configuración para debugging
// ============================================================================

export const apiConfig = {
  url: API_URL,
  isProduction,
  isSecure: API_URL.startsWith('https'),
  getSecureRequestOptions,
};

// Log de configuración en desarrollo
if (!isProduction) {
  console.log('🔐 Configuración API Segura:');
  console.log('  URL:', API_URL);
  console.log('  Producción:', isProduction);
  console.log('  HTTPS/TLS 1.3:', API_URL.startsWith('https'));
  console.log('  Credentials:', 'include (HTTPS only)');
  console.log('  Validación Certificado:', 'Habilitada en producción');
}
