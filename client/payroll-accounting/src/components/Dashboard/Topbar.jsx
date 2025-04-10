import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { HiBars3 } from "react-icons/hi2";
import { CiBellOn } from "react-icons/ci";
import { FaXmark } from "react-icons/fa6";
const navigation = [
    { name: 'Dashboard', href: '/dashboard', current: true },
    { name: 'Gehaltsabrechnungen', href: '#', current: false },
    { name: 'Steuer-Unterlagen', href: '#', current: false },

]

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export default function Topbar() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        const allowedRoutes = ["/register"]; // Routen, die ohne Token erlaubt sind

        if (!token && !allowedRoutes.includes(window.location.pathname)) {
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




    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    }


    return (
        <Disclosure as="nav" className="bg-gray-800 ">
            <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 z-50">
                <div className="relative flex h-16 items-center justify-between">
                    <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                        {/* Mobile menu button*/}
                        <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset">
                            <span className="absolute -inset-0.5" />
                            <span className="sr-only">Hauptmenü öffnen</span>
                            <HiBars3 aria-hidden="true" className="block size-6 group-data-open:hidden" />
                            <FaXmark aria-hidden="true" className="hidden size-6 group-data-open:block" />
                        </DisclosureButton>
                    </div>
                    <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                        <div className="flex shrink-0 items-center">
                        </div>
                        <div className="hidden sm:ml-6 sm:block">
                            <div className="flex space-x-4">
                                {navigation.map((item) => (
                                    <a
                                        key={item.name}
                                        href={item.href}
                                        aria-current={item.current ? 'page' : undefined}
                                        className={classNames(
                                            item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                                            'rounded-md px-3 py-2 text-sm font-medium',
                                        )}
                                    >
                                        {item.name}
                                    </a>
                                ))}
                            </div>
                        </div>
                    </div>
                    <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                        <button
                            type="button"
                            className="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800 focus:outline-hidden"
                        >
                            <span className="absolute -inset-1.5" />
                            <span className="sr-only">Benachrichtungen sehen</span>
                            <CiBellOn aria-hidden="true" className="size-6" />
                        </button>

                        {/* Profile dropdown */}
                        <Menu as="div" className="relative ml-3">
                            <div>
                                <MenuButton className="relative flex items-center space-x-3 rounded-full bg-gray-800 px-3 py-2 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                                    <span className="absolute -inset-1.5" />
                                    <span className="sr-only">Nutzer-Menü öffnen</span>
                                    <img
                                        src="https://cdn-icons-png.flaticon.com/128/3177/3177440.png"
                                        alt="Avatar"
                                        className="w-10 h-10 rounded-full"
                                    />
                                    <span className="text-lg font-semibold text-white">
                                        {user ? user.full_name : "Lädt..."}
                                    </span>
                                </MenuButton>


                            </div>
                            <MenuItems
                                transition
                                className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 ring-1 shadow-lg ring-black/5 transition focus:outline-hidden data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in"
                            >
                                <MenuItem>
                                    <a
                                        href="/profilesettings"
                                        className="block px-4 py-2 text-sm text-gray-700 data-focus:bg-gray-100 data-focus:outline-hidden"
                                    >
                                        Mein Profil
                                    </a>
                                </MenuItem>
                                <MenuItem>
                                    <a
                                        href="#"
                                        className="block px-4 py-2 text-sm text-gray-700 data-focus:bg-gray-100 data-focus:outline-hidden"
                                    >
                                        Einstellungen
                                    </a>
                                </MenuItem>
                                <MenuItem>
                                    <a
                                        onClick={handleLogout}
                                        href="#"
                                        className="block px-4 py-2 text-sm text-gray-700 data-focus:bg-gray-100 data-focus:outline-hidden"
                                    >
                                        Abmelden
                                    </a>
                                </MenuItem>
                            </MenuItems>
                        </Menu>
                    </div>
                </div>
            </div>

            <DisclosurePanel className="sm:hidden">
                <div className="space-y-1 px-2 pt-2 pb-3">
                    {navigation.map((item) => (
                        <DisclosureButton
                            key={item.name}
                            as="a"
                            href={item.href}
                            aria-current={item.current ? 'page' : undefined}
                            className={classNames(
                                item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                                'block rounded-md px-3 py-2 text-base font-medium',
                            )}
                        >
                            {item.name}
                        </DisclosureButton>
                    ))}
                </div>
            </DisclosurePanel>
        </Disclosure>
    )
}