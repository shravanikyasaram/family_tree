import React, { useState } from "react";
import AncestorForm from "./components/AncestorForm.jsx"
import LastNameForm from "./components/LastNameForm";

function App() {
    const [lastName, setLastName] = useState("");

    const handleLastNameSubmit = (name) => {
        setLastName(name);
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
            {lastName ? (
                <>
                    <h1>Welcome to {lastName.toUpperCase()}'s Family Tree</h1>
                    <AncestorForm />
                </>
            ) : (
                <LastNameForm onSubmit={handleLastNameSubmit} />
            )}
        </div>
    );
}

export default App;
