import "./Main.css";
import ProyectSection from "../features/ProyectSection";
import TaskSection from "../features/TaskSection";
import DeclarationSection from "../features/DeclarationSection";
import { getDetalleMetodologia } from "../services/api";
import { useState, useEffect } from "react";

const Main = () => {
    const [datosProyecto, setDatosProyecto] = useState({
        nombreProyecto: "",
        miembros: [],
        metodologia: ""
    });
    const [estructuraMetodologia, setEstructuraMetodologia] = useState(null);
    const [tareasSeleccionadas, setTareasSeleccionadas] = useState({});
    const [declaracionGenerada, setDeclaracionGenerada] = useState("");

    // Cargar datos del localStorage al montar
    useEffect(() => {
        const datosGuardados = localStorage.getItem('datosProyecto');
        const tareasGuardadas = localStorage.getItem('tareasSeleccionadas');
        
        if (datosGuardados) {
            const datos = JSON.parse(datosGuardados);
            setDatosProyecto(datos);
            
            // Si hay metodología guardada, cargar sus datos
            if (datos.metodologia) {
                cargarEstructuraMetodologia(datos.metodologia);
            }
        }
        
        if (tareasGuardadas) {
            setTareasSeleccionadas(JSON.parse(tareasGuardadas));
        }
    }, []);

    // Guardar datos cuando cambien
    useEffect(() => {
        localStorage.setItem('datosProyecto', JSON.stringify(datosProyecto));
    }, [datosProyecto]);

    useEffect(() => {
        localStorage.setItem('tareasSeleccionadas', JSON.stringify(tareasSeleccionadas));
    }, [tareasSeleccionadas]);

    const handleProyectoChange = (nuevosDatos) => {
        setDatosProyecto(prev => ({ ...prev, ...nuevosDatos }));

        if (nuevosDatos.metodologia && nuevosDatos.metodologia !== datosProyecto.metodologia) {
            cargarEstructuraMetodologia(nuevosDatos.metodologia);
        }
    };

    const handleTareasChange = (nuevasTareas) => {
        // Filtrar solo las tareas seleccionadas
        const tareasValidas = Object.entries(nuevasTareas)
            .filter(([_, tarea]) => tarea.seleccionada)
            .reduce((acc, [nombre, tarea]) => {
                acc[nombre] = tarea;
                return acc;
            }, {});
        
        // Validar que las tareas seleccionadas tengan campos requeridos
        const tienErrores = Object.entries(tareasValidas).some(([_, tarea]) => 
            !tarea.herramienta?.trim() || !tarea.version?.trim() || !tarea.justificacion?.trim()
        );
        
        if (tienErrores) {
            console.warn("Hay tareas seleccionadas sin herramienta, versión o justificación completas");
        }
        
        // Actualizar estado
        setTareasSeleccionadas(tareasValidas);
    };

    const cargarEstructuraMetodologia = async (nombre) => {
        try {
            const data = await getDetalleMetodologia(nombre);
            setEstructuraMetodologia(data);
            setTareasSeleccionadas({});
        } catch (error) {
            console.error("Error cargando metodología", error);
            // Mostrar error al usuario
            setEstructuraMetodologia({
                error: `No se pudo cargar "${nombre}". Intente nuevamente.`
            });
        }
    };


    return (
        <main className="main">
            <div className="info">
                <h2 className="text-main">Para divulgar el uso de IA generativa, complete los campos correspondientes.</h2>
                <p className="text-main">Tras esto, la declaración se generará automáticamente.</p>
            </div>
            <div className="form">
                <ProyectSection
                    datosActuales={datosProyecto}
                    onDatosChange={handleProyectoChange}
                />
                <TaskSection 
                    estructuraDatos={estructuraMetodologia}
                    miembros={datosProyecto.miembros}
                    onTareasChange={handleTareasChange} 
                />
                <DeclarationSection 
                    datosProyecto={datosProyecto}
                    tareasSeleccionadas={tareasSeleccionadas}
                    onDeclaracionRecibida={setDeclaracionGenerada}
                />
            </div>
        </main>
    )
}

export default Main