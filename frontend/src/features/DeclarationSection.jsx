import "./DeclarationSection.css"
import { Cog } from 'lucide-react';

const DeclarationSection  = () => {

    return (
        <div className="container">
            <fieldset>
                <legend>Declaración generada</legend>
                <button
                    className="generator"
                    type="button"
                >
                    Generar <Cog />
                </button>
                <textarea id="output" readOnly></textarea>
            </fieldset>
        </div>
    )
};

export default DeclarationSection;