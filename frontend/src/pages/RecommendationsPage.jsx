import React, { useState, useRef, useEffect } from 'react';
import ChatInput from '../components/Recommendations/ChatInput.jsx';
import ChatMessage from '../components/Recommendations/ChatMessage.jsx';
import { Sparkles } from 'lucide-react';

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

const RecommendationsPage = () => {
    const [messages, setMessages] = useState([
        { type: 'bot', content: "Hello! Describe the furniture you're looking for, and I'll find the best matches for you." }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const chatContainerRef = useRef(null);

    // Effect to auto-scroll to the latest message
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSendMessage = async (query) => {
        if (!query.trim() || isLoading) return;

        // Add user message to the chat
        const userMessage = { type: 'user', content: query };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: query }),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Failed to fetch recommendations");
            }

            const data = await response.json();

            if (data.length === 0) {
                const botMessage = { type: 'bot', content: "I couldn't find any products matching that description. Please try being more specific or use different keywords." };
                setMessages(prev => [...prev, botMessage]);
            } else {
                // Add bot response with product data
                const botMessage = { type: 'bot', products: data };
                setMessages(prev => [...prev, botMessage]);
            }

        } catch (err) {
            const errorMessage = { type: 'bot', content: `Sorry, an error occurred: ${err.message}` };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-10rem)] bg-white border border-gray-200 rounded-lg shadow-md">
            <div className="flex-1 overflow-y-auto p-6 space-y-6" ref={chatContainerRef}>
                {messages.map((msg, index) => (
                    <ChatMessage key={index} message={msg} />
                ))}
                {isLoading && (
                    <div className="flex justify-center">
                         <div className="inline-flex items-center gap-2 rounded-full bg-gray-100 px-4 py-2">
                           <Sparkles className="h-4 w-4 text-blue-600 animate-pulse" />
                           <span className="text-sm font-medium text-gray-700">AI is thinking...</span>
                         </div>
                    </div>
                )}
            </div>
            <div className="p-4 border-t border-gray-200 bg-gray-50">
                <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
        </div>
    );
};

export default RecommendationsPage;

