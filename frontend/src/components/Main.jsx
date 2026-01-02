import "./Main.css";
import ProyectSection from "../features/ProyectSection";
import TaskSection from "../features/TaskSection";
import DeclarationSection from "../features/DeclarationSection";

const Main = () => {
    return (
        <main className="main">
            <div className="info">
                <h2>Para divulgar el uso de IA generativa, complete los campos correspondientes.</h2>
                <p className="text-main">Tras esto, la declaración se generará automáticamente.</p>
            </div>
            <div className="form">
                <ProyectSection />
                <TaskSection />
                <DeclarationSection />
            </div>
        </main>
    )
}

export default Main