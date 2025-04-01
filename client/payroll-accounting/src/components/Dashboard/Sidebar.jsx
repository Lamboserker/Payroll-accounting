import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { CiLogout } from "react-icons/ci";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import "dayjs/locale/de"; // Deutsche Lokalisierung für dayjs
import { FcStart } from "react-icons/fc";
import { GiFinishLine } from "react-icons/gi";


export default function Sidebar({ sidebarWidth, setSidebarWidth }) {
    const [user, setUser] = useState(null);
    // const [documents, setDocuments] = useState([]);
    const [error, setError] = useState("");
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const navigate = useNavigate();

    // Maximalbreite der Sidebar
    const MAX_SIDEBAR_WIDTH = 400;


    useEffect(() => {
        console.log("Start- und Enddatum in Sidebar:", startDate, endDate);
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        let isMounted = true;

        fetch("http://localhost:8000/auth/me", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (isMounted) {
                    setUser(data);
                    console.log("Benutzer geladen:", data);
                }
            })
            .catch(() => {
                if (isMounted) {
                    setError("Fehler beim Laden des Benutzers");
                }
            });

        return () => {
            isMounted = false;
        };
    }, [navigate]);

    // Date Range Change Handler
    const handleDateChange = (newStartDate, newEndDate) => {
        console.log("Start- und Enddatum geändert:", newStartDate, newEndDate);
        setStartDate(newStartDate);
        setEndDate(newEndDate);
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const handleMouseDown = (e) => {
        document.body.style.userSelect = "none";

        const startX = e.clientX;
        const startWidth = sidebarWidth;

        const handleMouseMove = (moveEvent) => {
            const diff = moveEvent.clientX - startX;
            setSidebarWidth(Math.min(Math.max(200, startWidth + diff), MAX_SIDEBAR_WIDTH));
        };

        const handleMouseUp = () => {
            document.body.style.userSelect = "";
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("mouseup", handleMouseUp);
        };

        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseup", handleMouseUp);
    };

    return (
        <div
            id="sidebar"
            className="min-h-screen bg-gray-800 text-white p-4 fixed top-0 left-0 h-full overflow-y-auto z-40"
            style={{ width: `${sidebarWidth}px` }}
        >
            {/* Sidebar Content */}
            <div className="flex items-center space-x-3 mb-4">
                <img
                    src="https://cdn-icons-png.flaticon.com/128/3177/3177440.png"
                    alt="Avatar"
                    className="w-10 h-10 rounded-full"
                />
                <span className="text-lg font-semibold">
                    {user ? user.full_name : "Lädt..."}
                </span>
            </div>

            {/* Date Range Pickers */}
            <div className="mb-4">
                <h3 className="text-lg mb-2">Zeitraum wählen</h3>
                <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="de">
                    <div className="flex flex-col gap-4 mb-4">
                        {/* Start Date Picker */}
                        <DatePicker
                            views={['year', 'month', 'day']}
                            label="Startdatum"
                            value={startDate}
                            onChange={(newValue) => setStartDate(newValue)}
                            slots={{ openPickerIcon: FcStart }}
                            sx={{
                                "& .MuiInputBase-root": {
                                    backgroundColor: "#222", // Dunkler Hintergrund
                                    color: "white",
                                },
                                "& .MuiFormLabel-root": {
                                    color: "white",
                                    mixBlendMode: "difference", // Sorgt für automatische Anpassung
                                    "&.Mui-focused": {
                                        color: "white",
                                    },
                                },
                            }}
                            slotProps={{
                                textField: {
                                    InputProps: {
                                        sx: {
                                            color: "white",
                                            backgroundColor: "#222",
                                            "& input": {
                                                color: "white",
                                            },
                                        },
                                    },
                                },
                            }}
                        />

                        {/* End Date Picker */}
                        <DatePicker
                            views={['year', 'month', 'day']}
                            label="Enddatum"
                            value={endDate}
                            onChange={(newValue) => handleDateChange(newValue, endDate)}
                            slots={{ openPickerIcon: GiFinishLine }}
                            sx={{
                                "& .MuiInputBase-root": {
                                    backgroundColor: "#222", // Dunkler Hintergrund
                                    color: "white",
                                },
                                "& .MuiFormLabel-root": {
                                    color: "white",
                                    mixBlendMode: "difference",
                                    "&.Mui-focused": {
                                        color: "white",
                                    },
                                },
                                "& .MuiSvgIcon-root": {
                                    color: "white", // Weißes Icon
                                },
                            }}
                            slotProps={{
                                textField: {
                                    InputProps: {
                                        sx: {
                                            color: "white",
                                            backgroundColor: "#222",
                                            "& input": {
                                                color: "white",
                                            },
                                        },
                                    },
                                },
                                // Hier setzen wir die Farbe des Icons explizit
                                openPickerIcon: {
                                    color: "white",
                                },
                            }}
                        />
                    </div>
                </LocalizationProvider>
            </div>

            {/* Dokumentenliste */}
            <div className="overflow-auto flex-1">
                <h3 className="text-lg mb-2">Dokumente</h3>
                <p className="text-sm mb-2">Wählen Sie ein Dokument aus, um es anzuzeigen.</p>
                <p className="text-sm mb-2">Aktuelle Auswahl: {startDate ? startDate.format("DD.MM.YYYY") : "Kein Startdatum"} - {endDate ? endDate.format("DD.MM.YYYY") : "Kein Enddatum"}</p>
                {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
                {/* <ul>
                    {documents.map((doc) => (
                        <li key={doc._id} className="cursor-pointer p-2  rounded mb-2">
                            {doc.title}
                        </li>
                    ))}
                </ul> */}
            </div>

            {/* Resizable handle */}
            <div
                onMouseDown={handleMouseDown}
                className="absolute top-0 right-0 h-full w-2 bg-gray-600 cursor-ew-resize z-50"
            />

            {/* Logout-Icon */}
            <div
                onClick={handleLogout}
                className="absolute bottom-4 right-4 p-3 bg-gray-700 rounded-full cursor-pointer hover:bg-red-500"
            >
                <CiLogout size={30} className="text-white" />
            </div>
        </div>
    );
}
