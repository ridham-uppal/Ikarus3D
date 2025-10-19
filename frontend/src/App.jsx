// import React, { useState, useEffect } from 'react';

// // --- Configuration ---
// const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// // --- Helper Components ---

// // Simple loading spinner component
// const Spinner = () => (
//     <div className="flex justify-center items-center p-4">
//         <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//     </div>
// );

// // Error message component
// const ErrorDisplay = ({ message }) => (
//     <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative my-4" role="alert">
//         <strong className="font-bold">Error: </strong>
//         <span className="block sm:inline">{message}</span>
//     </div>
// );

// // Header component with navigation
// const Header = ({ activePage, setActivePage }) => (
//     <header className="bg-white shadow-md">
//         <div className="container mx-auto px-4 sm:px-6 lg:px-8">
//             <div className="flex items-center justify-between h-16">
//                 <div className="flex items-center">
//                     <svg className="h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                         <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
//                     </svg>
//                     <span className="ml-3 text-2xl font-bold text-gray-800">AI Furniture</span>
//                 </div>
//                 <nav className="flex space-x-4">
//                     <button
//                         onClick={() => setActivePage('recommendations')}
//                         className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'recommendations' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
//                     >
//                         Recommendations
//                     </button>
//                     <button
//                         onClick={() => setActivePage('analytics')}
//                         className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'analytics' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
//                     >
//                         Analytics
//                     </button>
//                 </nav>
//             </div>
//         </div>
//     </header>
// );


// // --- Analytics Page Components ---

// const StatCard = ({ title, value }) => (
//     <div className="bg-white p-6 rounded-lg shadow-md text-center">
//         <h3 className="text-lg font-medium text-gray-500">{title}</h3>
//         <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
//     </div>
// );

// const BarChartCard = ({ title, data }) => {
//     const maxValue = Math.max(...Object.values(data));
//     return (
//         <div className="bg-white p-6 rounded-lg shadow-md col-span-1 md:col-span-2">
//             <h3 className="text-lg font-medium text-gray-700 mb-4">{title}</h3>
//             <div className="space-y-4">
//                 {Object.entries(data).map(([key, value]) => (
//                     <div key={key} className="flex items-center">
//                         <span className="text-sm font-medium text-gray-600 w-28 truncate">{key}</span>
//                         <div className="flex-1 bg-gray-200 rounded-full h-6 mx-4">
//                             <div
//                                 className="bg-blue-500 h-6 rounded-full text-xs font-medium text-blue-100 text-center p-0.5 leading-none"
//                                 style={{ width: `${(value / maxValue) * 100}%` }}
//                             >
//                                {value}
//                             </div>
//                         </div>
//                     </div>
//                 ))}
//             </div>
//         </div>
//     );
// };


// // --- Recommendations Page Components ---

// const SearchForm = ({ setQuery, isLoading }) => {
//     const [inputValue, setInputValue] = useState("");

//     const handleSubmit = (e) => {
//         e.preventDefault();
//         if (inputValue.trim() && !isLoading) {
//             setQuery(inputValue.trim());
//         }
//     };

//     return (
//         <form onSubmit={handleSubmit} className="mb-8">
//             <div className="relative">
//                 <input
//                     type="text"
//                     value={inputValue}
//                     onChange={(e) => setInputValue(e.target.value)}
//                     placeholder="Describe the furniture you're looking for..."
//                     className="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition"
//                     disabled={isLoading}
//                 />
//                 <button
//                     type="submit"
//                     className="absolute inset-y-0 right-0 flex items-center px-4 font-semibold text-white bg-blue-600 rounded-r-lg hover:bg-blue-700 disabled:bg-blue-300 transition"
//                     disabled={isLoading}
//                 >
//                     Search
//                 </button>
//             </div>
//         </form>
//     );
// };

// const ProductCard = ({ recommendation }) => {
//     // Safely parse the images string
//     const parseImages = (imagesStr) => {
//         try {
//             // The string looks like "['url1', 'url2']", so we need to clean it for JSON.parse
//             const cleanedStr = imagesStr.replace(/'/g, '"');
//             const images = JSON.parse(cleanedStr);
//             return Array.isArray(images) && images.length > 0 ? images[0].trim() : null;
//         } catch (error) {
//             console.error("Failed to parse images:", imagesStr, error);
//             return null;
//         }
//     };

//     const imageUrl = parseImages(recommendation.details.images);

//     return (
//         <div className="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300">
//             <div className="h-48 bg-gray-200 flex items-center justify-center">
//                 {imageUrl ? (
//                     <img src={imageUrl} alt={recommendation.details.title} className="w-full h-full object-cover" />
//                 ) : (
//                     <span className="text-gray-500">No Image</span>
//                 )}
//             </div>
//             <div className="p-6">
//                 <h3 className="text-lg font-bold text-gray-800 truncate" title={recommendation.details.title}>
//                     {recommendation.details.title}
//                 </h3>
//                 <p className="text-sm text-gray-500 mt-1">
//                     {recommendation.details.brand || "Unknown Brand"}
//                 </p>
//                 <p className="text-xl font-semibold text-blue-600 my-3">
//                     {recommendation.details.price || "Price not available"}
//                 </p>
                
//                 <div className="mt-4 p-4 bg-gray-50 rounded-lg">
//                     <h4 className="font-semibold text-gray-700">Creative Description:</h4>
//                     <p className="text-gray-600 text-sm mt-2">{recommendation.creative_description}</p>
//                 </div>
//             </div>
//         </div>
//     );
// };


// // --- Main Page Components ---

// const AnalyticsPage = () => {
//     const [analytics, setAnalytics] = useState(null);
//     const [error, setError] = useState(null);
//     const [isLoading, setIsLoading] = useState(true);

//     useEffect(() => {
//         const fetchAnalytics = async () => {
//             try {
//                 const response = await fetch(`${API_BASE_URL}/analytics`);
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! Status: ${response.status}`);
//                 }
//                 const data = await response.json();
//                 setAnalytics(data);
//             } catch (e) {
//                 setError(e.message);
//             } finally {
//                 setIsLoading(false);
//             }
//         };

//         fetchAnalytics();
//     }, []);

//     if (isLoading) return <Spinner />;
//     if (error) return <ErrorDisplay message={error} />;
//     if (!analytics) return <p>No analytics data available.</p>;

//     return (
//         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
//             <StatCard title="Total Products" value={analytics.total_products} />
//             <StatCard title="Average Price" value={`$${analytics.price_statistics.average}`} />
//             <div className="col-span-1 md:col-span-2">
//                  <BarChartCard title="Top 10 Brands" data={analytics.top_brands} />
//             </div>
//             <div className="col-span-1 md:col-span-2">
//                  <BarChartCard title="Top 10 Materials" data={analytics.top_materials} />
//             </div>
//             <div className="col-span-1 md:col-span-2">
//                  <BarChartCard title="Top 10 Countries" data={analytics.top_countries} />
//             </div>
//         </div>
//     );
// };

// const RecommendationsPage = () => {
//     const [query, setQuery] = useState("");
//     const [recommendations, setRecommendations] = useState([]);
//     const [error, setError] = useState(null);
//     const [isLoading, setIsLoading] = useState(false);

//     useEffect(() => {
//         if (!query) return;

//         const fetchRecommendations = async () => {
//             setIsLoading(true);
//             setError(null);
//             try {
//                 const response = await fetch(`${API_BASE_URL}/recommend`, {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({ text: query }),
//                 });

//                 if (!response.ok) {
//                     throw new Error(`Network response was not ok: ${response.statusText}`);
//                 }
//                 const data = await response.json();
//                 setRecommendations(data);
//             } catch (e) {
//                 setError(e.message);
//             } finally {
//                 setIsLoading(false);
//             }
//         };

//         fetchRecommendations();
//     }, [query]);

//     return (
//         <div>
//             <SearchForm setQuery={setQuery} isLoading={isLoading} />
//             {isLoading && <Spinner />}
//             {error && <ErrorDisplay message={error} />}
//             {!isLoading && !error && (
//                 <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
//                     {recommendations.map((rec) => (
//                         <ProductCard key={rec.uniq_id} recommendation={rec} />
//                     ))}
//                 </div>
//             )}
//             {!isLoading && query && recommendations.length === 0 && !error && (
//                 <div className="text-center py-10">
//                     <p className="text-gray-600">No recommendations found. Try a different search!</p>
//                 </div>
//             )}
//         </div>
//     );
// };


// // --- The Main App Component ---

// function App() {
//     const [activePage, setActivePage] = useState('recommendations'); // 'recommendations' or 'analytics'

//     return (
//         <div className="bg-gray-50 min-h-screen font-sans">
//             <Header activePage={activePage} setActivePage={setActivePage} />
//             <main className="container mx-auto p-4 sm:p-6 lg:p-8">
//                 {activePage === 'recommendations' ? <RecommendationsPage /> : <AnalyticsPage />}
//             </main>
//         </div>
//     );
// }

// export default App;
import React, { useState } from 'react';
import Header from './components/common/Header.jsx';
import RecommendationsPage from './pages/RecommendationsPage.jsx';
import AnalyticsPage from './pages/AnalyticsPage.jsx';

function App() {
    const [activePage, setActivePage] = useState('recommendations');

    return (
        <div className="bg-gray-50 min-h-screen font-sans">
            <Header activePage={activePage} setActivePage={setActivePage} />
            <main className="container mx-auto p-4 sm:p-6 lg:p-8">
                {activePage === 'recommendations' ? <RecommendationsPage /> : <AnalyticsPage />}
            </main>
        </div>
    );
}

export default App;

