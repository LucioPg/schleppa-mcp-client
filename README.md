# Python MCP Client

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
   ```
   git clone https://github.com/kernelmax/python-mcp-client.git
   cd python-mcp-client
   ```

2. Set up a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```
   export OPENAI_API_KEY=your-api-key-here
   ```

### Running the Application

1. Start the Flask application:
   ```
   python flask_app.py
   ```

2. Open your browser and navigate to `http://localhost:5008`

## Usage

### Interacting with the MCP Client

The web interface allows you to:

1. Send natural language queries to the LLM agent
2. View available tools across all connected MCP servers
3. Add new MCP servers dynamically

### Example Queries

- "Query the users table in MySQL"
- "Create a new database called test_db"
- "List all tables in the current database"

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

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub or contact the maintainers directly. 