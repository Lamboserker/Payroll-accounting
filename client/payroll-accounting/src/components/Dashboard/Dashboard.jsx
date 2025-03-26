import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import { products } from "./data";
import ErrorBoundary from "../../../../payroll-accounting/Error-Boundary/SidebarBoundary";
import Topbar from "./Topbar";

export default function Dashboard() {
    const [sidebarWidth, setSidebarWidth] = useState(256);

    return (
        <>
            {/* Topbar - always on top */}
            <div className="fixed top-0 left-0 w-full z-50">
                <Topbar />
            </div>
            <div className="flex min-h-screen bg-schutzschild pt-16">
                {/* Sidebar */}
                <ErrorBoundary>
                    <Sidebar sidebarWidth={sidebarWidth} setSidebarWidth={setSidebarWidth} />
                </ErrorBoundary>

                {/* Main Content */}
                <div
                    className="flex-1 transition-all duration-300"
                    style={{ marginLeft: `${sidebarWidth}px`, transition: 'margin-left 0.3s ease' }}>
                    <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
                        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Customers also purchased</h2>

                        <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
                            {products.map((product) => (
                                <div key={product.id} className="group relative">
                                    <img
                                        alt={product.imageAlt}
                                        src={product.imageSrc}
                                        className="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 lg:aspect-auto lg:h-80"
                                    />
                                    <div className="mt-4 flex justify-between">
                                        <div>
                                            <h3 className="text-sm text-gray-700">
                                                <a href={product.href}>
                                                    <span aria-hidden="true" className="absolute inset-0" />
                                                    {product.name}
                                                </a>
                                            </h3>
                                            <p className="mt-1 text-sm text-gray-500">{product.color}</p>
                                        </div>
                                        <p className="text-sm font-medium text-gray-900">{product.price}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div >
        </>
    );
}
