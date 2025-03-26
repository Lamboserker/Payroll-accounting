import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SchutzschildLogo from "../../../assets/Slogo.jpg";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState(""); // Neues Feld für Bestätigung des Passworts
    const [fullName, setFullName] = useState("");
    const [role, setRole] = useState("user");
    const [error, setError] = useState("");
    const [passwordMismatchError, setPasswordMismatchError] = useState(""); // Fehler für nicht übereinstimmende Passwörter
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Passwortabgleich
        if (password !== confirmPassword) {
            setPasswordMismatchError("Die Passwörter stimmen nicht überein");
            return;
        } else {
            setPasswordMismatchError(""); // Fehler zurücksetzen, falls die Passwörter übereinstimmen
        }

        try {
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password, full_name: fullName, role }),
            });
            const data = await response.json();
            if (response.ok) {
                navigate("/login");
            } else {
                setError(data.detail);
            }
        } catch (err) {
            setError("Fehler bei der Registrierung");
        }
    };

    return (

        <div className="flex min-h-screen items-center justify-center bg-gray-100 bg-schutzschild">
            <div className="sm:mx-auto sm:w-full sm:max-w-sm bg-cyan-950 p-8 rounded shadow-lg">
                <div className="text-center">
                    <img
                        alt="Your Company"
                        src={SchutzschildLogo}
                        className="mx-auto h-10 w-auto"
                    />
                    <h2 className="mt-10 text-2xl font-bold text-white">
                        Registriere dich für dein SCHUTZschild-Konto
                    </h2>
                </div>

                <div className="mt-10">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label htmlFor="fullName" className="block text-sm font-medium text-white">
                                Vollständiger Name
                            </label>
                            <div className="mt-2">
                                <input
                                    id="fullName"
                                    name="fullName"
                                    type="text"
                                    required
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-white">
                                Email Adresse
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    required
                                    autoComplete="email"
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-white">
                                Passwort
                            </label>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    autoComplete="current-password"
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium text-white">
                                Passwort bestätigen
                            </label>
                            <div className="mt-2">
                                <input
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    type="password"
                                    required
                                    autoComplete="current-password"
                                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600 sm:text-sm"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                />
                            </div>
                        </div>

                        {/* Fehleranzeige für nicht übereinstimmende Passwörter */}
                        {passwordMismatchError && (
                            <div className="text-red-500 text-sm">{passwordMismatchError}</div>
                        )}

                        {error && <div className="text-red-500 text-sm">{error}</div>}

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-indigo-600"
                            >
                                Registrieren
                            </button>
                        </div>
                    </form>

                    <p className="mt-10 text-center text-sm text-gray-500">
                        Bereits ein Konto?{' '}
                        <a href="/login" className="font-semibold text-indigo-600 hover:text-indigo-500">
                            Melde dich hier an!
                        </a>
                    </p>
                </div>
            </div>
        </div>

    );
}
