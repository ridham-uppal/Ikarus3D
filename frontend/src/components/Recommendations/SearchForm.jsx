import React, { useState } from 'react';

const SearchForm = ({ setQuery, isLoading }) => {
    const [inputValue, setInputValue] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim() && !isLoading) {
            setQuery(inputValue.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="mb-8">
            <div className="relative">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Describe the furniture you're looking for..."
                    className="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    className="absolute inset-y-0 right-0 flex items-center px-4 font-semibold text-white bg-blue-600 rounded-r-lg hover:bg-blue-700 disabled:bg-blue-300 transition"
                    disabled={isLoading}
                >
                    Search
                </button>
            </div>
        </form>
    );
};

export default SearchForm;
