import "./Main.css";
import ProyectSection from "../features/ProyectSection";
import TaskSection from "../features/TaskSection";
import DeclarationSection from "../features/DeclarationSection";
import { getDetalleMetodologia } from "../services/Api";
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

    const cargarEstructuraMetodologia = async (nombre) => {
        try {
            const data = await getDetalleMetodologia(nombre);
            setEstructuraMetodologia(data);
            setTareasSeleccionadas({});
        } catch (error) {
            console.error("Error cargando metodología", error);
        }
    };

    const handleTareasChange = (nuevasTareas) => {
        setTareasSeleccionadas(nuevasTareas);
    };

    return (
        <main className="main">
            <div className="info">
                <h2>Para divulgar el uso de IA generativa, complete los campos correspondientes.</h2>
                <p className="text-main">Tras esto, la declaración se generará automáticamente.</p>
            </div>
            <div className="form">
                <ProyectSection
                    datosActuales={datosProyecto}
                    onDatosChange={handleProyectoChange}
                />
                <TaskSection 
                    estructuraDatos={estructuraMetodologia}
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