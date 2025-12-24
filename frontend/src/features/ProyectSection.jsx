import "./ProyectSection.css"
import { useState } from "react";
import { Plus, Trash2 } from 'lucide-react';

const ProyectSection = () => {
    const [nombre, setNombre] = useState("")
    const [lider, setLider] = useState("")
    const [miembros, setMiembros] = useState([
        { nombre: "", rol:""}
    ])
    const [metodologia, setMetodologia] = useState("")

    const agregarMiembro = () => {
        setMiembros([...miembros, { nombre:"", rol:""}])
    }

    const eliminarMiembro = (index) => {
        setMiembros(miembros.filter((_, i) => i !== index))
    }

    const actualizarMiembro = (index, campo, valor) => {
        const copia = [...miembros]
        copia[index][campo] = valor
        setMiembros(copia)
    }

    return (
        <div className="container">
            <fieldset>
                <legend>Datos del Proyecto</legend>
                <div className="form">
                    <label>
                        Nombre del Proyecto:
                        <input 
                            type="text"
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                            placeholder="" 
                        />
                    </label>

                    <label>
                        Líder del Proyecto:
                        <input 
                            type="text"
                            value={lider}
                            onChange={(e) => setLider(e.target.value)}
                            placeholder=""
                        />
                    </label>

                    <div className="team-data">
                        <label>
                            Miembros del Equipo de Desarrollo:
                        </label>
                        {miembros.map((m, i) => (
                            <div key={i} className="fila">
                                <input
                                    className="name" 
                                    type="text"
                                    placeholder="Nombre"
                                    value={m.nombre}
                                    onChange={(e) => 
                                        actualizarMiembro(i, "nombre", e.target.value)
                                    }
                                />
                                <input 
                                    className="rol"
                                    type="text"
                                    placeholder="Rol"
                                    value={m.rol}
                                    onChange={(e) => 
                                        actualizarMiembro(i, "rol", e.target.value)
                                    }
                                />
                                <button
                                    className="add" 
                                    type="button"
                                    onClick={() => agregarMiembro(i)}
                                >
                                    Agregar miembro <Plus />
                                </button>
                                {miembros.length > 1 && (
                                    <button
                                        className="delete" 
                                        type="button"
                                        onClick={() => eliminarMiembro(i)}
                                    >
                                        Eliminar Miembro <Trash2 />
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>

                    <label>
                        Seleccione la metodología utilizada:
                        <select name="" id="">
                            <option value="">-- Seleccione --</option>
                            <option value="1">Scrum</option>
                            <option value="2">Extreme Programming (XP)</option>
                            <option value="3">DSDM</option>
                        </select>
                    </label>
                </div>
            </fieldset>
        </div>
    );
};

export default ProyectSection;