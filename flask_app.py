from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS for cross-origin support
import asyncio
import os
import json
import logging
import sys
import signal
import atexit
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend.log')
    ]
)
logger = logging.getLogger('mcp-backend')

# Load environment variables
load_dotenv()

# Variabili globali per la gestione dei processi MCP
mcp_processes = []
shutdown_flag = False

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes - needed for Electron app
CORS(app)

# Get the absolute path to server scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")  # "openai" or "ollama"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen14_max")  # Default Ollama model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "fadsf11123fadf3vfa!!£fasdf4")

FLASK_PORT = os.getenv("FLASK_PORT", 5008)

servers = {
    "mysql": {
        "command": "uv",
        "args": ["run", os.path.join(current_dir, "mysql_mcp_server.py")],
        "transport": "stdio",
    },
    "file": {
        "command": "uv",
        "args": ["run", os.path.join(current_dir, "file_mcp_server.py")],
        "transport": "stdio",
    }
}

# Funzioni per la gestione dei processi MCP
def register_mcp_process(process):
    """Registra un processo MCP per la pulizia"""
    global mcp_processes
    mcp_processes.append(process)
    logger.info(f"Registered MCP process PID: {process.pid}")

def cleanup_processes():
    """Termina tutti i processi MCP"""
    global mcp_processes, shutdown_flag
    if shutdown_flag:
        return
        
    shutdown_flag = True
    logger.info("Cleaning up MCP processes...")
    
    for process in mcp_processes:
        try:
            if process and process.poll() is None:  # Processo ancora in esecuzione
                logger.info(f"Terminating MCP process PID: {process.pid}")
                process.terminate()
                
                # Aspetta un po' per la terminazione graceful
                try:
                    process.wait(timeout=5)
                    logger.info(f"MCP process PID {process.pid} terminated gracefully")
                except:
                    # Se non si termina, forza la terminazione
                    logger.warning(f"Force killing MCP process PID: {process.pid}")
                    process.kill()
                    try:
                        process.wait(timeout=2)
                        logger.info(f"MCP process PID {process.pid} force killed")
                    except:
                        logger.error(f"Failed to kill MCP process PID: {process.pid}")
        except Exception as e:
            logger.error(f"Error terminating process: {e}")
    
    mcp_processes.clear()
    logger.info("MCP processes cleanup completed")

def signal_handler(sig, frame):
    """Gestisce i segnali di terminazione"""
    logger.info(f"Received signal {sig}, shutting down...")
    cleanup_processes()
    sys.exit(0)

# Registra i signal handler e atexit
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
if hasattr(signal, 'SIGBREAK'):  # Windows
    signal.signal(signal.SIGBREAK, signal_handler)
atexit.register(cleanup_processes)

def get_llm_model():
    """Get the appropriate LLM model based on configuration"""
    if MODEL_PROVIDER.lower() == "ollama":
        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url="http://localhost:11434",  # Default Ollama URL
            temperature=0.7,
            top_p=0.9
        )
    else:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        return ChatOpenAI(model="gpt-4o")

# Function to run async code
def run_async(coroutine):
    global shutdown_flag
    if shutdown_flag:
        return {"error": "Server is shutting down"}
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

async def get_available_tools():
    """Get all available tools from all the servers"""
    try:
        logger.info("Getting available tools from all servers")
        # Create client for multiple MCP servers
        client = MultiServerMCPClient(servers)
        
        # Se il client ha un metodo per ottenere i processi, registrali
        if hasattr(client, '_sessions'):
            for session_name, session in client._sessions.items():
                if hasattr(session, '_process'):
                    register_mcp_process(session._process)
        
        tools = await client.get_tools()
        tool_info = []
        
        # Log retrieved tools
        logger.info(f"Retrieved {len(tools)} tools")
        for i, tool in enumerate(tools):
            logger.debug(f"Tool {i}: {tool.__class__.__name__} - {tool.name}")
            logger.debug(f"Tool {i} attributes: {dir(tool)}")
            
            # Extract available attributes safely
            tool_data = {
                "name": tool.name,
                "description": tool.description if hasattr(tool, 'description') else "No description available",
                # Since we don't have a server attribute, use the tool name to guess the server
                "server": "mysql" if "sql" in tool.name.lower() else "file"
            }
            tool_info.append(tool_data)
            
        return tool_info
    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}", exc_info=True)
        return []

async def process_query(query):
    """Process user query using multiple MCP servers"""
    try:
        logger.info(f"Processing query: {query}")
        model = get_llm_model()
        logger.info(f"Using model: {model.__class__.__name__}")

        # Create client for multiple MCP servers
        client = MultiServerMCPClient(servers)
        
        # Se il client ha un metodo per ottenere i processi, registrali
        if hasattr(client, '_sessions'):
            for session_name, session in client._sessions.items():
                if hasattr(session, '_process'):
                    register_mcp_process(session._process)
        
        # Get tools from all servers
        logger.info("Getting tools from all servers")
        tools = await client.get_tools()
        logger.info(f"Retrieved {len(tools)} tools")

        # Create and run the agent
        logger.info("Creating agent")
        agent = create_react_agent(model, tools)

        # Convert string query to proper format
        logger.info("Preparing messages")
        messages = [{"role": "user", "content": query}]

        logger.info("Invoking agent")
        agent_response = await agent.ainvoke({"messages": messages})
        logger.info("Agent response received")

        # Track tool usage
        tool_usage = []
        final_answer = None

        if "messages" in agent_response:
            messages = agent_response["messages"]
            logger.info(f"Response contains {len(messages)} messages")

            for i, msg in enumerate(messages):
                msg_type = msg.__class__.__name__
                logger.debug(f"Message {i}: {msg_type}")

                # Get tool calls
                if msg_type == "AIMessage" and hasattr(msg, 'tool_calls') and msg.tool_calls:
                    logger.info(f"Found tool calls in message {i}: {len(msg.tool_calls)}")
                    for tool_call in msg.tool_calls:
                        # Store the tool call
                        tool_data = {
                            "tool": tool_call.get('name', 'unknown'),
                            "args": tool_call.get('args', {})
                        }
                        tool_usage.append(tool_data)
                        logger.debug(f"Added tool usage: {tool_data}")

                # Get tool responses
                if msg_type == "ToolMessage" and hasattr(msg, 'content'):
                    # Add the tool response to the most recent tool call
                    if tool_usage and 'result' not in tool_usage[-1]:
                        tool_usage[-1]['result'] = msg.content
                        logger.debug(f"Added result to tool")

                # Get the final AI answer
                if i == len(messages) - 1 and msg_type == "AIMessage":
                    final_answer = msg.content
                    logger.info(f"Final answer captured")
        else:
            logger.warning("No messages in response")
            logger.debug(f"Response keys: {agent_response.keys()}")

        return {
            "final_answer": final_answer if final_answer else "No answer was generated.",
            "tool_usage": tool_usage
        }
    except Exception as e:
        logger.error(f"Error in process_query: {str(e)}", exc_info=True)
        return {
            "final_answer": f"Error processing your request: {str(e)}",
            "tool_usage": []
        }


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Return list of available tools from all servers"""
    logger.info("API request: GET /api/tools")
    try:
        tools = run_async(get_available_tools())
        logger.info(f"Returning {len(tools)} tools")
        return jsonify(tools)
    except Exception as e:
        logger.error(f"Error in get_tools route: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Return list of available MCP servers"""
    logger.info("API request: GET /api/servers")
    try:
        logger.info(f"Returning {len(servers)} servers")
        return jsonify(servers)
    except Exception as e:
        logger.error(f"Error in get_servers route: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/add_server', methods=['POST'])
def add_server():
    """Add a new MCP server to the servers dictionary"""
    logger.info("API request: POST /api/add_server")
    try:
        data = request.json
        if not data:
            logger.warning("No data provided in add_server request")
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        name = data.get('name', '').lower()
        config = data.get('config', {})
        
        # Validate required fields
        if not name:
            logger.warning("Server name is required")
            return jsonify({"success": False, "error": "Server name is required"}), 400
            
        if not config:
            logger.warning("Server configuration is required")
            return jsonify({"success": False, "error": "Server configuration is required"}), 400
            
        if not config.get('command'):
            logger.warning("Command is required")
            return jsonify({"success": False, "error": "Command is required"}), 400
            
        if not config.get('args') or not isinstance(config['args'], list) or not config['args']:
            logger.warning("Args must be a non-empty list")
            return jsonify({"success": False, "error": "Args must be a non-empty list"}), 400
            
        if not config.get('transport'):
            logger.warning("Transport is required")
            return jsonify({"success": False, "error": "Transport is required"}), 400
        
        # Check if server with this name already exists
        if name in servers:
            logger.warning(f"Server '{name}' already exists")
            return jsonify({"success": False, "error": f"Server '{name}' already exists"}), 400
        
        # Add the new server
        servers[name] = {
            "command": config['command'],
            "args": config['args'],
            "transport": config['transport']
        }
        
        logger.info(f"Added new server: {name} with config: {servers[name]}")
        
        return jsonify({"success": True, "message": f"Server '{name}' added successfully"})
    except Exception as e:
        logger.error(f"Error in add_server: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/')
def index():
    # Serve the main template
    return render_template('index.html')

# Process query endpoint
@app.route('/api/process_query', methods=['POST'])
def process_query_route():
    """Process a user query and return the result"""
    logger.info("API request: POST /api/process_query")
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            logger.warning("Query is required")
            return jsonify({"error": "Query is required"}), 400
            
        logger.info(f"Processing query via /api/process_query: {query}")
        result = run_async(process_query(query))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in process_query_route: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# Keep the /api/calculate endpoint for backward compatibility
@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Legacy endpoint for processing queries (kept for backward compatibility)"""
    logger.info("API request: POST /api/calculate")
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            logger.warning("Query is required")
            return jsonify({"error": "Query is required"}), 400
            
        logger.info(f"Processing query via /api/calculate: {query}")
        # Process query
        result = run_async(process_query(query))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in calculate: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    
    # Log server startup
    logger.info("Starting MCP Client Backend Server")
    logger.info(f"Model Provider: {MODEL_PROVIDER}")
    if MODEL_PROVIDER.lower() == "ollama":
        logger.info(f"Ollama Model: {OLLAMA_MODEL}")
    logger.info(f"Available servers: {list(servers.keys())}")
    
    # Run the Flask app
    logger.info(f"Starting Flask server on port {FLASK_PORT}...")
    app.run(debug=True, host='0.0.0.0', port=FLASK_PORT)