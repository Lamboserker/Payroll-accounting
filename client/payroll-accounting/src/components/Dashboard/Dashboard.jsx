// import { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";

// export default function Dashboard() {
//     const [documents, setDocuments] = useState([]);
//     const [error, setError] = useState("");
//     const navigate = useNavigate();

//     useEffect(() => {
//         const token = localStorage.getItem("token");
//         if (!token) {
//             navigate("/login");
//         } else {
//             fetch("http://localhost:8000/protected/documents", {
//                 method: "GET",
//                 headers: {
//                     Authorization: `Bearer ${token}`,
//                 },
//             })
//                 .then((response) => response.json())
//                 .then((data) => {
//                     setDocuments(data);
//                 })
//                 .catch((err) => {
//                     setError("Fehler beim Laden der Dokumente");
//                 });
//         }
//     }, [navigate]);

//     return (
//         <div className="min-h-screen bg-gray-100">
//             <div className="max-w-4xl mx-auto p-6">
//                 <h2 className="text-3xl font-semibold mb-6">Deine Dokumente</h2>
//                 {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
//                 <ul>
//                     {documents.map((doc) => (
//                         <li key={doc._id} className="mb-4">
//                             <div className="bg-white p-4 rounded-md shadow-md">
//                                 <h3 className="text-xl font-semibold">{doc.title}</h3>
//                                 <p>{doc.date}</p>
//                                 <a
//                                     href={`http://localhost:8000/pdf/${doc._id}`}
//                                     className="text-blue-500"
//                                     target="_blank"
//                                     rel="noopener noreferrer"
//                                 >
//                                     PDF anzeigen
//                                 </a>
//                             </div>
//                         </li>
//                     ))}
//                 </ul>
//             </div>
//         </div>
//     );
// }


// import { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";

// export default function Dashboard() {
//     const [documents, setDocuments] = useState([]);
//     const [error, setError] = useState("");
//     const navigate = useNavigate();

//     useEffect(() => {
//         const token = localStorage.getItem("token");
//         if (!token) {
//             navigate("/login");
//         } else {
//             // Beispiel: Dummy-API mit Test-PDFs
//             fetch("https://jsonplaceholder.typicode.com/posts")
//                 .then((response) => response.json())
//                 .then((data) => {
//                     // Simuliere PDF-Daten
//                     const fakeDocs = data.slice(0, 5).map((item) => ({
//                         _id: item.id,
//                         title: item.title,
//                         date: new Date().toLocaleDateString(),
//                         url: `https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf`
//                     }));
//                     setDocuments(fakeDocs);
//                 })
//                 .catch(() => {
//                     setError("Fehler beim Laden der Dokumente");
//                 });
//         }
//     }, [navigate]);

//     return (
//         <div className="min-h-screen bg-gray-100">
//             <div className="max-w-4xl mx-auto p-6">
//                 <h2 className="text-3xl font-semibold mb-6">Deine Dokumente</h2>
//                 {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
//                 <ul>
//                     {documents.map((doc) => (
//                         <li key={doc._id} className="mb-4">
//                             <div className="bg-white p-4 rounded-md shadow-md">
//                                 <h3 className="text-xl font-semibold">{doc.title}</h3>
//                                 <p>{doc.date}</p>
//                                 <a
//                                     href={doc.url}
//                                     className="text-blue-500"
//                                     target="_blank"
//                                     rel="noopener noreferrer"
//                                 >
//                                     PDF anzeigen
//                                 </a>
//                             </div>
//                         </li>
//                     ))}
//                 </ul>
//             </div>
//         </div>
//     );
// }

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";

// const [selectedFile, setSelectedFile] = useState(null);
const products = [
    {
        id: 1,
        name: 'Basic Tee',
        href: '#',
        imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
        imageAlt: "Front of men's Basic Tee in black.",
        price: '$35',
        color: 'Black',
    },
    {
        id: 2,
        name: 'Basic Tee',
        href: '#',
        imageSrc: 'https://tailwindcss.com/plus-assets/img/ecommerce-images/product-page-01-related-product-02.jpg',
        imageAlt: "Front of Basic Tee in gray.",
        price: '$35',
        color: 'Gray',
    },
    {
        id: 3,
        name: 'Slim Fit Jeans',
        href: '#',
        imageSrc: 'https://plus.unsplash.com/premium_photo-1718913936342-eaafff98834b?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3Dhttps://via.placeholder.com/150x150?text=Slim+Fit+Jeans',
        imageAlt: "Slim fit jeans in dark blue.",
        price: '$50',
        color: 'Dark Blue',
    },
    {
        id: 4,
        name: 'Denim Jacket',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Denim jacket in light wash.",
        price: '$60',
        color: 'Light Wash',
    },
    {
        id: 5,
        name: 'Graphic Hoodie',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Front of a graphic hoodie in black.",
        price: '$45',
        color: 'Black',
    },
    {
        id: 6,
        name: 'Sporty Joggers',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Sporty joggers in grey.",
        price: '$40',
        color: 'Grey',
    },
    {
        id: 7,
        name: 'Leather Boots',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1622470953794-aa9c70b0fb9d?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Leather boots in brown.",
        price: '$120',
        color: 'Brown',
    },
    {
        id: 8,
        name: 'V-neck T-shirt',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1616006897093-5e4635c0de35?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "V-neck T-shirt in navy.",
        price: '$30',
        color: 'Navy',
    },
    {
        id: 9,
        name: 'Chino Shorts',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1613852348851-df1739db8201?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Chino shorts in beige.",
        price: '$35',
        color: 'Beige',
    },
    {
        id: 10,
        name: 'Plaid Shirt',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1622351772377-c3dda74beb03?q=80&w=2148&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Plaid shirt in red and black.",
        price: '$40',
        color: 'Red/Black',
    },
    {
        id: 11,
        name: 'Puffer Jacket',
        href: '#',
        imageSrc: 'https://plus.unsplash.com/premium_photo-1661373644394-ebc6f569826c?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Puffer jacket in olive green.",
        price: '$80',
        color: 'Olive Green',
    },
    {
        id: 12,
        name: 'Canvas Sneakers',
        href: '#',
        imageSrc: 'https://images.unsplash.com/photo-1618453292459-53424b66bb6a?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        imageAlt: "Canvas sneakers in white.",
        price: '$50',
        color: 'White',
    }

    // More products...
]

export default function Dashboard() {
    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:max-w-7xl lg:px-8">
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
    )
}