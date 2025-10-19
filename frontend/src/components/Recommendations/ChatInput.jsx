import React, { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSendMessage, isLoading }) => {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim()) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Describe the furniture you want..."
                className="w-full px-4 py-2 text-base border-2 border-gray-300 rounded-full focus:ring-blue-500 focus:border-blue-500 transition"
                disabled={isLoading}
            />
            <button
                type="submit"
                className="p-3 text-white bg-blue-600 rounded-full hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
                disabled={isLoading || !inputValue.trim()}
            >
                <Send className="h-5 w-5" />
            </button>
        </form>
    );
};

export default ChatInput;
