import React from "react";
import { useNavigate } from "react-router-dom";
import NotFoundImage from "../../assets/2526919.png"; // Stelle sicher, dass das Bild im richtigen Ordner liegt
import "./notfound.css"; // Importiere die CSS-Datei
// import cursorImage from "../../assets/cursor.png"; // Stelle sicher, dass das Bild im richtigen Ordner liegt

const NotFound = () => {
    const navigate = useNavigate();

    // Funktion für den Klick auf das Bild, die zum Login weiterleitet
    const handleClick = () => {
        navigate("/login");
    };

    return (
        <div className="flex justify-center items-center h-screen maindiv">
            <div className="flex justify-center items-center h-screen">
                <img
                    className="not-found-img"
                    src={NotFoundImage} // Bildquelle
                    alt="404"
                    onClick={handleClick} // Klick zum Weiterleiten
                />
            </div>
        </div>
    );
};

export default NotFound;
