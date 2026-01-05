import "./DeclarationSection.css"
import { useState } from "react";
import { 
    Cog,
    ArrowDownToLine
} from 'lucide-react';

const DeclarationSection  = ({ datosProyecto, tareasSeleccionadas, onDeclaracionRecibida }) => {
    const [loading, setLoading] = useState(false)
    const [declaracionGenerada, setDeclaracionGenerada] = useState("")

    const handleGenerar = async () => {
        // Validar que haya datos
        if (!datosProyecto.nombreProyecto || !datosProyecto.metodologia || datosProyecto.miembros.length === 0) {
            alert("Por favor complete los campos: Nombre del Proyecto, Metodología y Equipo de Desarrollo");
            return;
        }

        if (Object.keys(tareasSeleccionadas).length === 0 || !Object.values(tareasSeleccionadas).some(t => t.seleccionada)) {
            alert("Por favor seleccione al menos una tarea");
            return;
        }

        setLoading(true);  

        const payload = {
            proyecto: datosProyecto,
            tareas: tareasSeleccionadas
        };

        try {
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

    const handleDescargar = async () => {
        const payload = {
            proyecto: datosProyecto,
            tareas: tareasSeleccionadas
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/api/descargar-pdf/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Error descargando PDF");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Declaracion_IA_${datosProyecto.nombreProyecto}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
        } catch (error) {
            alert("Error al descargar PDF: " + error.message);
        }
    };

    return (
        <div className="container">
            <fieldset>
                <legend>Declaración generada</legend>
                <div className="fieldset-container">
                    <div className="buttons-container">
                        <button
                            className="generator"
                            type="button"
                            onClick={handleGenerar}
                            disabled={loading}
                        >
                            Generar <Cog />
                        </button>
                        {declaracionGenerada && (
                            <button
                                className="download"
                                type="button"
                                onClick={handleDescargar}
                                disabled={loading}
                            >
                                Descargar PDF <ArrowDownToLine /> 
                            </button>
                        )}
                    </div>
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