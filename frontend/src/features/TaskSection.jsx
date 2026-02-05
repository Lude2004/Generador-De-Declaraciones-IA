import "./TaskSection.css";
import { useState, useEffect } from "react";
import { 
    TriangleAlert,
    Check 
} from 'lucide-react';

const TaskSection = ({ estructuraDatos, miembros = [], onTareasChange }) => {
    const [respuestas, setRespuestas] = useState({});
    const [tareasDescripcion, setTareasDescripcion] = useState({});
    const[touched, setTouched] = useState({
        nombreHerramienta: false,
        versionHerramienta: false,
        justificacion: false,
    })

    const handleCheckbox = (nombreTarea, isChecked, nombreFase) => {
        setRespuestas(prev => ({
            ...prev,
            [nombreTarea]: {
                seleccionada: isChecked,
                herramienta: prev[nombreTarea]?.herramienta || "",
                version: prev[nombreTarea]?.version || "",
                justificacion: prev[nombreTarea]?.justificacion || "",
                responsable: prev[nombreTarea]?.responsable || "",
                fase: isChecked ? (nombreFase || "") : (prev[nombreTarea]?.fase || ""),
                descripcion: tareasDescripcion[nombreTarea] || nombreTarea
            }
        }));
    };

    const handleInputChange = (nombreTarea, campo, valor) => {
        setTouched(prev => ({
            ...prev,
            [nombreTarea]: {
                ...prev[nombreTarea],
                [campo]:true
            }
        }));
        setRespuestas(prev => ({
            ...prev,
            [nombreTarea]: {
                ...prev[nombreTarea],
                [campo]: valor,
                descripcion: tareasDescripcion[nombreTarea] || nombreTarea
            }
        }));
    };

    const handleResponsableChange = (nombreTarea, responsable) => {
        setRespuestas(prev => ({
            ...prev,
            [nombreTarea]: {
                ...prev[nombreTarea],
                responsable: responsable
            }
        }));
    };

    const handleInputBlur = (nombreTarea, campo) => {
        // Marcar como touched cuando el usuario sale del input
        setTouched(prev => ({
            ...prev,
            [nombreTarea]: {
                ...prev[nombreTarea],
                [campo]: true
            }
        }));
    };

    // Función para validar si un campo es válido
    const isFieldValid = (nombreTarea, campo) => {
        return respuestas[nombreTarea]?.[campo]?.trim() !== "";
    };

    // Mapear descripciones de tareas cuando viene estructuraDatos
    useEffect(() => {
        if (estructuraDatos && estructuraDatos.fases) {
            const mapeo = {};
            estructuraDatos.fases.forEach(fase => {
                if (fase.tareas) {
                    fase.tareas.forEach(tarea => {
                        mapeo[tarea.nombre] = tarea.descripcion;
                    });
                }
            });
            setTareasDescripcion(mapeo);
        }
    }, [estructuraDatos]);

    // AQUÍ AGREGA EL useEffect
    useEffect(() => {
        if (onTareasChange) {
            onTareasChange(respuestas);
        }
    }, [respuestas, onTareasChange]);

    return (
        <div className="container">
            <fieldset>
                <legend>Seleccionar tareas delegadas por IA generativa</legend>
                <div className="fieldset-container">
                    {!estructuraDatos ? (
                        <div className="warning-message">
                            <p className="message-text">
                                <TriangleAlert id="alert-icon" /> Seleccione una metodología para ver las tareas
                            </p>
                        </div>
                    ) : (
                        <div className="metodologia-info">
                            {estructuraDatos.fases.map((fase, indexFase) => (
                                <div key={indexFase} className="fase-section">
                                    <h2 className="fase-name">{fase.nombre}:</h2>
                                    <div className="tareas-list">
                                        {fase.tareas.map((tarea, indexTarea) => {
                                            const estaSeleccionada = respuestas[tarea.nombre]?.seleccionada || false;
                                            const herramientaValida = isFieldValid(tarea.nombre, "herramienta");
                                            const versionValida = isFieldValid(tarea.nombre, "version");
                                            const herramientaTouched = touched[tarea.nombre]?.herramienta || false;
                                            const versionTouched = touched[tarea.nombre]?.version || false;
                                            return (
                                                <div key={indexTarea} className="tarea-item">
                                                    <div className="tarea-checkbox">
                                                        <input
                                                            type="checkbox"
                                                            id={`tarea-${indexFase}-${indexTarea}`}
                                                            checked={estaSeleccionada}
                                                            onChange={(e) => handleCheckbox(tarea.nombre, e.target.checked, fase.nombre)}
                                                        />
                                                        <label htmlFor={`tarea-${indexFase}-${indexTarea}`}>
                                                            {tarea.descripcion}
                                                        </label>
                                                    </div>

                                                    {estaSeleccionada && (
                                                        <div className="tarea-inputs">
                                                            <div className="name-IA">
                                                                <input
                                                                    type="text"
                                                                    placeholder="Nombre de la herramienta IA (ej: ChatGPT)"
                                                                    value={respuestas[tarea.nombre]?.herramienta || ""}
                                                                    onChange={(e) => handleInputChange(tarea.nombre, "herramienta", e.target.value)}
                                                                    className="input-herramienta"
                                                                />
                                                            </div>
                                                            <div className="version-IA">
                                                                <input
                                                                    type="text"
                                                                    placeholder="Versión (ej: 4.0)"
                                                                    value={respuestas[tarea.nombre]?.version || ""}
                                                                    onChange={(e) => handleInputChange(tarea.nombre, "version", e.target.value)}
                                                                    className="input-version"
                                                                />
                                                            </div>
                                                            <div className="justificacion-IA">
                                                                <input
                                                                    type="text"
                                                                    placeholder="Justificación del uso de IA generativa"
                                                                    value={respuestas[tarea.nombre]?.justificacion || ""}
                                                                    onChange={(e) => handleInputChange(tarea.nombre, "justificacion", e.target.value)}
                                                                    className="input-justificacion"
                                                                />
                                                            </div>

                                                            {miembros.length > 1 && (
                                                                <div className="responsable-IA">
                                                                    <select
                                                                        value={respuestas[tarea.nombre]?.responsable || ""}
                                                                        onChange={(e) => handleResponsableChange(tarea.nombre, e.target.value)}
                                                                        className="select-responsable"
                                                                    >
                                                                        <option value="">-- Seleccione responsable --</option>
                                                                        {miembros.map((miembro) => (
                                                                            <option key={miembro.id} value={`${miembro.nombre} ${miembro.apellido}`}>
                                                                                {miembro.nombre} {miembro.apellido} ({miembro.rol})
                                                                            </option>
                                                                        ))}
                                                                    </select>
                                                                </div>
                                                            )}
                                                        </div>
                                                    )}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </fieldset>
        </div>
    );
};

export default TaskSection;