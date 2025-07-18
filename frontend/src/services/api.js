import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Fetch all available servers
 * @returns {Promise<Array>} Array of server objects
 */
export const fetchServers = async () => {
  try {
    const response = await api.get('/servers');
    
    // Transform the server data from object to array format
    const serverArray = Object.entries(response.data).map(([name, details]) => ({
      id: name,
      name: name.charAt(0).toUpperCase() + name.slice(1), // Capitalize first letter
      type: "Python",
      command: details.command,
      transport: details.transport || "stdio",
      args: details.args || []
    }));
    
    return serverArray;
  } catch (error) {
    console.error('Error fetching servers:', error);
    throw error;
  }
};

/**
 * Fetch all available tools
 * @returns {Promise<Array>} Array of tool objects
 */
export const fetchTools = async () => {
  try {
    const response = await api.get('/tools');
    return response.data;
  } catch (error) {
    console.error('Error fetching tools:', error);
    throw error;
  }
};

/**
 * Process a user query
 * @param {string} query - The user's query
 * @returns {Promise<Object>} Response object with final_answer and tool_usage
 */
export const processQuery = async (query) => {
  try {
    const response = await api.post('/process_query', { query });
    return response.data;
  } catch (error) {
    console.error('Error processing query:', error);
    throw error;
  }
};

/**
 * Add a new server
 * @param {string} name - Server name
 * @param {Object} config - Server configuration
 * @returns {Promise<Object>} Response object
 */
export const addServer = async (name, config) => {
  try {
    const response = await api.post('/add_server', { 
      name,
      config
    });
    return response.data;
  } catch (error) {
    console.error('Error adding server:', error);
    throw error;
  }
};

export default api;