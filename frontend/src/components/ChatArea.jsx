import React, { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaPalette } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';

const ChatArea = ({ messages, thinking, onSendMessage, error }) => {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef(null);
  const chatMessagesRef = useRef(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  // Render different message types
  const renderMessage = (msg) => {
    switch (msg.type) {
      case 'user':
        return <div className="message user-message">{msg.content}</div>;
      
      case 'bot':
        return (
          <div className="message bot-message">
            <ReactMarkdown>{msg.content}</ReactMarkdown>
            
            {/* Tool badges */}
            {msg.toolUsage && msg.toolUsage.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px', marginTop: '10px' }}>
                {msg.toolUsage.map((tool, index) => (
                  <div key={index} className="tool-badge">
                    <i className="fas fa-wrench"></i>
                    {tool.tool || tool.name || "Tool"}
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      
      case 'error':
        return <div className="message error-message">{msg.content}</div>;
      
      case 'welcome':
        return (
          <div className="welcome-message">
            <i className="fas fa-terminal"></i>
            <h4>MCP Client Interface</h4>
            <p>Try asking about your connected MCP servers and tools.</p>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="main-content">
      <div className="chat-header">
        <div className="header-title">
          <svg className="mcp-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 4C8.68629 4 6 6.68629 6 10C6 11.2144 6.36084 12.3435 6.98117 13.2895C7.89138 14.7478 7.89138 16.6456 6.98117 18.1039M12 4C15.3137 4 18 6.68629 18 10C18 11.2144 17.6392 12.3435 17.0188 13.2895C16.1086 14.7478 16.1086 16.6456 17.0188 18.1039M12 4V2M6.98117 18.1039C6.46012 18.9073 5.55694 19.4634 4.5 19.5V22M17.0188 18.1039C17.5399 18.9073 18.4431 19.4634 19.5 19.5V22M8.5 10.5H15.5M8.5 13.5H15.5" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <circle cx="12" cy="10" r="8" stroke="white" strokeWidth="2" opacity="0.2"/>
          </svg>
          <h3>PYTHON MCP CLIENT</h3>
          <span className="server-info">Connected to MCP servers</span>
        </div>
        <div className="theme-toggle">
          <FaPalette />
        </div>
      </div>
      
      <div className="chat-messages" ref={chatMessagesRef}>
        {error && <div className="message error-message">{error}</div>}
        
        {messages.map((msg) => (
          <React.Fragment key={msg.id}>
            {renderMessage(msg)}
          </React.Fragment>
        ))}
        
        {thinking && (
          <div className="loading-message">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <circle cx="4" cy="12" r="2" fill="#7e8cc0">
                <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0" />
              </circle>
              <circle cx="12" cy="12" r="2" fill="#7e8cc0">
                <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.3" />
              </circle>
              <circle cx="20" cy="12" r="2" fill="#7e8cc0">
                <animate attributeName="opacity" dur="1s" values="0;1;0" repeatCount="indefinite" begin="0.6" />
              </circle>
            </svg>
            <span>Processing your request...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            autoComplete="off"
          />
          <button type="submit">
            <FaPaperPlane />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatArea;