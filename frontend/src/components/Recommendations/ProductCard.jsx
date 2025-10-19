import React from 'react';

// FIX: This component now accepts a single 'recommendation' prop
const ProductCard = ({ recommendation }) => {
    
    // Destructure with default values to prevent errors if a field is missing
    const { details = {}, creative_description = "No description available." } = recommendation || {};

    const parseImages = (imagesStr) => {
        if (!imagesStr || typeof imagesStr !== 'string') return null;
        try {
            const cleanedStr = imagesStr.replace(/'/g, '"');
            const images = JSON.parse(cleanedStr);
            return Array.isArray(images) && images.length > 0 ? images[0].trim() : null;
        } catch (error) {
            return null;
        }
    };

    const imageUrl = parseImages(details.images);

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 flex flex-col border border-gray-100">
            <div className="h-48 bg-gray-200 flex items-center justify-center">
                {imageUrl ? (
                    <img src={imageUrl} alt={details.title} className="w-full h-full object-cover" />
                ) : (
                    <span className="text-gray-500">No Image</span>
                )}
            </div>
            <div className="p-4 flex flex-col flex-grow">
                <h3 className="text-md font-bold text-gray-800 truncate" title={details.title}>
                    {details.title || "Untitled Product"}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                    {details.brand || "Unknown Brand"}
                </p>
                <p className="text-lg font-semibold text-blue-600 my-2">
                    {details.price || "Price not available"}
                </p>
                
                <div className="mt-auto pt-3 border-t border-gray-100">
                    <h4 className="font-semibold text-gray-700 text-sm">Creative Description:</h4>
                    <p className="text-gray-600 text-sm mt-1 italic">"{creative_description}"</p>
                </div>
            </div>
        </div>
    );
};

export default ProductCard;

