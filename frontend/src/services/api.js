import axios from 'axios';
let envs = null
let FLASK_URL = null
let api = null;

const initEnvs = async () => {
  if(!envs){
    envs = await window.electron.getEnv().then(envs => {return envs});
    FLASK_URL = `http://${envs.FLASK_HOST}:${envs.FLASK_PORT}/api`;
    console.log('ENVS HAVE BEEN LOADED: ',envs);

  }
  return envs
};

// Inizializza l'istanza axios in modo asincrono
const initializeApi = async () => {
  if (!api) {
    const baseURL = await getBaseUrl();
    api = axios.create({
      baseURL: baseURL,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
  return api;
};


/**
 * Determine the base URL for API requests
 * In Electron (desktop mode), we need to use the full URL with the port
 * In web mode, we can use the relative URL
 */
const getBaseUrl = async () => {
  // Check if we're running in Electron
  const isElectron = window.electron !== undefined;
  
  if (isElectron) {
    // In Electron, use the full URL with the port
    // The Flask backend runs on port 5008 by default
    await initEnvs();
    return `${FLASK_URL}`;
  } else {
    // In web mode, use the relative URL
    return '/api';
  }
};

// Create an axios instance with default config
// rimpiazzata con una funzione async
// const api = axios.create({
//   baseURL: getBaseUrl(),
//   headers: {
//     'Content-Type': 'application/json'
//   }
// });

/**
 * Fetch all available servers
 * @returns {Promise<Array>} Array of server objects
 */
export const fetchServers = async () => {
  try {
    const api = await initializeApi();
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
    const api = await initializeApi();
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
    const api = await initializeApi();
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
    const api = await initializeApi();
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

// Funzione helper per ottenere l'istanza API
export const getApiInstance = () => initializeApi();
