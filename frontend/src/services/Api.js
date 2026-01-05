const API_URL = "http://127.0.0.1:8000/api";

export const getListaMetodologias = async () => {
    // Esta coincide con tu path 'api/metodologias-lista/'
    const res = await fetch(`${API_URL}/metodologias-lista/`);
    if (!res.ok) throw new Error("Error cargando lista");
    return await res.json();
};

export const getDetalleMetodologia = async (nombre) => {
    // CORRECCIÓN AQUÍ:
    // Antes decía: /metodologia-detalle/
    // Ahora dice:  /metodologia/ (Tal como lo tienes en urls.py)
    
    // Enviamos el nombre como parámetro ?nombre=Scrum
    const res = await fetch(`${API_URL}/metodologia/?nombre=${nombre}`);
    
    if (!res.ok) throw new Error("Error cargando detalles");
    return await res.json();
};