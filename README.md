# Python MCP Client

Python MCP (Message Communication Protocol) Client is a framework for creating and interacting with tools using standardized messaging protocols. This project demonstrates how to create and use MCP servers and clients in Python.

![MCP Client Interface](./static/Screenshot%20from%202025-04-13%2006-50-45.png)

## Features

- **MCP Server Implementation**: Create servers with tools that can be accessed through the MCP protocol
- **Flask-based Web Interface**: Interact with MCP servers through a user-friendly web interface
- **MySQL Integration**: Execute MySQL commands via MCP tools
- **Dynamic Server Management**: Add or configure servers at runtime

## Components

1. **Flask App**: Web interface for interacting with MCP servers and tools
2. **MySQL MCP Server**: Provides tools for MySQL database operations
3. **Client Interface**: Simple user interface to send commands to MCP servers

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- LangChain
- LangGraph
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

2. Open your browser and navigate to `http://localhost:5000`

## Usage

### Interacting with MySQL Server

You can send SQL queries through the MCP client interface. Examples:

- "Query the users table in MySQL"
- "Create a new database called test_db"
- "List all tables in the current database"

## Project Structure

- `flask_app.py`: Main Flask application
- `mysql_mcp_server.py`: MySQL MCP server implementation
- `file_mcp_server.py`: File operations MCP server
- `static/`: Static files for the web interface
- `templates/`: HTML templates for the web interface

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub or contact the maintainers directly. 