import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const generarDeclaracionService = async (payload) => {
    try {
        const response = await apiClient.post('/generar/', payload);
        return response.data;
    } catch (error) {
        throw error;
    }
}