import { useState } from "react";

export default function Upload() {
    const [file, setFile] = useState(null);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8000/pdf/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setSuccess("Datei erfolgreich hochgeladen");
                setError("");
            } else {
                setError("Fehler beim Hochladen der Datei");
            }
        } catch (err) {
            setError("Fehler beim Hochladen der Datei");
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded shadow-lg w-80">
                <h2 className="text-2xl font-semibold mb-6">PDF hochladen</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        onChange={handleFileChange}
                        className="w-full mb-4 p-2 border rounded"
                        required
                    />
                    {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
                    {success && <div className="text-green-500 text-sm mb-4">{success}</div>}
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-md">
                        Hochladen
                    </button>
                </form>
            </div>
        </div>
    );
}
