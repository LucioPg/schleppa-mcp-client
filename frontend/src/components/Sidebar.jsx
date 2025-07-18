import React, { useState } from 'react';
import { FaServer, FaPlus, FaChevronDown, FaTools } from 'react-icons/fa';

const Sidebar = ({ servers, tools, loading }) => {
  const [expandedServer, setExpandedServer] = useState(null);
  const [showToolsModal, setShowToolsModal] = useState(false);
  const [selectedServer, setSelectedServer] = useState(null);

  // Toggle server expansion
  const toggleServerExpansion = (serverId) => {
    setExpandedServer(expandedServer === serverId ? null : serverId);
  };

  // Show tools modal for a server
  const handleViewTools = (e, server) => {
    e.stopPropagation();
    setSelectedServer(server);
    setShowToolsModal(true);
  };

  // Filter tools for a specific server
  const getServerTools = (serverId) => {
    return tools.filter(tool => {
      if (tool.server) {
        return tool.server === serverId;
      } else {
        // Fallback server assignment based on tool name
        if (serverId === 'mysql') {
          return tool.name.toLowerCase().includes('sql') || 
            tool.name.toLowerCase().includes('database') ||
            tool.name.toLowerCase().includes('query');
        } else if (serverId === 'file') {
          return tool.name.toLowerCase().includes('file') || 
            tool.name.toLowerCase().includes('read') || 
            tool.name.toLowerCase().includes('write') ||
            tool.name.toLowerCase().includes('list');
        }
        return false;
      }
    });
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h4><FaServer className="me-2" /> MCP</h4>
      </div>
      
      <div id="servers-container">
        {loading ? (
          <div className="loading-spinner">
            <i className="fas fa-circle-notch fa-spin"></i> Loading servers...
          </div>
        ) : servers.length > 0 ? (
          servers.map((server) => (
            <div 
              key={server.id} 
              className={`server-details ${expandedServer === server.id ? 'active' : ''}`}
              data-server-id={server.id}
            >
              <div 
                className="server-header" 
                onClick={() => toggleServerExpansion(server.id)}
              >
                <h6>
                  <i className={`fas ${server.id === 'mysql' ? 'fa-database' : 'fa-file-alt'}`}></i>
                  {server.name} MCP Server
                </h6>
                <FaChevronDown className={`toggle-icon ${expandedServer !== server.id ? 'collapsed' : ''}`} />
              </div>
              
              <div className={`server-content ${expandedServer === server.id ? 'expanded' : ''}`}>
                <div className="server-info-details">
                  <div className="detail-item">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{server.type}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Command:</span>
                    <span className="detail-value">{server.command}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Transport:</span>
                    <span className="detail-value">{server.transport}</span>
                  </div>
                  
                  {server.args && server.args.length > 0 && (
                    <div className="detail-item">
                      <span className="detail-label">Script:</span>
                      <span className="detail-value">{server.args[0].split('/').pop()}</span>
                    </div>
                  )}
                  
                  <button 
                    className="view-tools-btn" 
                    onClick={(e) => handleViewTools(e, server)}
                  >
                    <FaTools className="me-1" /> View Tools
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-servers">No MCP servers available</div>
        )}
      </div>
      
      <div className="add-server-container">
        <button id="addServerBtn" className="add-server-btn">
          <FaPlus className="me-2" /> Add Server
        </button>
      </div>
      
      {/* Tools Modal would be implemented in a separate component or in the parent App component */}
    </div>
  );
};

export default Sidebar;