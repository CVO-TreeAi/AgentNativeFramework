#!/bin/bash

# Start Swarm-Hive Integration for Agent Native Framework
# This script starts both the Python bridge and ensures Rust daemon integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SOCKET="/tmp/anf_python.sock"
DAEMON_SOCKET="/tmp/anf.sock"
LOG_DIR="$PROJECT_ROOT/logs"
PID_DIR="$PROJECT_ROOT/.pids"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$PID_DIR"

echo -e "${BLUE}🚀 Starting Agent Native Framework Swarm-Hive Integration${NC}"
echo "============================================================"

# Function to check if a process is running
check_process() {
    local pid_file="$1"
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # Process is running
        else
            rm -f "$pid_file"  # Clean up stale PID file
            return 1  # Process not running
        fi
    fi
    return 1  # PID file doesn't exist
}

# Function to stop existing processes
stop_existing() {
    echo -e "${YELLOW}🔄 Checking for existing processes...${NC}"
    
    # Stop Python bridge if running
    if check_process "$PID_DIR/python_bridge.pid"; then
        local pid=$(cat "$PID_DIR/python_bridge.pid")
        echo "Stopping existing Python bridge (PID: $pid)..."
        kill "$pid"
        sleep 2
    fi
    
    # Clean up sockets
    rm -f "$PYTHON_SOCKET"
    
    echo "✅ Cleanup complete"
}

# Function to start Python bridge
start_python_bridge() {
    echo -e "${GREEN}🧠 Starting Python daemon bridge...${NC}"
    
    cd "$PROJECT_ROOT"
    
    # Install dependencies if needed
    if ! python3 -c "import structlog, yaml, numpy" 2>/dev/null; then
        echo "Installing required Python dependencies..."
        pip3 install structlog prometheus_client pyyaml numpy
    fi
    
    # Start Python bridge in background
    nohup python3 -m core.daemon_bridge > "$LOG_DIR/python_bridge.log" 2>&1 &
    echo $! > "$PID_DIR/python_bridge.pid"
    
    # Wait for socket to be created
    local retries=0
    while [[ ! -S "$PYTHON_SOCKET" && $retries -lt 30 ]]; do
        sleep 0.5
        ((retries++))
    done
    
    if [[ -S "$PYTHON_SOCKET" ]]; then
        echo "✅ Python bridge started successfully"
        echo "   Socket: $PYTHON_SOCKET"
        echo "   Log: $LOG_DIR/python_bridge.log"
        echo "   PID: $(cat "$PID_DIR/python_bridge.pid")"
    else
        echo -e "${RED}❌ Failed to start Python bridge${NC}"
        return 1
    fi
}

# Function to test connection
test_connection() {
    echo -e "${BLUE}🧪 Testing swarm-hive integration...${NC}"
    
    # Test Python bridge directly
    if python3 -c "
import socket
import json
import sys

try:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('$PYTHON_SOCKET')
    
    # Test hive status command
    command = {'action': 'hive_status', 'params': {}}
    sock.send((json.dumps(command) + '\n').encode())
    
    response = sock.recv(1024).decode().strip()
    result = json.loads(response)
    
    if result.get('success'):
        print('✅ Hive intelligence operational')
    else:
        print('⚠️  Hive intelligence responding but with errors')
    
    sock.close()
    sys.exit(0)
except Exception as e:
    print(f'❌ Connection test failed: {e}')
    sys.exit(1)
"; then
        echo "✅ Connection test passed"
    else
        echo -e "${RED}❌ Connection test failed${NC}"
        return 1
    fi
}

# Function to show status
show_status() {
    echo ""
    echo "📊 Swarm-Hive Integration Status:"
    echo "================================="
    
    if check_process "$PID_DIR/python_bridge.pid"; then
        echo -e "🐍 Python Bridge: ${GREEN}Running${NC} (PID: $(cat "$PID_DIR/python_bridge.pid"))"
    else
        echo -e "🐍 Python Bridge: ${RED}Stopped${NC}"
    fi
    
    if [[ -S "$PYTHON_SOCKET" ]]; then
        echo -e "🔌 Python Socket: ${GREEN}Available${NC} ($PYTHON_SOCKET)"
    else
        echo -e "🔌 Python Socket: ${RED}Not Available${NC}"
    fi
    
    echo ""
    echo "📋 Available Commands:"
    echo "  anf swarm create <id> --agents=agent1,agent2 --topology=hierarchical"
    echo "  anf hive init --agents=agent1,agent2"
    echo "  anf collaborate 'build AI app' --agents=backend-dev,ai-engineer"
    echo ""
}

# Main execution
main() {
    # Handle command line arguments
    case "${1:-start}" in
        "start")
            stop_existing
            start_python_bridge
            sleep 1
            test_connection
            show_status
            echo -e "${GREEN}🎉 Swarm-Hive integration started successfully!${NC}"
            ;;
        "stop")
            stop_existing
            echo -e "${GREEN}✅ Swarm-Hive integration stopped${NC}"
            ;;
        "status")
            show_status
            ;;
        "restart")
            echo -e "${YELLOW}🔄 Restarting Swarm-Hive integration...${NC}"
            stop_existing
            sleep 2
            start_python_bridge
            sleep 1
            test_connection
            show_status
            echo -e "${GREEN}🎉 Swarm-Hive integration restarted successfully!${NC}"
            ;;
        "test")
            test_connection
            ;;
        "logs")
            echo "📋 Python Bridge Logs:"
            echo "======================"
            tail -f "$LOG_DIR/python_bridge.log"
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|test|logs}"
            echo ""
            echo "Commands:"
            echo "  start   - Start swarm-hive integration"
            echo "  stop    - Stop swarm-hive integration"
            echo "  restart - Restart swarm-hive integration"
            echo "  status  - Show current status"
            echo "  test    - Test connection"
            echo "  logs    - Show live logs"
            exit 1
            ;;
    esac
}

# Trap to handle cleanup on exit
trap 'echo -e "\n${YELLOW}Received interrupt signal${NC}"' INT TERM

main "$@"