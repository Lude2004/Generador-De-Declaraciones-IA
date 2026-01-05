import "./DeclarationSection.css"
import { useState } from "react";
import { Cog } from 'lucide-react';

const DeclarationSection  = ({ datosProyecto, tareasSeleccionadas, onDeclaracionRecibida }) => {
    const [loading, setLoading] = useState(false)
    const [declaracionGenerada, setDeclaracionGenerada] = useState("")

    const handleGenerar = async () => {
        setLoading(true);  

        // 1. Preparamos el paquete de datos para Django
        const payload = {
            proyecto: datosProyecto,
            tareas: tareasSeleccionadas
        };

        try {
            // 2. Enviamos a Django (Asegúrate de crear esta URL en urls.py)
            const response = await fetch('http://127.0.0.1:8000/api/generar-declaracion/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Error generando declaración");

            const data = await response.json();

            setDeclaracionGenerada(data.texto_declaracion);

            if (onDeclaracionRecibida) {
                onDeclaracionRecibida(data.texto_declaracion);
            }
            
        } catch (error) {
        alert("Hubo un error al conectar con la IA: " + error.message);
        } finally {
        setLoading(false);
        }
    };

    return (
        <div className="container">
            <fieldset>
                <legend>Declaración generada</legend>
                <div className="fieldset-container">
                    <button
                        className="generator"
                        type="button"
                        onClick={handleGenerar}
                        disabled={loading}
                    >
                        Generar <Cog />
                    </button>
                    <textarea 
                        id="output" 
                        readOnly 
                        value={loading ? "Generando..." : declaracionGenerada}
                    ></textarea>
                </div>
            </fieldset>
        </div>
    )
};

export default DeclarationSection;