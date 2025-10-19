import React from 'react';

const Header = ({ activePage, setActivePage }) => (
    <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 sm:px-6 lg:p-8">
            <div className="flex items-center justify-between h-16">
                <div className="flex items-center">
                    <svg className="h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span className="ml-3 text-2xl font-bold text-gray-800">AI Furniture</span>
                </div>
                <nav className="flex space-x-4">
                    <button
                        onClick={() => setActivePage('recommendations')}
                        className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'recommendations' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
                    >
                        Recommendations
                    </button>
                    <button
                        onClick={() => setActivePage('analytics')}
                        className={`px-3 py-2 rounded-md text-sm font-medium ${activePage === 'analytics' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
                    >
                        Analytics
                    </button>
                </nav>
            </div>
        </div>
    </header>
);

export default Header;
