# MCP Client Frontend

This is the React frontend for the Python MCP Client application. It's built with Vite for faster development and smaller production builds.

## Features

- Modern React application with Vite build system
- Connects to the Flask backend API
- Displays available MCP servers and their tools
- Chat interface for interacting with MCP servers
- Responsive design with Bootstrap

## Prerequisites

- Node.js 14.18+ or 16+
- npm or yarn
- Python Flask backend running on port 5000

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

To start the development server:

```bash
npm run dev
```

This will start the Vite development server on port 3000 with hot module replacement (HMR) enabled.

The development server is configured to proxy API requests to the Flask backend running on port 5000.

## Building for Production

To build the application for production:

```bash
npm run build
```

This will create a `dist` directory with optimized production files.

To preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   │   ├── Sidebar.jsx
│   │   └── ChatArea.jsx
│   ├── services/     # API services
│   │   └── api.js
│   ├── styles/       # CSS styles
│   │   ├── App.css
│   │   └── index.css
│   ├── App.js        # Main App component
│   └── index.js      # Entry point
├── index.html        # HTML template
├── vite.config.js    # Vite configuration
└── package.json      # Dependencies and scripts
```

## API Integration

The frontend communicates with the Flask backend through the API service defined in `src/services/api.js`. The Vite development server is configured to proxy API requests to the backend.

## Notes

- Make sure the Flask backend is running on port 5000 before starting the frontend
- The frontend is configured to work with the API endpoints provided by the backend
- For production deployment, you may need to adjust the API base URL in the api.js file