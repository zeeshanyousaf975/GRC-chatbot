import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './ChatInterface.css';
import NavLinks from './NavLinks';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi there! I can help you navigate. Where would you like to go?'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sources, setSources] = useState([]);
  const messagesEndRef = useRef(null);

  // Debug API URL
  useEffect(() => {
    console.log("API URL:", process.env.REACT_APP_API_URL || 'http://localhost:8000');
  }, []);

  // Function to scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle user input
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Don't send empty messages
    if (!inputValue.trim()) return;

    // Add user message to state
    const userMessage = {
      role: 'user',
      content: inputValue
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    console.log("Sending request to:", `${apiUrl}/api/query`);
    
    try {
      // Call the backend API
      const response = await axios.post(`${apiUrl}/api/query`, {
        query: userMessage.content
      });

      console.log("API Response:", response.data);

      // Add assistant response to state
      const assistantMessage = {
        role: 'assistant',
        content: response.data.response
      };

      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
      
      // Set sources if available
      if (response.data.sources && response.data.sources.length > 0) {
        setSources(response.data.sources);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      console.error('Error details:', error.response?.data || error.message);
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.'
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle link selection
  const handleLinkSelect = (url) => {
    // Open the URL in a new tab
    window.open(url, '_blank', 'noopener,noreferrer');
    
    // Send feedback
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      axios.post(`${apiUrl}/api/feedback`, {
        query: messages[messages.length - 2]?.content || '',
        response: messages[messages.length - 1]?.content || '',
        helpful: true,
        selected_node_id: sources.find(s => s.url === url)?.id
      });
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message">
            <div className="message-content">
              <div className="loading-indicator">
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {sources.length > 0 && (
        <NavLinks sources={sources} onLinkSelect={handleLinkSelect} />
      )}

      <form className="input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Ask a question about navigating the platform..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface; 