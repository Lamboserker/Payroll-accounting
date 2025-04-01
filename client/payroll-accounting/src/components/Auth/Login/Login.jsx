// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import "./Login.css";
// export default function Login() {
//     const [email, setEmail] = useState("");
//     const [password, setPassword] = useState("");
//     const navigate = useNavigate();
//     const [error, setError] = useState("");

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             const response = await fetch("http://localhost:8000/auth/login", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify({ email, password }),
//             });
//             const data = await response.json();
//             if (response.ok) {
//                 localStorage.setItem("token", data.access_token);
//                 navigate("/dashboard");
//             } else {
//                 setError(data.detail);
//             }
//         } catch (err) {
//             setError("Fehler bei der Anmeldung");
//         }
//     };

//     return (
//         <div className="flex items-center justify-center min-h-screen bg-gray-100 bg-schutzschild">
//             <div className="bg-white p-8 rounded shadow-lg w-80">
//                 <h2 className="text-2xl font-semibold mb-6">Login</h2>
//                 <form onSubmit={handleSubmit}>
//                     <div className="mb-4">
//                         <label className="block text-sm font-medium text-gray-700">E-Mail</label>
//                         <input
//                             type="email"
//                             className="w-full px-4 py-2 border rounded-md"
//                             value={email}
//                             onChange={(e) => setEmail(e.target.value)}
//                             required
//                         />
//                     </div>
//                     <div className="mb-6">
//                         <label className="block text-sm font-medium text-gray-700">Passwort</label>
//                         <input
//                             type="password"
//                             className="w-full px-4 py-2 border rounded-md"
//                             value={password}
//                             onChange={(e) => setPassword(e.target.value)}
//                             required
//                         />
//                     </div>
//                     {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
//                     <button
//                         type="submit"
//                         className="w-full bg-blue-500 text-white py-2 rounded-md"
//                     >
//                         Anmelden
//                     </button>
//                 </form>
//             </div>
//         </div>
//     );
// }
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import SchutzschildLogo from "../../../assets/Slogo.jpg";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const [error, setError] = useState("");

    const handleRegisterRedirect = () => {
        navigate("/register");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem("token", data.access_token);
                navigate("/dashboard");
            } else {
                setError(data.detail);
            }
        } catch (err) {
            setError("Fehler bei der Anmeldung");
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
                        Melde dich mit deinem SCHUTZschild-Konto an
                    </h2>
                </div>

                <div className="mt-10">
                    <form onSubmit={handleSubmit} className="space-y-6">
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

                        {error && <div className="text-red-500 text-sm">{error}</div>}

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-indigo-600"
                            >
                                Anmelden
                            </button>
                        </div>
                    </form>

                    <p className="mt-10 text-center text-sm text-gray-500">
                        Noch kein Konto?{' '}
                        <button onClick={handleRegisterRedirect} className="font-semibold text-indigo-600 hover:text-indigo-500">
                            Registriere dich
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}
