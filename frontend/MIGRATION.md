# Migration from Create React App to Vite

This document outlines the steps taken to migrate the MCP Client frontend from Create React App (CRA) to Vite.

## Why Migrate to Vite?

The migration was performed to address several issues with Create React App:

1. **Deprecated Dependencies**: CRA was using many deprecated packages, causing npm warnings
2. **Performance**: Vite offers faster development server startup and hot module replacement
3. **Maintenance**: Vite is actively maintained and has fewer dependencies
4. **Modern Features**: Vite provides better support for modern JavaScript features and optimizations

## Migration Steps

### 1. Package.json Updates

- Removed CRA-specific dependencies:
  - Removed `react-scripts`
  - Removed testing libraries that were causing deprecation warnings
  - Removed `web-vitals`
- Added Vite dependencies:
  - Added `vite` as a dev dependency
  - Added `@vitejs/plugin-react` for JSX support
- Updated scripts:
  - Changed `start` to `dev`
  - Changed build commands to use Vite
- Added `"type": "module"` for ES modules support

### 2. Configuration Files

- Created `vite.config.js` with:
  - React plugin configuration
  - Development server settings
  - API proxy configuration (replacing the CRA proxy setting)

### 3. HTML Entry Point

- Moved `index.html` from `public/` to the root directory
- Updated HTML to use Vite's conventions:
  - Removed CRA-specific placeholders like `%PUBLIC_URL%`
  - Added script tag with `type="module"` pointing to the entry point

### 4. JavaScript Updates

- Updated `index.js`:
  - Removed CRA-specific imports like `reportWebVitals`
  - Simplified ReactDOM rendering
- Kept `App.js` and API service files unchanged as they were already compatible

### 5. Component Creation

- Created React components in JSX format:
  - `Sidebar.jsx` for displaying server information
  - `ChatArea.jsx` for the chat interface
- Used React Icons instead of Font Awesome classes for better React integration

### 6. Documentation

- Created a frontend README.md with Vite-specific instructions
- Updated the main project README.md to mention Vite
- Added this migration document

### 7. Git Configuration

- Updated .gitignore to include Vite and Node.js specific entries

## Running the Vite Frontend

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Benefits of the Migration

- **Cleaner Dependencies**: Fewer dependencies with no deprecation warnings
- **Faster Development**: Quicker startup and hot module replacement
- **Better Performance**: Optimized builds for production
- **Modern Tooling**: Access to the latest frontend development tools
- **Easier Maintenance**: Simpler configuration and better documentation

## Security Updates

### July 2025: Upgrade to Vite 7.0.5

- Updated Vite from version 5.0.8 to 7.0.5 to address security vulnerabilities:
  - Fixed a moderate severity vulnerability (GHSA-67mh-4wv8-2f99) in esbuild <=0.24.2
  - This vulnerability allowed any website to send requests to the development server and read the response
  - The fix was applied using `npm audit fix --force`

### July 2025: Plugin Compatibility Fix

- After upgrading to Vite 7.0.5, the `npm run dev` command was failing due to compatibility issues:
  - The @vitejs/plugin-react version 4.2.1 was not compatible with Vite 7.0.5
  - Initially tried updating to version 5.0.0, but found this version doesn't exist
  - Downgraded to @vitejs/plugin-react version 4.6.0 (the latest available version)
  - This resolved the dependency error and allowed the development server to run correctly

### July 2025: JSX File Extension Fix

- Encountered an error with JSX syntax in .js files:
  - Vite's import analysis plugin failed to parse JSX syntax in index.js and App.js
  - Renamed src/index.js to src/index.jsx and src/App.js to src/App.jsx to ensure proper processing
  - Updated the script reference in index.html to point to index.jsx
  - No changes needed for App imports as they don't include file extensions
  - These changes resolved the JSX parsing errors

#### Potential Breaking Changes in Vite 7.0.5

When upgrading from Vite 5.x to Vite 7.0.5, be aware of these potential breaking changes:

- API changes in Vite's plugin interface
- Changes to the default configuration and build output
- Updates to how assets are handled and processed
- Modifications to the development server behavior

If you encounter issues after the upgrade, consult the [Vite documentation](https://vitejs.dev/guide/) for migration guidance.

## Future Improvements

- Add TypeScript support
- Implement unit tests with Vitest
- Add ESLint and Prettier for code quality
- Consider adding a component library like Chakra UI or Material UI