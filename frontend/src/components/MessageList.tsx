import React, { useEffect, useRef } from 'react';
import { Message } from './ChatWindow';
import '../styles/MessageList.css';

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Format timestamp nicely
  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-message">
          <p>No messages yet. Start a conversation!</p>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.role}`}>
              {message.role === 'assistant' && (
                <div className="avatar assistant-avatar">AI</div>
              )}
              <div className="message-bubble">
                {message.content}
                <span className="message-timestamp">
                  {formatTime(message.timestamp)}
                </span>
              </div>
              {message.role === 'user' && (
                <div className="avatar user-avatar">You</div>
              )}
            </div>
          ))}
          {/* Invisible div at the end for auto-scrolling */}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};

export default MessageList; 