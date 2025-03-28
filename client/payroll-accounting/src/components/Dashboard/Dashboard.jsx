import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import { products } from "./data";
import ErrorBoundary from "../../../../payroll-accounting/Error-Boundary/SidebarBoundary";
import { format } from 'date-fns';
import { Skeleton } from '@mui/material'; // MUI Skeleton für Ladeanzeige
import pdfIcon from "../../assets/pdf.png";
// Hilfsfunktion zur Generierung eines zufälligen Datums
const getRandomDate = (start, end) => {
    const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    return date;
};

// Hilfsfunktion zur Generierung eines zufälligen Namens
const getRandomName = () => {
    const names = ['Bericht', 'Rechnung', 'Vertrag', 'Angebot', 'Buchung', 'Notiz', 'Dokument'];
    const randomIndex = Math.floor(Math.random() * names.length);
    return `${names[randomIndex]}-${Math.floor(Math.random() * 1000)}`;
};

export default function Dashboard() {
    const [sidebarWidth, setSidebarWidth] = useState(256);
    const [documents, setDocuments] = useState([]);
    const [filteredDocuments, setFilteredDocuments] = useState([]);
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [isLoading, setIsLoading] = useState(true); // Ladezustand für Skeletons


    // useEffect(() => {
    //     fetch("http://localhost:8000/documents")
    //         .then((response) => response.json())
    //         .then((data) => setDocuments(data))
    //         .catch((error) => console.error("Fehler beim Laden der Dokumente:", error));
    // }, []);


    useEffect(() => {
        const documentsArray = [];
        const startDate = new Date('2023-01-01');
        const endDate = new Date();

        // Erstelle mehrere Dokumente
        for (let i = 0; i < 50; i++) {
            const randomDate = getRandomDate(startDate, endDate);
            documentsArray.push({
                title: getRandomName(),
                createdAt: randomDate,
                fileURL: `https://via.placeholder.com/300x200?text=PDF${i + 1}`,
                imageURL: "https://via.placeholder.com/150x150?text=PDF",
            });
        }

        // Simuliere Ladezeit
        setTimeout(() => {
            setDocuments(documentsArray);
            setIsLoading(false);
        }, 2000); // 2 Sekunden Ladezeit simuliert
    }, []);

    // Filter documents based on the date range
    useEffect(() => {
        if (startDate && endDate) {
            const filtered = documents.filter((doc) => {
                const docDate = new Date(doc.createdAt);
                return docDate >= startDate && docDate <= endDate;
            });
            setFilteredDocuments(filtered);
        } else {
            setFilteredDocuments(documents); // No filter, show all documents
        }
    }, [startDate, endDate, documents]);


    return (
        <>

            <div className="flex min-h-screen bg-schutzschild pt-16">
                {/* Sidebar */}
                <ErrorBoundary>
                    <Sidebar
                        sidebarWidth={sidebarWidth}
                        setSidebarWidth={setSidebarWidth}
                        setStartDate={setStartDate}
                        setEndDate={setEndDate}
                    />
                </ErrorBoundary>

                {/* Main Content */}
                <div
                    className="flex-1 transition-all duration-300"
                    style={{ marginLeft: `${sidebarWidth}px`, transition: 'margin-left 0.3s ease' }}
                >
                    <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
                        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Dokumentenvorschau</h2>

                        <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
                            {isLoading ? (
                                // Skeletons während des Ladens anzeigen
                                Array.from({ length: 13 }).map((_, index) => (
                                    <div key={index} className="group relative bg-white rounded-lg shadow-md overflow-hidden">
                                        <div className="flex flex-col items-center p-4">
                                            <Skeleton variant="rectangular" width={200} height={150} />
                                            <div className="mt-4 text-center">
                                                <Skeleton width="60%" />
                                                <Skeleton width="40%" />
                                            </div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                // Dokumente anzeigen, wenn sie geladen wurden
                                filteredDocuments.map((doc, index) => (
                                    <div key={index} className="group relative bg-white rounded-lg shadow-md overflow-hidden">
                                        <div className="flex flex-col items-center p-4">
                                            <div className="bg-gray-200 w-full h-32 flex items-center justify-center">
                                                <img
                                                    src={pdfIcon}
                                                    alt={doc.title}
                                                    className="w-16 h-16 object-cover"
                                                />
                                            </div>
                                            <div className="mt-4 text-center">
                                                <h3 className="text-sm text-gray-700">{doc.title}</h3>
                                                <p className="text-xs text-gray-400">{format(new Date(doc.createdAt), 'dd.MM.yyyy')}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
