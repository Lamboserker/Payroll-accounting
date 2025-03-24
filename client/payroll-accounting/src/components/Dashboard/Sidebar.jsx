// Sidebar.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Sidebar({ setSelectedFile }) {
    const [documents, setDocuments] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
        } else {
            fetch("http://localhost:8000/protected/documents", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    setDocuments(data);
                })
                .catch((err) => {
                    setError("Fehler beim Laden der Dokumente");
                });
        }
    }, [navigate]);

    const handleFileSelect = (file) => {
        setSelectedFile(file); // Aktualisiert die ausgewählte Datei
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="min-h-screen bg-gray-800 text-white w-64 p-4">
            <h2 className="text-xl font-semibold mb-4">Sidebar</h2>
            <button
                onClick={handleLogout}
                className="w-full p-2 bg-red-500 rounded mb-4"
            >
                Logout
            </button>
            <h3 className="text-lg mb-2">Dokumente</h3>
            {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
            <ul>
                {documents.map((doc) => (
                    <li
                        key={doc._id}
                        onClick={() => handleFileSelect(doc)}
                        className="cursor-pointer p-2 hover:bg-gray-600 rounded mb-2"
                    >
                        {doc.title}
                    </li>
                ))}
            </ul>
        </div>
    );
}
