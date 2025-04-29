import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendMessage, clearChatHistory } from '../services/api';
import '../styles/ChatWindow.css';

// Define message type
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'error';
  timestamp: Date;
}

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isClearingChat, setIsClearingChat] = useState<boolean>(false);

  // Show welcome message on first load
  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMessage: Message = {
        id: 'welcome',
        content: 'Hello! I am your AI assistant. How can I help you today?',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, [messages.length]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;
    
    // Create a new user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };
    
    // Add user message to the chat
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);
    setError(null);
    
    try {
      // Send the message to the API
      const response = await sendMessage(content);
      
      // Create an assistant message from the response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        role: 'assistant',
        timestamp: new Date(),
      };
      
      // Add the assistant message to the chat
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (err: any) {
      console.error('Error sending message:', err);
      
      // Create error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: err.message || 'Failed to send message. Please try again.',
        role: 'error',
        timestamp: new Date(),
      };
      
      // Add the error message to the chat
      setMessages(prevMessages => [...prevMessages, errorMessage]);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    // Get the last user message
    const lastUserMessage = [...messages].reverse().find(m => m.role === 'user');
    if (lastUserMessage) {
      handleSendMessage(lastUserMessage.content);
    } else {
      setError('No previous message to retry');
    }
  };

  const handleClearChat = async () => {
    if (isClearingChat) return; // Prevent multiple clear attempts
    
    setIsClearingChat(true);
    setError(null);
    
    try {
      console.log('[DEBUG] Starting chat clear process');
      const response = await clearChatHistory();
      console.log('[DEBUG] Clear chat response:', response);
      
      if (response.success) {
        // Reset messages to just the welcome message
        const welcomeMessage: Message = {
          id: 'welcome',
          content: 'Chat history cleared. How can I help you today?',
          role: 'assistant',
          timestamp: new Date(),
        };
        setMessages([welcomeMessage]);
        setError(null);
        console.log('[DEBUG] Chat cleared successfully');
      } else {
        throw new Error(response.message || 'Failed to clear chat history');
      }
    } catch (err: any) {
      console.error('[DEBUG] Error in handleClearChat:', err);
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: err.message || 'Failed to clear chat history. Please try again.',
        role: 'error',
        timestamp: new Date(),
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
      setError('Failed to clear chat history. Please try again.');
    } finally {
      setIsClearingChat(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Chat Agent</h3>
      </div>
      <div className="chat-container">
        <MessageList messages={messages} />
        
        {isLoading && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
            <div className="typing-text">AI is thinking...</div>
          </div>
        )}
        
        {error && (
          <div className="error-container">
            <div className="error-message">{error}</div>
            <button className="retry-button" onClick={handleRetry}>
              Retry
            </button>
          </div>
        )}
        
        <div className="chat-controls">
          <button 
            className="clear-chat-button"
            onClick={handleClearChat}
            disabled={isClearingChat || messages.length <= 1}
          >
            {isClearingChat ? 'Clearing...' : 'Clear Chat'}
          </button>
          <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow; 