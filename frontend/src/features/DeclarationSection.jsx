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
        if (!datosProyecto.nombreProyecto) {
            alert("Por favor registra el nombre del proyecto de software");
            return;
        }

        if (!datosProyecto.metodologia) {
            alert("Por favor selecciona la metodología utilizada en el proyecto de software");
            return;
        }

        if (datosProyecto.miembros.length === 0) {
            alert("Por favor registra la(s) persona(s) que forma(n) parte del Equipo de Desarrollo");
            return;
        }        

        if (Object.keys(tareasSeleccionadas).length === 0 || !Object.values(tareasSeleccionadas).some(t => t.seleccionada)) {
            alert("Por favor seleccione al menos una tarea");
            return;
        }

        const tareasIncompletas = Object.entries(tareasSeleccionadas)
            .filter(([_, tarea]) => tarea.seleccionada)
            .filter(([_, tarea]) => !tarea.herramienta?.trim() || !tarea.version?.trim());

        if (tareasIncompletas.length > 0) {
            const nombresTareas = tareasIncompletas.map(([nombre]) => nombre).join("\n");
            alert(`Por favor registra el nombre y la versión de la herramienta IA para las siguientes tareas:\n\n${nombresTareas}`);
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
                            <Cog /> Generar
                        </button>
                        {declaracionGenerada && (
                            <button
                                className="download"
                                type="button"
                                onClick={handleDescargar}
                                disabled={loading}
                            >
                                <ArrowDownToLine /> Descargar PDF 
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