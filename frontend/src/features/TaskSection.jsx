import "./TaskSection.css";
import { useState, useEffect } from "react";
import { TriangleAlert } from 'lucide-react';

const TaskSection = ({ estructuraDatos, onTareasChange }) => {
    const [respuestas, setRespuestas] = useState({});

    const handleCheckbox = (nombreTarea, isChecked) => {
        setRespuestas(prev => ({
            ...prev,
            [nombreTarea]: {
                seleccionada: isChecked,
                herramienta: prev[nombreTarea]?.herramienta || "",
                version: prev[nombreTarea]?.version || ""
            }
        }));
    };

    const handleInputChange = (nombreTarea, campo, valor) => {
        setRespuestas(prev => ({
            ...prev,
            [nombreTarea]: {
                ...prev[nombreTarea],
                [campo]: valor
            }
        }));
    };

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
                                            return (
                                                <div key={indexTarea} className="tarea-item">
                                                    <div className="tarea-checkbox">
                                                        <input
                                                            type="checkbox"
                                                            id={`tarea-${indexFase}-${indexTarea}`}
                                                            checked={estaSeleccionada}
                                                            onChange={(e) => handleCheckbox(tarea.nombre, e.target.checked)}
                                                        />
                                                        <label htmlFor={`tarea-${indexFase}-${indexTarea}`}>
                                                            {tarea.nombre}
                                                        </label>
                                                    </div>

                                                    {estaSeleccionada && (
                                                        <div className="tarea-inputs">
                                                            <input
                                                                type="text"
                                                                placeholder="Nombre de la herramienta IA (ej: ChatGPT)"
                                                                value={respuestas[tarea.nombre]?.herramienta || ""}
                                                                onChange={(e) => handleInputChange(tarea.nombre, "herramienta", e.target.value)}
                                                                className="input-herramienta"
                                                            />
                                                            <input
                                                                type="text"
                                                                placeholder="Versión (ej: 4.0)"
                                                                value={respuestas[tarea.nombre]?.version || ""}
                                                                onChange={(e) => handleInputChange(tarea.nombre, "version", e.target.value)}
                                                                className="input-version"
                                                            />
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