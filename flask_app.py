from flask import Flask, render_template, request, jsonify
import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient


app = Flask(__name__)

# Get the absolute path to server scripts
current_dir = os.path.dirname(os.path.abspath(__file__))

servers = {
    "mysql": {
        "command": "python",
        "args": [os.path.join(current_dir, "mysql_mcp_server.py")],
        "transport": "stdio",
    },
    # "file": {
    #     "command": "python",
    #     "args": [os.path.join(current_dir, "file_mcp_server.py")],
    #     "transport": "stdio",
    # }
}

# Set a default API key or use environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Function to run async code
def run_async(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

async def get_available_tools():
    """Get all available tools from all the servers"""
    try:
        async with MultiServerMCPClient(servers) as client:
            # Get tools directly without awaiting
            tools = client.get_tools()
            tool_info = []
            
            # Debug information
            print(f"Retrieved {len(tools)} tools")
            for i, tool in enumerate(tools):
                print(f"Tool {i}: {tool.__class__.__name__} - {tool.name}")
                print(f"Tool {i} attributes: {dir(tool)}")
                
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
        print(f"Error getting tools: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

async def process_query(query):
    """Process user query using multiple MCP servers"""
    try:
        print(f"Processing query: {query}")
        model = ChatOpenAI(model="gpt-4o")
        
        async with MultiServerMCPClient(servers) as client:
            # Get tools from all servers
            print("Getting tools from all servers")
            tools = client.get_tools()
            print(f"Retrieved {len(tools)} tools")
            
            # Create and run the agent
            print("Creating agent")
            agent = create_react_agent(model, tools)
            
            # Convert string query to proper format
            print("Preparing messages")
            messages = [{"role": "user", "content": query}]
            
            print("Invoking agent")
            agent_response = await agent.ainvoke({"messages": messages})
            print("Agent response received")
            
            # Track tool usage
            tool_usage = []
            final_answer = None
            
            if "messages" in agent_response:
                messages = agent_response["messages"]
                print(f"Response contains {len(messages)} messages")
                
                for i, msg in enumerate(messages):
                    msg_type = msg.__class__.__name__
                    print(f"Message {i}: {msg_type}")
                    
                    # Get tool calls
                    if msg_type == "AIMessage" and hasattr(msg, 'tool_calls') and msg.tool_calls:
                        print(f"Found tool calls in message {i}: {len(msg.tool_calls)}")
                        for tool_call in msg.tool_calls:
                            # Store the tool call
                            tool_data = {
                                "tool": tool_call.get('name', 'unknown'),
                                "args": tool_call.get('args', {})
                            }
                            tool_usage.append(tool_data)
                            print(f"Added tool usage: {tool_data}")
                    
                    # Get tool responses
                    if msg_type == "ToolMessage" and hasattr(msg, 'content'):
                        # Add the tool response to the most recent tool call
                        if tool_usage and 'result' not in tool_usage[-1]:
                            tool_usage[-1]['result'] = msg.content
                            print(f"Added result to tool")
                    
                    # Get the final AI answer
                    if i == len(messages) - 1 and msg_type == "AIMessage":
                        final_answer = msg.content
                        print(f"Final answer captured")
            else:
                print("No messages in response")
                print(f"Response keys: {agent_response.keys()}")
            
            return {
                "final_answer": final_answer if final_answer else "No answer was generated.",
                "tool_usage": tool_usage
            }
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "final_answer": f"Error processing your request: {str(e)}",
            "tool_usage": []
        }

@app.route('/api/tools', methods=['GET'])
def get_tools():
    tools = run_async(get_available_tools())
    return jsonify(tools)

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Return list of available MCP servers"""
    return jsonify(servers)

@app.route('/api/add_server', methods=['POST'])
def add_server():
    """Add a new MCP server to the servers dictionary"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        name = data.get('name', '').lower()
        config = data.get('config', {})
        
        # Validate required fields
        if not name:
            return jsonify({"success": False, "error": "Server name is required"}), 400
            
        if not config:
            return jsonify({"success": False, "error": "Server configuration is required"}), 400
            
        if not config.get('command'):
            return jsonify({"success": False, "error": "Command is required"}), 400
            
        if not config.get('args') or not isinstance(config['args'], list) or not config['args']:
            return jsonify({"success": False, "error": "Args must be a non-empty list"}), 400
            
        if not config.get('transport'):
            return jsonify({"success": False, "error": "Transport is required"}), 400
        
        # Check if server with this name already exists
        if name in servers:
            return jsonify({"success": False, "error": f"Server '{name}' already exists"}), 400
        
        # Add the new server
        servers[name] = {
            "command": config['command'],
            "args": config['args'],
            "transport": config['transport']
        }
        
        print(f"Added new server: {name} with config: {servers[name]}")
        
        return jsonify({"success": True, "message": f"Server '{name}' added successfully"})
    except Exception as e:
        print(f"Error in add_server: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/')
def index():
    # Serve the main template
    return render_template('index.html')

# Process query endpoint
@app.route('/api/process_query', methods=['POST'])
def process_query_route():
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
            
        print(f"Processing query via /api/process_query: {query}")
        result = run_async(process_query(query))
        return jsonify(result)
    except Exception as e:
        print(f"Error in process_query_route: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Keep the /api/calculate endpoint for backward compatibility
@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
            
        print(f"Processing query via /api/calculate: {query}")
        # Process query
        result = run_async(process_query(query))
        return jsonify(result)
    except Exception as e:
        print(f"Error in calculate: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(current_dir, 'templates'), exist_ok=True)
    app.run(debug=True, port=5008) 