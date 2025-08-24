#!/bin/bash

# Install Claude Hive Swarm Integration
# This script sets up the enhanced claude command with swarm-hive capabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLAUDE_WRAPPER="$PROJECT_ROOT/bin/claude"

echo -e "${CYAN}🧠🐛 Installing Claude Hive Swarm Integration${NC}"
echo "=============================================="
echo ""

# Function to detect shell and config file
detect_shell_config() {
    if [[ -n "$ZSH_VERSION" ]]; then
        echo "$HOME/.zshrc"
    elif [[ -n "$BASH_VERSION" ]]; then
        if [[ -f "$HOME/.bash_profile" ]]; then
            echo "$HOME/.bash_profile"
        else
            echo "$HOME/.bashrc"
        fi
    else
        echo "$HOME/.profile"
    fi
}

# Function to check if claude is already installed
check_existing_claude() {
    local claude_path
    claude_path=$(which claude 2>/dev/null || echo "")
    
    if [[ -n "$claude_path" ]]; then
        echo -e "${GREEN}✅ Found existing Claude Code installation: $claude_path${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Claude Code not found in PATH${NC}"
        echo "   You can still use the enhanced command, but you'll need to install Claude Code separately."
        return 1
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    
    # Check if dependencies are already installed
    if python3 -c "import structlog, yaml, numpy, prometheus_client" 2>/dev/null; then
        echo -e "${GREEN}✅ Dependencies already installed${NC}"
        return 0
    fi
    
    # Install dependencies
    if command -v pip3 &> /dev/null; then
        pip3 install structlog prometheus_client pyyaml numpy
        echo -e "${GREEN}✅ Dependencies installed${NC}"
    else
        echo -e "${RED}❌ pip3 not found. Please install Python dependencies manually:${NC}"
        echo "   pip3 install structlog prometheus_client pyyaml numpy"
        return 1
    fi
}

# Function to add to PATH
add_to_path() {
    local shell_config
    shell_config=$(detect_shell_config)
    local bin_dir="$PROJECT_ROOT/bin"
    
    echo -e "${BLUE}🔗 Adding to PATH in $shell_config...${NC}"
    
    # Check if already in PATH
    if echo "$PATH" | grep -q "$bin_dir"; then
        echo -e "${GREEN}✅ Already in PATH${NC}"
        return 0
    fi
    
    # Add to shell config
    echo "" >> "$shell_config"
    echo "# AgentNativeFramework Claude Hive Swarm Integration" >> "$shell_config"
    echo "export PATH=\"$bin_dir:\$PATH\"" >> "$shell_config"
    echo "" >> "$shell_config"
    
    # Update current session
    export PATH="$bin_dir:$PATH"
    
    echo -e "${GREEN}✅ Added to PATH${NC}"
    echo -e "${YELLOW}   Please restart your terminal or run: source $shell_config${NC}"
}

# Function to create desktop shortcut (macOS)
create_desktop_shortcut() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}🖥️  Creating desktop shortcut (macOS)...${NC}"
        
        local app_dir="/Applications"
        local shortcut_path="$app_dir/Claude Hive Swarm.app"
        
        # Create simple app bundle
        mkdir -p "$shortcut_path/Contents/MacOS"
        mkdir -p "$shortcut_path/Contents/Resources"
        
        # Create Info.plist
        cat > "$shortcut_path/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>claude-hive-swarm</string>
    <key>CFBundleIdentifier</key>
    <string>com.anthropic.claude-hive-swarm</string>
    <key>CFBundleName</key>
    <string>Claude Hive Swarm</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF
        
        # Create executable
        cat > "$shortcut_path/Contents/MacOS/claude-hive-swarm" << EOF
#!/bin/bash
cd "$HOME"
"$CLAUDE_WRAPPER" hive swarm
EOF
        
        chmod +x "$shortcut_path/Contents/MacOS/claude-hive-swarm"
        
        echo -e "${GREEN}✅ Desktop shortcut created: $shortcut_path${NC}"
    fi
}

# Function to test installation
test_installation() {
    echo -e "${BLUE}🧪 Testing installation...${NC}"
    
    # Test if claude command works
    if command -v claude &> /dev/null; then
        echo -e "${GREEN}✅ Claude command available${NC}"
        
        # Test swarm-hive integration
        if "$CLAUDE_WRAPPER" --help > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Swarm-Hive integration working${NC}"
            return 0
        else
            echo -e "${RED}❌ Swarm-Hive integration test failed${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Claude command not available${NC}"
        echo "   The installation completed, but you may need to restart your terminal"
        return 1
    fi
}

# Function to show usage instructions
show_usage() {
    echo ""
    echo -e "${GREEN}🎉 Installation Complete!${NC}"
    echo "======================="
    echo ""
    echo -e "${CYAN}Available Commands:${NC}"
    echo "  ${YELLOW}claude hive swarm${NC}       - Start Claude Code with full collective intelligence"
    echo "  ${YELLOW}claude hive${NC}             - Start Claude Code with hive intelligence only"  
    echo "  ${YELLOW}claude swarm${NC}            - Start Claude Code with swarm coordination only"
    echo "  ${YELLOW}claude${NC}                  - Standard Claude Code (unchanged)"
    echo ""
    echo -e "${BLUE}🚀 Try it now:${NC}"
    echo "  ${YELLOW}claude hive swarm${NC}"
    echo ""
    echo -e "${MAGENTA}What you get:${NC}"
    echo "  🧠 Collective decision making with multiple AI agents"
    echo "  🐛 Swarm coordination for complex task execution"
    echo "  💾 Persistent collective memory across sessions"
    echo "  🤝 Multi-agent collaboration on your coding tasks"
    echo "  📊 Real-time coordination and progress tracking"
    echo ""
    echo -e "${GREEN}Example workflow:${NC}"
    echo '  1. Type: claude hive swarm'
    echo '  2. In Claude Code, ask: "Help me build a secure API"'
    echo '  3. Claude will coordinate with security, backend, and performance agents'
    echo '  4. Get comprehensive solutions from collective AI intelligence'
    echo ""
}

# Main installation process
main() {
    echo "Starting installation..."
    echo ""
    
    # Step 1: Check existing Claude installation
    check_existing_claude
    echo ""
    
    # Step 2: Install Python dependencies
    install_dependencies
    echo ""
    
    # Step 3: Add to PATH
    add_to_path
    echo ""
    
    # Step 4: Create desktop shortcut (optional)
    if [[ "${1:-}" != "--no-shortcut" ]]; then
        create_desktop_shortcut
        echo ""
    fi
    
    # Step 5: Test installation
    if test_installation; then
        echo ""
        show_usage
    else
        echo ""
        echo -e "${YELLOW}⚠️  Installation completed with warnings${NC}"
        echo "   Please restart your terminal and try: claude hive swarm"
    fi
    
    # Step 6: Offer to start integration now
    echo ""
    read -p "Would you like to start Claude Hive Swarm now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}🚀 Starting Claude Hive Swarm...${NC}"
        exec "$CLAUDE_WRAPPER" hive swarm
    fi
}

# Handle command line arguments
case "${1:-}" in
    "--help"|"-h")
        echo "Usage: $0 [--no-shortcut]"
        echo ""
        echo "Options:"
        echo "  --no-shortcut    Skip desktop shortcut creation"
        echo "  --help, -h       Show this help"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac