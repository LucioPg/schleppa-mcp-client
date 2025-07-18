// preload.js - Secure bridge between Electron main process and renderer process
const { contextBridge, ipcRenderer } = require('electron');
/**
 * Expose protected methods that allow the renderer process to use
 * the ipcRenderer without exposing the entire object
 */
contextBridge.exposeInMainWorld(
  'electron', 
  {
    /**
     * Get the application version from package.json
     * @returns {Promise<string>} Application version
     */
    getAppVersion: () => ipcRenderer.invoke('get-app-version'),
    
    /**
     * Open the developer tools
     */
    openDevTools: () => ipcRenderer.send('open-dev-tools'),
    
    /**
     * Listen for backend status updates
     * @param {Function} callback Function to call when backend status changes
     * @returns {Function} Function to remove the listener
     */
    onBackendStatus: (callback) => {
      // Add the event listener
      const listener = (_, status) => callback(status);
      ipcRenderer.on('backend-status', listener);
      
      // Return a function to remove the listener
      return () => {
        ipcRenderer.removeListener('backend-status', listener);
      };
    },
    getEnv: async () => {
    return await ipcRenderer.invoke('get-env');
    },
    /**
     * Check if running in Electron
     * @returns {boolean} True if running in Electron
     */
    isElectron: true,
  }
);

// Log when preload script has loaded
console.log('Preload script loaded successfully');