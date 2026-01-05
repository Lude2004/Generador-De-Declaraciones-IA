import "./ProyectSection.css"
import { useState, useEffect } from "react";
import { 
    UserPlus, 
    Trash2,
    Pencil,
    Save,
    Check,
    TriangleAlert,
    User  
} from 'lucide-react';
import { getListaMetodologias } from "../services/Api";

const ProyectSection = ({ onSeleccion, datosActuales, onDatosChange }) => {
    const [datos, setDatos] = useState({
        nombreProyecto: "",
        metodologia: ""
    })
    const [equipo, setEquipo] = useState([])
    const [miembro, setMiembro] = useState({
        nombre: "",
        apellido: "",
        rol: ""
    })

    const[touched, setTouched] = useState({
        nombreProyecto: false,
        metodologia: false,
        miembroNombre: false,
        miembroApellido: false,
        miembroRol: false,
    })

    const [editandoId, setEditandoId] = useState(null)
    const [backupMiembro, setBackupMiembro] = useState(null)

    const [opciones, setOpciones] = useState([])

    // Cargar miembros del localStorage al montar
    useEffect(() => {
        const datosGuardados = localStorage.getItem('datosProyecto');
        if (datosGuardados) {
            const datos = JSON.parse(datosGuardados);
            if (datos.miembros && datos.miembros.length > 0) {
                setEquipo(datos.miembros);
            }
        }
    }, []);

    // Sincronizar equipo con el padre
    useEffect(() => {
        onDatosChange({ miembros: equipo });
    }, [equipo, onDatosChange]);

    useEffect(() => {
        getListaMetodologias().then(data => setOpciones(data))
    }, [])

    const handleChangeInput = (e) => {
        const { name, value } = e.target;
        onDatosChange({ [name]: value });
    }

    const handleMetodologiaChange = (e) => {
        const nombreMetodologia = e.target.value;
        onDatosChange({ metodologia: nombreMetodologia });
    }

    const handleMiembroChange = (e) => {
        const { name, value } = e.target;
        setMiembro(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleBlur = (e) => {
        const { name } = e.target;
        
        if (name === "nombreProyecto" || name === "metodologia") {
            setTouched(prev => ({
                ...prev,
                [name]: true
            }))
        }
        else if (name === "nombre") {
            setTouched(prev => ({
                ...prev,
                miembroNombre: true
            }))
        } else if (name === "apellido") {
            setTouched(prev => ({
                ...prev,
                miembroApellido: true
            }))
        } else if (name === "rol") {
            setTouched(prev => ({
                ...prev,
                miembroRol: true
            }))
        }
    }

    const isValid = (field) => {
        return datos[field]?.trim() !== "";
    }

    const isMiembroValid = (field) => {
        return miembro[field]?.trim() !== "";
    }

    const agregarMiembro = (e) => {
        e.preventDefault()
        setTouched(prev => ({
            ...prev,
            miembroNombre: true,
            miembroApellido: true,
            miembroRol: true
        }))
        if (!miembro.nombre || !miembro.apellido || !miembro.rol) return;
        
        const nuevoMiembro = { ...miembro, id: Date.now() };
        const nuevoEquipo = [...equipo, nuevoMiembro];
        
        setEquipo(nuevoEquipo);
        onDatosChange({ miembros: nuevoEquipo }); // Ahora usa el nuevo equipo
        
        setMiembro({ 
            nombre: "", 
            apellido: "", 
            rol: "" 
        })
        setTouched(prev => ({
            ...prev,
            miembroNombre: false,
            miembroApellido: false,
            miembroRol: false
        }))
    }

    const eliminarMiembro = (id) => {
        if (equipo.length === 1) return;
        const nuevoEquipo = equipo.filter(m => m.id !== id);
        setEquipo(nuevoEquipo);
        onDatosChange({ miembros: nuevoEquipo }); // Notificar cambio
    }

    const editarMiembro = (item) => {
        setBackupMiembro({ ...item })
        setEditandoId(item.id)
    }

    const guardarEdicion = (e) => {
        e.preventDefault()
        const equipoActualizado = equipo.map(m =>
            m.id === editandoId ? { ...m, nombre: m.nombre, apellido: m.apellido, rol: m.rol } : m
        );
        setEquipo(equipoActualizado);
        onDatosChange({ miembros: equipoActualizado }); // Agregar esta línea
        setEditandoId(null)
        setMiembro({ nombre: "", apellido: "", rol: "" })
    }

    const cancelarEdicion = () => {
        const equipoActualizado = equipo.map(m =>
            m.id === backupMiembro.id ? backupMiembro : m
        );
        setEquipo(equipoActualizado);
        onDatosChange({ miembros: equipoActualizado }); // Agregar esta línea
        setEditandoId(null)
    }

    return (
        <div className="container">
            <fieldset>
                <legend>Datos del Proyecto de Software</legend>
                <div className="fieldset-container">
                    <div className="form">

                        {/* NOMBRE DEL PROYECTO */}
                        <div className="project-name">
                            <h2>
                                Nombre del Proyecto:
                            </h2>
                            <div className="project-name-entry">
                                <input 
                                    type="text"
                                    name="nombreProyecto"
                                    value={datos.nombreProyecto || datosActuales.nombreProyecto}
                                    placeholder=""
                                    onChange={handleChangeInput}
                                    onBlur={handleBlur}
                                />
                                {touched.nombreProyecto && (
                                    isValid("nombreProyecto")
                                        ? <span className="icon-check"><Check /></span>
                                        : <span className="icon-alert"><TriangleAlert /></span>
                                )}
                            </div>
                        </div>

                        {/* EQUIPO DE DESARROLLO */}
                        <div className="team-data">
                            <h2>
                                Equipo de Desarrollo:
                            </h2>

                            <div className="member-form">
                                <div className="member-name-entry">
                                    <input
                                        className="name" 
                                        type="text"
                                        name="nombre"
                                        placeholder="Nombre"
                                        value={miembro.nombre}
                                        onChange={handleMiembroChange}
                                        onBlur={handleBlur}
                                    />
                                    {touched.miembroNombre && (
                                        isMiembroValid("nombre")
                                            ? <span className="icon-check"><Check /></span>
                                            : <span className="icon-alert"><TriangleAlert /></span>
                                    )} 
                                </div>
                                <div className="member-name-entry">
                                    <input 
                                        className="last-name"
                                        type="text" 
                                        name="apellido"
                                        placeholder="Apellido"
                                        value={miembro.apellido}
                                        onChange={handleMiembroChange}
                                        onBlur={handleBlur}
                                    />
                                    {touched.miembroApellido && (
                                        isMiembroValid("apellido")
                                            ? <span className="icon-check"><Check /></span>
                                            : <span className="icon-alert"><TriangleAlert /></span>
                                    )}                                     
                                </div>
                                <div className="member-rol-entry">
                                    <input 
                                        className="rol"
                                        type="text"
                                        name="rol"
                                        placeholder="Rol"
                                        value={miembro.rol}
                                        onChange={handleMiembroChange}
                                        onBlur={handleBlur}
                                    />
                                    {touched.miembroRol && (
                                        isMiembroValid("rol")
                                            ? <span className="icon-check"><Check /></span>
                                            : <span className="icon-alert"><TriangleAlert /></span>
                                    )}                                     
                                </div>

                                <button
                                    className="add"
                                    type="button"
                                    onClick={agregarMiembro}
                                >
                                    Agregar <UserPlus />
                                </button>
                            </div>

                            {/* LISTA DE LOS MIEMBROS */}
                            <fieldset>
                                <legend className="card-title">Miembros Registrados</legend>
                                <div className="member-list">
                                    {equipo.map(item => (
                                        <div className="member-card" key={item.id}>
                                            {editandoId === item.id ? (
                                                <></>
                                            ) : (
                                                <div className="successful-member-added">
                                                    <User />
                                                </div>
                                            )}

                                            {/* NOMBRE DEL MIEMBRO */}
                                            {editandoId === item.id ? (
                                                <input
                                                    className="edit-name"
                                                    type="text"
                                                    name="nombre"
                                                    value={item.nombre}
                                                    onChange={(e) =>
                                                        setEquipo(
                                                            equipo.map(m =>
                                                                m.id === item.id
                                                                    ? { ...m, nombre: e.target.value }
                                                                    : m
                                                        ))
                                                    } 
                                                />
                                            ) : (
                                                <p className="member-name">
                                                    {item.nombre}
                                                </p>
                                            )}

                                            {/*APELLIDO DEL MIEMBRO */}
                                            {editandoId === item.id ? (
                                                <input
                                                    className="edit-last-name"
                                                    type="text"
                                                    name="apellido"
                                                    value={item.apellido}
                                                    onChange={(e) =>
                                                        setEquipo(
                                                            equipo.map(m =>
                                                                m.id === item.id
                                                                    ? { ...m, apellido: e.target.value }
                                                                    : m
                                                        ))
                                                    }
                                                />
                                            ) : (
                                                <p className="member-last-name">
                                                    {item.apellido}
                                                </p>
                                            )}

                                            {/* ROL DEL MIEMBRO */}
                                            {editandoId === item.id ? (
                                                <input
                                                    className="edit-rol"
                                                    type="text"
                                                    name="rol"
                                                    value={item.rol}
                                                    onChange={(e) =>
                                                        setEquipo(
                                                            equipo.map(m =>
                                                                m.id === item.id
                                                                    ? { ...m, rol: e.target.value }
                                                                    : m
                                                        ))
                                                    }
                                                />
                                            ) : (
                                                <p className="member-rol">
                                                    {item.rol}
                                                </p>
                                            )}

                                            {/* BOTONES */}
                                            <div className="member-actions">

                                                {editandoId === item.id ? (
                                                    <>
                                                        <button
                                                            className="save"
                                                            type="button"
                                                            onClick={guardarEdicion}
                                                        >
                                                            Guardar <Save />
                                                        </button>
                                                        <button
                                                            className="cancel"
                                                            type="button"
                                                            onClick={() => cancelarEdicion()}
                                                        >
                                                            Cancelar
                                                        </button>
                                                    </>
                                                ) : (
                                                    <>
                                                        <button
                                                            className="edit"
                                                            type="button"
                                                            onClick={() => editarMiembro(item)}
                                                        >
                                                            Editar <Pencil />
                                                        </button>
                                                        {equipo.length > 1 && (
                                                            <button
                                                                className="delete"
                                                                type="button"
                                                                onClick={() => eliminarMiembro(item.id)}
                                                            >
                                                                Eliminar <Trash2 />
                                                            </button>
                                                        )}
                                                    </>
                                                )}  

                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </fieldset>
                        </div>

                        {/* METODOLOGÍA ÁGIL */}
                        <div className="agile-methodology">
                            <h2>
                                Metodología utilizada:
                            </h2>
                            <select name="" id="" onChange={handleMetodologiaChange} defaultValue="">
                                <option value="">-- Seleccione --</option>
                                {opciones.map(op => (
                                    <option key={op} value={op}>{op}
                                    </option>
                                ))}
                            </select>
                        </div>

                    </div>
                </div>
            </fieldset>
        </div>
    );
};

export default ProyectSection;