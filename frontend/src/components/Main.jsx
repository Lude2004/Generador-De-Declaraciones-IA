import React from "react";
import ProyectSection from "../features/ProyectSection";
import TaskSection from "../features/TaskSection";
import DeclarationSection from "../features/DeclarationSection";

const Main = () => {
    return (
        <main>
            <div className="form">
                <ProyectSection />
                <TaskSection />
                <DeclarationSection />
            </div>
        </main>
    )
}

export default Main