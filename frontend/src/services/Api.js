const API_URL = "http://127.0.0.1:8000/api";

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