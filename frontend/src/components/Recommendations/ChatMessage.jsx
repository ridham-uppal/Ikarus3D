import React from 'react';
import ProductCard from './ProductCard';

const ChatMessage = ({ message }) => {
    const isUser = message.type === 'user';

    if (isUser) {
        return (
            <div className="flex justify-end">
                <div className="bg-blue-600 text-white rounded-lg p-3 max-w-lg">
                    <p>{message.content}</p>
                </div>
            </div>
        );
    }

    // Bot message
    return (
        <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 rounded-lg p-3 max-w-full">
                {/* If the message has product data, render product cards */}
                {message.products ? (
                    <div>
                        <p className="mb-4 font-semibold">Here are some recommendations I found for you:</p>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {message.products.map(product => (
                                // FIX: Pass the entire product object as a single 'recommendation' prop
                                // to match what the ProductCard component expects.
                                <ProductCard 
                                    key={product.uniq_id}
                                    recommendation={product}
                                />
                            ))}
                        </div>
                    </div>
                ) : (
                    // Otherwise, render simple text content
                    <p>{message.content}</p>
                )}
            </div>
        </div>
    );
};

export default ChatMessage;

