# Python MCP Client
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://github.com/hwchase17/langchain)

Python MCP (Model Context Protocol) Client is a framework for creating and interacting with LLM-powered tools using standardized messaging protocols. This project demonstrates how to create MCP servers and clients in Python that can be used with LangChain and LangGraph.

![MCP Client Interface](./static/Screenshot%20from%202025-04-13%2006-50-45.png)

## Features

- **MCP Server Implementation**: Create servers with tools that can be accessed through the Model Context Protocol
- **Flask-based Web Interface**: Interact with MCP servers through a user-friendly web interface
- **LangChain & LangGraph Integration**: Utilize LangChain and LangGraph for LLM-powered agents
- **MySQL Integration**: Execute MySQL commands via MCP tools
- **Multi-Server Support**: Connect to multiple MCP servers simultaneously
- **Dynamic Server Management**: Add or configure servers at runtime

## Architecture

1. **Flask Web Application**: Serves as the frontend interface and API gateway
2. **MultiServerMCPClient**: Connects to multiple MCP servers (MySQL, File operations)
3. **LangChain React Agent**: Processes user queries and decides which tools to use
4. **MCP Servers**: Independent processes that expose tools through the Model Context Protocol

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- LangChain
- LangGraph
- OpenAI API key (for GPT-4o model)
- MCP libraries

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kernelmax/python-mcp-client.git
   cd python-mcp-client
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

### Running the Application

1. Start the Flask application:
   ```bash
   python flask_app.py
   ```

2. Open your browser and navigate to `http://localhost:5008`

## Usage Examples

### 1. Query a MySQL Database

```python
# Example user query
"Show me all users in the database that registered in the last month"

# How it works behind the scenes
# 1. The LLM agent processes the query
# 2. It selects the mysql_query tool
# 3. It generates and executes SQL: "SELECT * FROM users WHERE registration_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
# 4. Results are returned to the user
```

### 2. Create a New Database

```python
# Example user query
"Create a new database called customer_analytics"

# How it works behind the scenes
# 1. The LLM agent processes the query
# 2. It selects the mysql_create_database tool
# 3. It executes: mysql_create_database("customer_analytics")
# 4. Success message is returned to the user
```

### 3. File Operations

```python
# Example user query
"List all Python files in the current directory"

# How it works behind the scenes
# 1. The LLM agent processes the query
# 2. It selects the list_files tool
# 3. It filters the results for Python files
# 4. Filtered results are returned to the user
```

## API Endpoints

- `GET /api/tools`: Returns a list of all available tools from all servers
- `GET /api/servers`: Returns a list of configured MCP servers
- `POST /api/add_server`: Adds a new MCP server configuration
- `POST /api/process_query`: Processes a user query using the LLM agent

## Sample MCP Servers

### MySQL MCP Server (mysql_mcp_server.py)
A server that provides tools for MySQL database operations:
- Query execution
- Table creation, insertion, selection, updating, and deletion
- Database creation and management
- Database listing

### File MCP Server (file_mcp_server.py)
A server that provides tools for file system operations:
- Reading files
- Writing to files
- Creating new files
- Listing files in the current directory

## How It Works

1. The Flask app initializes connections to MCP servers
2. User queries are received through the web interface
3. The LangChain React Agent processes the query using GPT-4o
4. The agent selects appropriate tools from the available MCP servers
5. Tool calls are executed on the respective servers
6. Results are returned to the user through the web interface

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Ensure all MCP servers are running correctly
   - Check for port conflicts if using HTTP transport

2. **API Key Issues**:
   - Verify your OpenAI API key is set correctly
   - Check for sufficient API credits

3. **Tool Execution Failures**:
   - MySQL server must be running for MySQL tools
   - File paths must be accessible for file operation tools

## Roadmap

- [ ] Add authentication and user management
- [ ] Support for more database engines (PostgreSQL, MongoDB)
- [ ] Implement WebSocket transport for real-time communication
- [ ] Create a Docker compose setup for easier deployment
- [ ] Add unit and integration tests
- [ ] Implement persistent session storage

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests** (if available)
5. **Commit your changes**:
   ```bash
   git commit -m "Add some feature"
   ```
6. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request**

Please make sure your code follows the project's coding style and includes appropriate tests.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For questions or support, please open an issue on GitHub or contact the maintainers directly. 