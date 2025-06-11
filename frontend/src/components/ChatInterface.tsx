import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import apiService from '../services/api';
import './ChatInterface.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hi there! I can help you navigate. Where would you like to go?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check API health on component mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const isHealthy = await apiService.checkHealth();
        if (!isHealthy) {
          setError('The navigation service is currently unavailable. Please try again later.');
        }
      } catch (err) {
        setError('Unable to connect to the navigation service. Please check your internet connection.');
      }
    };
    
    checkApiHealth();
    
    // Clear error message after 5 seconds
    return () => {
      if (error) {
        const timer = setTimeout(() => setError(null), 5000);
        return () => clearTimeout(timer);
      }
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Clear any previous errors
    setError(null);
    
    // Create new user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input.trim(),
      sender: 'user',
      timestamp: new Date(),
    };
    
    // Add user message to state
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    
    // Clear input field
    setInput('');
    
    // Set loading state
    setIsLoading(true);
    
    try {
      // Convert messages to chat history format for API
      const chatHistory = messages
        .filter(msg => msg.id !== '1') // Filter out the initial welcome message
        .map(msg => ({
          type: msg.sender === 'user' ? 'human' : 'ai',
          content: msg.text,
        }));
      
      // Send query to API
      const response = await apiService.sendQuery(userMessage.text, chatHistory);
      
      // Add bot response to messages
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: (Date.now() + 1).toString(),
          text: response.response,
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);
    } catch (err: any) {
      // Handle errors
      const errorMessage = err.message || 'Something went wrong. Please try again.';
      setError(errorMessage);
      
      // Add error message as bot response
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: (Date.now() + 1).toString(),
          text: `Error: ${errorMessage}`,
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);
    } finally {
      // Clear loading state
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Navigation Assistant</h2>
      </div>
      
      {error && <div className="error-banner">{error}</div>}
      
      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className="message-content">
              <ReactMarkdown>{message.text}</ReactMarkdown>
            </div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content loading">
              <div className="loading-dots">
                <span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Where would you like to go?"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface; 