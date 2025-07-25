# Python Client for MCP Servers (Web Based Platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://github.com/hwchase17/langchain)
[![LLM Tools](https://img.shields.io/badge/LLM-Tools-orange.svg)](https://github.com/LucioPg/schleppa-mcp-client)
[![Open Source](https://img.shields.io/badge/Open-Source-brightgreen.svg)](https://github.com/LucioPg/schleppa-mcp-client)

A web-based Python platform for connecting to multiple MCP servers, enabling natural language interactions with databases, file systems, and web services. Connect with pre-built or custom MCP implementations in a unified interface. Future integrations include Google Workspace, Microsoft 365, Slack, Salesforce, and GitHub. Free to use under the MIT license.

![MCP Client Interface - LLM-powered tool orchestration dashboard](https://raw.githubusercontent.com/LucioPg/schleppa-mcp-client/main/static/Screenshot%20from%202025-04-13%2006-50-45.png)

## 🚀 Key Features

- **MCP Tool Orchestration**: Build and connect powerful LLM tools using standardized messaging protocols
- **Flask Web Interface**: Interact with AI agents through an intuitive, user-friendly dashboard
- **LangChain & LangGraph Integration**: Create sophisticated AI workflows with industry-standard frameworks
- **Multi-Server Support**: Connect to multiple tool servers simultaneously from a single interface
- **Dynamic Server Management**: Add, configure, and update tool servers at runtime without restarts

## 🏗️ Architecture Overview

1. **Flask Web Application**: Modern web interface serving as the command center for your AI tools
2. **MultiServerMCPClient**: Advanced client that orchestrates connections to multiple tool servers
3. **LangChain React Agent**: Intelligent decision-making system that chooses the right tools for each task
4. **MCP Servers**: Specialized microservices that expose domain-specific tools through a standardized protocol

## 🔧 Getting Started with Python MCP

### Installation Options

#### Option 1: Install from PyPI (Recommended)
The simplest way to install Python MCP Client is via pip:

```bash
pip install schleppa-mcp-client
```

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

1. Start the Flask application:
   ```bash
   python flask_app.py
   ```

2. Open your browser and navigate to `http://localhost:5008`

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
- [ ] **Containerized Deployment**: Docker compose setup for one-click deployment
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

Contribute to the project on GitHub: [https://github.com/LucioPg/schleppa-mcp-client](https://github.com/LucioPg/schleppa-mcp-client)

### Ways to Contribute

- **Code contributions**: Add new features or fix bugs
- **Documentation**: Improve explanations, add examples, or fix typos
- **Bug reports**: Help us identify issues
- **Feature requests**: Suggest new capabilities
- **User experience**: Provide feedback on usability
- **Testing**: Help ensure everything works properly

## 📜 License Information

This project is fully open source and available under the [MIT License](LICENSE). This means you are free to:

- Use the code commercially
- Modify the code
- Distribute your modifications
- Use privately
- Sublicense

We believe in the power of open source to drive innovation and make AI tools accessible to everyone. By making this project open source, we encourage collaboration, transparency, and community-driven development.

## 📬 Contact & Support

For questions, feature requests, or support, please open an issue on [GitHub](https://github.com/LucioPg/schleppa-mcp-client/issues) or contact the maintainers directly. 