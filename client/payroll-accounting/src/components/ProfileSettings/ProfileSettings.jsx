import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import CancelRoundedIcon from '@mui/icons-material/CancelRounded';
import axios from 'axios';

const ProfileSettings = () => {
    const [user, setUser] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({
        full_name: "",
        email: "",
        password: "",
    });

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const token = localStorage.getItem("token"); // Beispiel, Token aus localStorage holen
                const response = await axios.get("http://localhost:8000/auth/me", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setUser(response.data);
                setFormData({
                    full_name: response.data.full_name,
                    email: response.data.email,
                    password: "",
                });
            } catch (error) {
                console.error("Error fetching user data:", error);
            }
        };

        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSave = async () => {
        try {
            const token = localStorage.getItem("token");
            await axios.put(
                "http://localhost:8000/profile",
                formData,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setUser(formData); // Userdaten im State aktualisieren
            setEditMode(false); // Bearbeitungsmodus beenden
        } catch (error) {
            console.error("Error updating user data:", error);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-100">
            <div className="w-full max-w-lg p-8 bg-white shadow-lg rounded-lg">
                <div className="text-center mb-12">
                    <div className="relative">
                        <div className="w-24 h-24 bg-indigo-100 mx-auto rounded-full shadow-2xl flex items-center justify-center text-indigo-500">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                            </svg>
                        </div>
                    </div>
                    <h2 className="text-2xl font-semibold mt-4 text-gray-700">Profil-Einstellungen</h2>
                </div>

                <div className="space-y-6">
                    {editMode ? (
                        <>
                            <TextField
                                label="Vollständiger Name"
                                type="text"
                                variant="outlined"
                                fullWidth
                                size="small"
                                name="full_name"
                                value={formData.full_name}
                                onChange={handleChange}
                                InputProps={{
                                    endAdornment: formData.full_name && (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="clear input"
                                                onClick={() => setFormData({ ...formData, full_name: "" })}
                                            >
                                                <CancelRoundedIcon />
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                }}
                                sx={{ mb: 2 }}  // MUI-Styling für den Abstand
                            />
                            <TextField
                                label="Email"
                                type="email"
                                variant="outlined"
                                fullWidth
                                size="small"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                InputProps={{
                                    endAdornment: formData.email && (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="clear input"
                                                onClick={() => setFormData({ ...formData, email: "" })}
                                            >
                                                <CancelRoundedIcon />
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                }}
                                sx={{ mb: 2 }}  // MUI-Styling für den Abstand
                            />
                        </>
                    ) : (
                        <>
                            <h3 className="text-xl font-medium text-gray-700">{formData.full_name || 'Full Name'}</h3>
                            <p className="font-light text-gray-600 mt-2">{formData.email || 'Email'}</p>
                        </>
                    )}
                </div>

                <div className="mt-8 text-center">
                    {editMode ? (
                        <button
                            className="text-indigo-500 py-2 px-6 font-medium mt-4 border rounded-md border-indigo-500 hover:bg-indigo-500 hover:text-white"
                            onClick={handleSave}
                        >
                            Einstellungen speichern
                        </button>
                    ) : (
                        <button
                            className="text-indigo-500 py-2 px-6 font-medium mt-4 border rounded-md border-indigo-500 hover:bg-indigo-500 hover:text-white"
                            onClick={() => setEditMode(true)}
                        >
                            Profil bearbeiten
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfileSettings;
