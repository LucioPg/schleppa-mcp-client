import React, { useState, useEffect } from 'react';
import './styles/App.css';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import { fetchServers, fetchTools, processQuery } from './services/api';

function App() {
  const [servers, setServers] = useState([]);
  const [tools, setTools] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [thinking, setThinking] = useState(false);
  const [error, setError] = useState(null);

  // Load servers and tools on component mount
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const serversData = await fetchServers();
        setServers(serversData);
        
        const toolsData = await fetchTools();
        setTools(toolsData);
        
        // Add welcome message
        setMessages([
          {
            id: 'welcome',
            type: 'welcome',
            content: 'Welcome to MCP Client Interface'
          }
        ]);
      } catch (err) {
        console.error('Error loading data:', err);
        setError('Failed to load servers and tools. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Handle sending a message
  const handleSendMessage = async (message) => {
    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: message
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    
    // Show thinking indicator
    setThinking(true);
    
    try {
      // Process query
      const response = await processQuery(message);
      
      // Add bot message to chat
      const botMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: response.final_answer || 'Sorry, I could not process this request.',
        toolUsage: response.tool_usage || []
      };
      
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (err) {
      console.error('Error processing query:', err);
      
      // Add error message to chat
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'error',
        content: `Error: ${err.message || 'Something went wrong'}`
      };
      
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      // Hide thinking indicator
      setThinking(false);
    }
  };

  return (
    <div className="app-container">
      <Sidebar servers={servers} tools={tools} loading={loading} />
      <ChatArea 
        messages={messages} 
        thinking={thinking} 
        onSendMessage={handleSendMessage} 
        error={error}
      />
    </div>
  );
}

export default App;