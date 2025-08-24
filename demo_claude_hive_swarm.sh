#!/bin/bash

# Demo Script for Claude Hive Swarm Integration
# Shows the enhanced Claude Code capabilities with collective intelligence

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🧠🐛 Claude Hive Swarm Integration Demo${NC}"
echo "======================================="
echo ""

echo -e "${GREEN}What you're about to see:${NC}"
echo "🚀 Enhanced Claude Code with collective AI intelligence"
echo "🧠 Hive mind decision-making across multiple expert agents"
echo "🐛 Swarm coordination for complex task execution"
echo "💾 Persistent collective memory that learns and grows"
echo ""

echo -e "${BLUE}Available Commands After Installation:${NC}"
echo ""
echo -e "${YELLOW}claude hive swarm${NC}   - Full collective intelligence"
echo "  └─ Combines strategic hive planning with swarm execution"
echo "  └─ Best for: Complex projects, full-stack development"
echo ""
echo -e "${YELLOW}claude hive${NC}         - Hive intelligence only"  
echo "  └─ Collective decision-making and persistent memory"
echo "  └─ Best for: Strategic decisions, research, knowledge building"
echo ""
echo -e "${YELLOW}claude swarm${NC}        - Swarm coordination only"
echo "  └─ Multi-agent task coordination and parallel execution"
echo "  └─ Best for: Implementation tasks, code reviews, optimization"
echo ""
echo -e "${YELLOW}claude${NC}              - Standard Claude Code (unchanged)"
echo "  └─ Your familiar single-agent experience"
echo ""

echo -e "${MAGENTA}🎯 Example Workflows:${NC}"
echo ""

echo -e "${GREEN}1. Building a Secure API${NC}"
echo "   Command: ${YELLOW}claude hive swarm${NC}"
echo "   In Claude Code: 'Help me build a secure REST API for my e-commerce platform'"
echo "   Result: Coordinated solution from backend, security, and performance experts"
echo ""

echo -e "${GREEN}2. Architecture Decisions${NC}"
echo "   Command: ${YELLOW}claude hive${NC}"
echo "   In Claude Code: 'Should I use microservices or monolith for my chat app?'"
echo "   Result: Collective decision from multiple architecture experts"
echo ""

echo -e "${GREEN}3. Code Optimization${NC}"
echo "   Command: ${YELLOW}claude swarm${NC}"
echo "   In Claude Code: 'Optimize this React component for performance'"
echo "   Result: Parallel analysis from React, performance, and testing experts"
echo ""

echo -e "${BLUE}🛠️ Installation Options:${NC}"
echo ""
echo "Option 1 - Full Installation:"
echo "  ${YELLOW}./scripts/install-claude-hive-swarm.sh${NC}"
echo ""
echo "Option 2 - Just Add to PATH:"
echo "  ${YELLOW}export PATH=\"$(pwd)/bin:\$PATH\"${NC}"
echo "  ${YELLOW}echo 'export PATH=\"$(pwd)/bin:\$PATH\"' >> ~/.bashrc${NC}"
echo ""

echo -e "${CYAN}🎮 Interactive Demo${NC}"
echo "=================="
echo ""

# Check if user wants to run interactive demo
read -p "Would you like to run the interactive demo? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🚀 Starting interactive demo...${NC}"
    echo ""
    
    # Ensure integration is running
    echo "1. Starting swarm-hive integration..."
    ./scripts/start-swarm-hive.sh start
    echo ""
    
    # Add to PATH for this session
    export PATH="$(pwd)/bin:$PATH"
    
    echo "2. Testing MCP server..."
    if python3 mcp_server/swarm_hive_mcp.py &
    local mcp_pid=$!
    sleep 2
    
    echo -e "${GREEN}✅ MCP server running (PID: $mcp_pid)${NC}"
    echo ""
    
    echo "3. Available commands:"
    ./bin/claude help
    echo ""
    
    echo -e "${YELLOW}🎯 Ready to test! Try these commands:${NC}"
    echo "  ./bin/claude hive swarm"
    echo "  ./bin/claude hive"
    echo "  ./bin/claude swarm"
    echo ""
    
    # Clean up background process
    kill $mcp_pid 2>/dev/null || true
    
    echo -e "${GREEN}🎉 Demo complete! Your claude hive swarm integration is ready.${NC}"
    echo ""
    echo "To make it permanent, restart your terminal or run:"
    echo "  source ~/.bashrc"
    echo ""
else
    echo -e "${YELLOW}Demo skipped. To install manually:${NC}"
    echo "  ./scripts/install-claude-hive-swarm.sh"
fi

echo ""
echo -e "${CYAN}🚀 What's Next?${NC}"
echo "==============="
echo ""
echo "1. Run: ${YELLOW}claude hive swarm${NC}"
echo "2. In Claude Code, try: ${YELLOW}'Create a development swarm and help me build a secure API'${NC}"
echo "3. Watch as multiple AI agents coordinate to solve your task!"
echo ""
echo -e "${MAGENTA}You now have collective AI intelligence at your fingertips! 🧠🐛${NC}"