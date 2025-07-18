# Python Client for MCP Servers (Web Based Platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://github.com/hwchase17/langchain)
[![LLM Tools](https://img.shields.io/badge/LLM-Tools-orange.svg)](https://github.com/LucioPg/schleppa-mcp-client)
[![Open Source](https://img.shields.io/badge/Open-Source-brightgreen.svg)](https://github.com/LucioPg/schleppa-mcp-client)

A desktop application for connecting to multiple MCP servers for Ollama models, enabling natural language interactions with databases, file systems, and web services. Connect with pre-built or custom MCP implementations in a unified interface. Future integrations include Google Workspace, Microsoft 365, Slack, Salesforce, and GitHub. Free to use under the MIT license.

![MCP Client Interface - LLM-powered tool orchestration dashboard](./static/Screenshot%20from%202025-04-13%2006-50-45.png)

## 🚀 Key Features
- **Ollama Models**: Officially supported
- **MCP Tool Orchestration**: Build and connect powerful LLM tools using standardized messaging protocols
- **Desktop Application**: Electron-based desktop app for local operation with React frontend and Flask backend
- **LangChain & LangGraph Integration**: Create sophisticated AI workflows with industry-standard frameworks
- **Multi-Server Support**: Connect to multiple tool servers simultaneously from a single interface
- **Dynamic Server Management**: Add, configure, and update tool servers at runtime without restarts
- **Local Operation**: Works entirely locally for improved security and privacy
- **Easy Debugging**: Built-in tools for debugging both frontend and backend

## 🏗️ Architecture Overview

1. **Electron Desktop Application**: Cross-platform desktop application framework for local operation
2. **React Frontend with Vite**: Fast, modern React components built with Vite for improved performance and development experience
3. **Flask Backend**: Robust Python backend providing REST API endpoints for the frontend
4. **MultiServerMCPClient**: Advanced client that orchestrates connections to multiple tool servers
5. **LangChain React Agent**: Intelligent decision-making system that chooses the right tools for each task
6. **MCP Servers**: Specialized microservices that expose domain-specific tools through a standardized protocol

## 🔧 Getting Started with Python MCP

### Installation Options

#### Option 1: Install from PyPI (Recommended)
The simplest way to install Python MCP Client is via pip:

```bash
pip install schleppa-mcp-client
```

You can find the package on PyPI at: [https://pypi.org/project/schleppa-mcp-client/](https://pypi.org/project/schleppa-mcp-client/)

#### Option 2: Install from Source
If you want the latest development version or plan to contribute:

1. Clone the repository:
   ```bash
   git clone https://github.com/LucioPg/schleppa-mcp-client.git
   cd schleppa-mcp-client
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

### Running Your AI Tool Platform

#### Option 1: Run as Desktop Application (Recommended)

##### Windows Users (Easiest Method)

1. Simply double-click the `start-app.bat` file in the project root directory.
   - This batch file will automatically check for Node.js, install dependencies if needed, and start the application.
   - The first run may take a few minutes as it installs dependencies.
   - The application will launch as an Electron desktop app, not just in a browser window.
   - If you encounter any issues, you can try running the `test-electron.bat` file which directly tests the Electron launch process.

##### Manual Setup (All Platforms)

1. Install frontend dependencies (first time only):
   ```bash
   cd frontend
   npm install
   ```

2. Run the Electron desktop application in development mode:
   - On Windows:
     ```powershell
     cd frontend
     npm run start
     ```
   - On macOS/Linux:
     ```bash
     cd frontend
     npm run electron:dev
     ```
   This will start both the Vite development server and the Electron app, with the Flask backend running as a child process.

3. For production builds:
   ```bash
   cd frontend
   npm run electron:build
   ```
   This will create a distributable package in the `frontend/release` directory.

#### Option 2: Run as Web Application (Legacy)

1. Start the Flask backend:
   ```bash
   python flask_app.py
   ```

2. Start the React frontend (in a separate terminal):
   ```bash
   cd frontend
   npm install  # Only needed the first time
   npm run dev
   ```

3. Open your browser and navigate to:
   - Frontend: `http://localhost:5173` (Vite development server)
   - Backend API: `http://localhost:5008` (Flask server)

### Debugging Your Application

The project includes VS Code debugging configurations for both the frontend and backend:

1. **Frontend Debugging**:
   - Use the "Debug Electron Main Process" configuration to debug the Electron main process
   - Use the "Debug Electron Renderer Process" configuration to debug the React frontend

2. **Backend Debugging**:
   - Use the "Debug Flask Backend" configuration to debug the Flask backend

3. **Combined Debugging**:
   - Use the "Debug Electron + Flask (Compound)" configuration to debug both the frontend and backend simultaneously

These configurations are available in the VS Code debug panel and provide full debugging capabilities including breakpoints, variable inspection, and step-through debugging.

### Troubleshooting

If you encounter issues with the Electron desktop application:

1. **Application opens in browser instead of as desktop app**:
   - Make sure you're using the `start-app.bat` file or running `npm run electron:dev:win` from the frontend directory
   - Try running the `test-electron.bat` file which directly tests the Electron launch process
   - Check that all dependencies are installed correctly with `npm install` in the frontend directory

2. **Backend connection issues**:
   - Verify that the Flask backend is running (you should see console output indicating it started)
   - Check that the backend is running on port 5008 as expected
   - Look for any error messages in the Electron console (View > Toggle Developer Tools)

3. **Dependency issues**:
   - Run `npm audit` in the frontend directory to check for any package vulnerabilities
   - Try deleting the `node_modules` folder and running `npm install` again
   - Make sure you have the latest version of Node.js installed

#### Option 3: Run with Docker

You can also run Python MCP Client using Docker:

1. Pull the pre-built image from Docker Hub:
   ```bash
   docker pull LucioPg/schleppa-mcp-client
   ```

2. Run the container:
   ```bash
   docker run -p 5008:5008 -e OPENAI_API_KEY=your-api-key-here LucioPg/schleppa-mcp-client
   ```

3. Open your browser and navigate to `http://localhost:5008`

#### Option 4: Run with Docker Compose

For a more convenient setup, you can use Docker Compose:

1. Create a `docker-compose.yml` file or use the one provided in the repository:
   ```yaml
   version: '3'
   services:
     mcp-app:
       image: LucioPg/schleppa-mcp-client
       # or build from source:
       # build: .
       ports:
         - "5008:5008"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
       volumes:
         - ./templates:/app/templates
       restart: unless-stopped
   ```

2. Set your OpenAI API key in your environment:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

3. Start the service:
   ```bash
   docker-compose up
   ```

4. Open your browser and navigate to `http://localhost:5008`

## 💡 Natural Language AI Tool Examples

### Database Management with Natural Language

```python
# Example natural language query
"Show me all users in the database that registered in the last month"

# How the AI agent processes your request
# 1. The LLM agent interprets the natural language query
# 2. It selects the appropriate database tool
# 3. It generates and executes optimized SQL: "SELECT * FROM users WHERE registration_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
# 4. Results are returned in a human-readable format
```

### Database Creation Through Conversation

```python
# Example natural language command
"Create a new database called customer_analytics"

# How the AI agent executes your request
# 1. The LLM agent processes your instructions
# 2. It selects the database creation tool
# 3. It executes the appropriate command with error handling
# 4. Confirmation is provided with next steps
```

### Intelligent File Operations

```python
# Example natural language request
"List all Python files in the current directory"

# How the AI assistant helps you
# 1. The LLM agent processes your request
# 2. It selects the file system tools
# 3. It intelligently filters results for Python files
# 4. Results are displayed in an organized format
```

## 🛠️ Available MCP Tool Servers

### MySQL Database Assistant
A powerful AI database interface providing tools for:
- SQL query execution with natural language translation
- Automated table creation, insertion, and data manipulation
- Database management with intelligent suggestions
- Schema visualization and exploration

### File System Navigator
An intelligent file system assistant with tools for:
- Context-aware file reading and analysis
- Smart file writing with formatting suggestions
- Automatic file creation with templates
- Directory organization and file discovery

## 🔮 Future Development Roadmap

- [ ] **User Authentication**: Secure access control with role-based permissions
- [ ] **Database Engine Expansion**: Support for PostgreSQL, MongoDB, and other databases
- [ ] **Real-time Communication**: WebSocket integration for live updates and responses
- [x] **Containerized Deployment**: Docker compose setup for one-click deployment
- [ ] **Comprehensive Testing**: Extensive test suite for reliability and stability
- [ ] **Session Persistence**: Save and resume conversations with your AI tools

### Planned MCP Server Integrations

We plan to expand our MCP server ecosystem with integrations for popular platforms:

- [ ] **Google Workspace**: Connect to Gmail, Google Docs, Google Drive, and Google Calendar
- [ ] **Microsoft 365**: Integrate with Outlook, OneDrive, and Microsoft Teams
- [ ] **Slack**: Send messages, manage channels, and automate workflows
- [ ] **Salesforce**: Query customer data, manage leads, and update records
- [ ] **Jira**: Create and manage issues, track projects, and generate reports
- [ ] **GitHub**: Manage repositories, issues, and pull requests
- [ ] **Zoho**: Connect to Zoho CRM, Zoho Books, and other Zoho applications
- [ ] **Zendesk**: Handle support tickets and customer inquiries
- [ ] **HubSpot**: Manage marketing campaigns and customer relationships
- [ ] **Notion**: Create and update pages, databases, and workspaces

## 💪 How to Contribute

We **enthusiastically welcome** contributors of all experience levels! Whether you're fixing a typo, improving documentation, or adding a major feature, your help makes this project better.

### Ways to Contribute

- **Code contributions**: Add new features or fix bugs
- **Documentation**: Improve explanations, add examples, or fix typos
- **Bug reports**: Help us identify issues
- **Feature requests**: Suggest new capabilities
- **User experience**: Provide feedback on usability
- **Testing**: Help ensure everything works properly

### Getting Started for New Contributors

If you're new to open source or this project, look for issues tagged with `good-first-issue` or `beginner-friendly`. These are carefully selected to be accessible entry points.

Need help? Join our [community chat](https://discord.gg/example) or ask questions in the issue you're working on.

### Contribution Workflow

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/LucioPg/schleppa-mcp-client.git
   cd schleppa-mcp-client
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test your changes**:
   ```bash
   # Run tests to ensure nothing breaks
   pytest
   ```
6. **Commit your changes** with a clear message:
   ```bash
   git commit -m "Add: clear description of your changes"
   ```
7. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a pull request** with a description of your changes

### Code Review Process

All submissions require review before merging:

1. A maintainer will review your PR
2. They may request changes or clarification
3. Once approved, your contribution will be merged

Thank you for contributing to make Python MCP Client better for everyone!

## 🏷️ Repository Tags and Topics

This project is tagged with the following GitHub topics to improve discoverability:

- `mcp` - Model Context Protocol implementation
- `ai-agent` - Artificial intelligence agent architecture
- `langchain` - LangChain framework integration
- `langgraph` - LangGraph agent workflows
- `python-ai` - Python-based artificial intelligence
- `llm-tools` - Large Language Model tooling
- `llm-orchestration` - LLM tool orchestration
- `ai-assistant` - AI assistant capabilities
- `language-model-tools` - Tools for language models
- `agent-framework` - Framework for building AI agents
- `multi-tool-agent` - Agent with multiple tool capabilities
- `python-llm` - Python LLM integration
- `openai-integration` - OpenAI model integration
- `natural-language-processing` - NLP capabilities

If you're forking or referencing this project, consider using these tags for consistency and to help others find related work.

### Adding Tags to Your Fork

When working with a fork of this repository, you can add these tags to improve its discoverability:

1. Go to your fork on GitHub
2. Click on the gear icon next to "About" on the right sidebar
3. Enter relevant topics in the "Topics" field
4. Click "Save changes"

Using consistent tagging helps build a connected ecosystem of related projects!

## 📜 License Information

This project is fully open source and available under the [MIT License](LICENSE). This means you are free to:

- Use the code commercially
- Modify the code
- Distribute your modifications
- Use privately
- Sublicense

We believe in the power of open source to drive innovation and make AI tools accessible to everyone. By making this project open source, we encourage collaboration, transparency, and community-driven development.

## 📬 Contact & Support

For questions, feature requests, or support, please open an issue on GitHub or contact the maintainers directly. 


# New Features
#### file: .guidelines.md
This document describes all the new features
that should be implemented, divided by stages.


### Stage 1
- [x] **deprecated** The browser interface ( aka frontend) must be converted in reactjs
- [x] The frontend must be converted into an Electron App for local operation
- [x] All the necessary tools for the frontend must be added
- [x] The frontend MUST be easily debuggable
- [x] The backend MUST be easily debuggable
- [x] The frontend must be separated from the backend logic
- [x] The backend must work async and provide rest api endpoints

### Stage 2
- [ ] The llm answer must be streamed
- [ ] The Thinking part of the llm answer MUST be enclosed in a box, clearly separated from the actual answer
- [ ] The Human message must have three buttons just below the submitted prompt:
  - Copy: copy the message in the system clipboard
  - Edit: edit the Human message in a modal dialog window, with two buttons Abort and Ok, if the user clicks outside the dialog, the dialog must be closed with abort. When the dialog accepts the edit all the message history after that message MUST be deleted, in this way the message history can continue with the edited Human message and the next llm answer
  - Delete: delete the Human message, the history should be truncated
- [ ] The conversations must be stored in a database, with a unique id, datetime, llm model in use and maybe something else
- [ ] The conversations must be listed in an accordion or similar on one of the side the chat window
- [ ] The User should have the opportunity to select a previous conversation and continue
- [ ] The User Must have the opportunity to attach images and documents to the chat
- [ ] The Interface must provide a dialog box that allows the user to edit the model parameters such as:
  - temperature
  - top_p
  - system prompt
  - attachment process mode (if the attached file should be converted in base64 or attached to the prompt just by using the path)
  - context length strategy (sliding window, summarize the oldest, truncate the oldest, summarize the middle)
- [ ] The context strategies must be implemented
- [ ] The Interface must show what the context fullness percentage is (counting the overall tokens) 
- [ ] The model parameters must be validated through a pydantic model
- [ ] The Interface must provide a dialog box that allows the user to select which model to run
- [ ] The llm answer must provide the args used to call the tool and the related tool response
