#!/bin/bash

# Agent Native Framework - Installation Script
# Terminal-native agent coordination system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║      █████╗ ██╗  ██╗███████╗    ████████╗███████╗██████╗ ███╗   ███╗    ║
    ║     ██╔══██╗██║ ██╔╝██╔════╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ║
    ║     ███████║█████╔╝ █████╗         ██║   █████╗  ██████╔╝██╔████╔██║    ║
    ║     ██╔══██║██╔═██╗ ██╔══╝         ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║    ║
    ║     ██║  ██║██║  ██╗██║            ██║   ███████╗██║  ██║██║ ╚═╝ ██║    ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝            ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝    ║
    ║                                                                          ║
    ║            Agent Native Framework - Terminal Agent System                ║
    ║                      Jarvis for Terminal Power Users                     ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
check_os() {
    log_info "Checking operating system compatibility..."
    
    case "$(uname -s)" in
        Darwin)
            OS="macos"
            log_success "macOS detected"
            ;;
        Linux)
            OS="linux"
            log_success "Linux detected"
            ;;
        *)
            log_error "Unsupported operating system: $(uname -s)"
            exit 1
            ;;
    esac
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check for Rust/Cargo
    if ! command -v cargo &> /dev/null; then
        log_warning "Rust not found. Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source ~/.cargo/env
        log_success "Rust installed successfully"
    else
        log_success "Rust found: $(cargo --version)"
    fi
    
    # Check for Git
    if ! command -v git &> /dev/null; then
        log_error "Git is required but not installed. Please install Git first."
        exit 1
    else
        log_success "Git found: $(git --version)"
    fi
    
    # Check for Python (for agent coordination)
    if ! command -v python3 &> /dev/null; then
        log_warning "Python 3 not found. Some features may be limited."
    else
        log_success "Python 3 found: $(python3 --version)"
    fi
}

# Create necessary directories
setup_directories() {
    log_info "Setting up directories..."
    
    local config_dir="$HOME/.anf"
    local data_dir="$HOME/.anf/data"
    local agents_dir="$HOME/.anf/agents"
    local workflows_dir="$HOME/.anf/workflows"
    local logs_dir="$HOME/.anf/logs"
    
    mkdir -p "$config_dir" "$data_dir" "$agents_dir" "$workflows_dir" "$logs_dir"
    
    log_success "Directories created:"
    log_success "  Config: $config_dir"
    log_success "  Data: $data_dir"
    log_success "  Agents: $agents_dir"
    log_success "  Workflows: $workflows_dir"
    log_success "  Logs: $logs_dir"
}

# Install ANF binaries
install_binaries() {
    log_info "Building and installing ANF binaries..."
    
    # Build the Rust components
    if cargo build --release; then
        log_success "ANF binaries built successfully"
    else
        log_error "Failed to build ANF binaries"
        exit 1
    fi
    
    # Install binaries to /usr/local/bin or ~/.cargo/bin
    if [[ "$OS" == "macos" ]] && [[ -w "/usr/local/bin" ]]; then
        cp target/release/anf /usr/local/bin/
        cp target/release/anfd /usr/local/bin/
        log_success "Binaries installed to /usr/local/bin/"
    elif [[ -d "$HOME/.cargo/bin" ]]; then
        cp target/release/anf ~/.cargo/bin/
        cp target/release/anfd ~/.cargo/bin/
        log_success "Binaries installed to ~/.cargo/bin/"
    else
        log_warning "Could not install binaries to system PATH. You may need to run them from target/release/"
    fi
}

# Create default configuration
create_config() {
    log_info "Creating default configuration..."
    
    local config_file="$HOME/.anf/config.toml"
    
    if [[ ! -f "$config_file" ]]; then
        cat > "$config_file" << 'EOF'
[daemon]
port = 8765
log_level = "info"
max_agents = 50
auto_start = true
socket_path = "/tmp/anf.sock"

[interface]
theme = "hacker"
colors = true
animations = true
prompt_style = "jarvis"

[hotkeys]
global_activate = "Ctrl+Shift+A"
quick_ask = "Ctrl+A, A"
spawn_menu = "Ctrl+A, S"
emergency_stop = "Ctrl+A, Ctrl+C"

[agents]
default_timeout = 300
auto_cleanup = true
favorite_agents = [
    "rust-expert",
    "fullstack-developer", 
    "security-auditor",
    "performance-optimizer"
]

[workflows]
auto_save = true
parallel_by_default = false
confirmation_required = ["deploy", "delete"]

[claude_code]
integration_enabled = true
auto_spawn_on_claude = true
preferred_agents = [
    "backend-typescript-architect",
    "react-pro",
    "python-backend-engineer"
]
EOF
        log_success "Default configuration created: $config_file"
    else
        log_info "Configuration file already exists: $config_file"
    fi
}

# Install Python dependencies (for agent coordination)
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if command -v python3 &> /dev/null; then
        # Install required Python packages
        python3 -m pip install --user anthropic pydantic PyYAML structlog prometheus-client 2>/dev/null || {
            log_warning "Failed to install Python dependencies. Some features may be limited."
        }
        log_success "Python dependencies installed"
    else
        log_warning "Skipping Python dependencies (Python not found)"
    fi
}

# Setup shell integration
setup_shell_integration() {
    log_info "Setting up shell integration..."
    
    local shell_config=""
    if [[ -f "$HOME/.zshrc" ]]; then
        shell_config="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        shell_config="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        shell_config="$HOME/.bash_profile"
    fi
    
    if [[ -n "$shell_config" ]]; then
        # Add ANF aliases and completions
        if ! grep -q "# ANF - Agent Native Framework" "$shell_config"; then
            cat >> "$shell_config" << 'EOF'

# ANF - Agent Native Framework
export ANF_CONFIG_DIR="$HOME/.anf"

# Quick aliases
alias a="anf ask"
alias anfs="anf spawn"
alias anfr="anf run"
alias anfl="anf agents list"
alias anfd-start="anfd --start --daemon"
alias anfd-stop="anfd --stop"
alias anfd-status="anfd --status"

# Global hotkey support (if terminal supports it)
# Ctrl+Shift+A to activate ANF
bind -x '"\C-\M-a": "anf quick"'

EOF
            log_success "Shell integration added to $shell_config"
            log_info "Run 'source $shell_config' or restart your terminal to activate"
        else
            log_info "Shell integration already exists in $shell_config"
        fi
    else
        log_warning "Could not detect shell configuration file for integration"
    fi
}

# Create systemd service (Linux) or launchd service (macOS)
setup_daemon_service() {
    log_info "Setting up daemon service..."
    
    case "$OS" in
        macos)
            local plist_file="$HOME/Library/LaunchAgents/com.anf.daemon.plist"
            cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anf.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which anfd || echo ~/.cargo/bin/anfd)</string>
        <string>--start</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/.anf/logs/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.anf/logs/daemon.error.log</string>
</dict>
</plist>
EOF
            log_success "macOS Launch Agent created: $plist_file"
            log_info "Run 'launchctl load $plist_file' to start the daemon automatically"
            ;;
            
        linux)
            local service_file="$HOME/.config/systemd/user/anf-daemon.service"
            mkdir -p "$(dirname "$service_file")"
            
            cat > "$service_file" << EOF
[Unit]
Description=Agent Native Framework Daemon
After=network.target

[Service]
Type=simple
ExecStart=$(which anfd || echo ~/.cargo/bin/anfd) --start --daemon
Restart=always
RestartSec=10
StandardOutput=file:$HOME/.anf/logs/daemon.log
StandardError=file:$HOME/.anf/logs/daemon.error.log

[Install]
WantedBy=default.target
EOF
            log_success "Systemd service created: $service_file"
            log_info "Run 'systemctl --user enable anf-daemon.service' to enable auto-start"
            ;;
    esac
}

# Test installation
test_installation() {
    log_info "Testing installation..."
    
    # Test if binaries exist and are executable
    if command -v anf &> /dev/null; then
        local version=$(anf --version 2>/dev/null || echo "unknown")
        log_success "anf command available: $version"
    else
        log_error "anf command not found in PATH"
        return 1
    fi
    
    if command -v anfd &> /dev/null; then
        log_success "anfd daemon available"
    else
        log_error "anfd daemon not found in PATH"
        return 1
    fi
    
    # Test configuration loading
    if [[ -f "$HOME/.anf/config.toml" ]]; then
        log_success "Configuration file exists"
    else
        log_error "Configuration file missing"
        return 1
    fi
    
    log_success "Installation test passed!"
}

# Show post-installation instructions
show_instructions() {
    echo
    echo -e "${GREEN}🎉 ANF Installation Complete!${NC}"
    echo
    echo -e "${CYAN}Quick Start:${NC}"
    echo -e "  ${YELLOW}anfd --start${NC}              Start the daemon"
    echo -e "  ${YELLOW}anf agents list${NC}           List available agents"
    echo -e "  ${YELLOW}anf ask \"hello world\"${NC}      Ask an agent"
    echo -e "  ${YELLOW}anf interactive${NC}           Enter interactive mode"
    echo
    echo -e "${CYAN}Power User Commands:${NC}"
    echo -e "  ${YELLOW}anf spawn rust-expert${NC}     Spawn a specific agent"
    echo -e "  ${YELLOW}anf dashboard${NC}             View system dashboard"
    echo -e "  ${YELLOW}anf context set .${NC}         Set current directory as context"
    echo
    echo -e "${CYAN}Keyboard Shortcuts (in interactive mode):${NC}"
    echo -e "  ${YELLOW}Ctrl+A, A${NC}                Quick ask"
    echo -e "  ${YELLOW}Ctrl+A, S${NC}                Spawn menu"
    echo -e "  ${YELLOW}Ctrl+A, L${NC}                List agents"
    echo
    echo -e "${CYAN}Configuration:${NC}"
    echo -e "  Config file: ${YELLOW}~/.anf/config.toml${NC}"
    echo -e "  Logs: ${YELLOW}~/.anf/logs/${NC}"
    echo -e "  Custom agents: ${YELLOW}~/.anf/agents/${NC}"
    echo
    echo -e "${BLUE}For more help: anf --help${NC}"
}

# Main installation function
main() {
    print_banner
    
    echo -e "${BLUE}Installing Agent Native Framework...${NC}"
    echo
    
    check_os
    check_dependencies
    setup_directories
    install_binaries
    create_config
    install_python_deps
    setup_shell_integration
    setup_daemon_service
    
    echo
    if test_installation; then
        show_instructions
        echo
        log_success "ANF has been successfully installed! 🚀"
        echo
        echo -e "${YELLOW}Next steps:${NC}"
        echo -e "1. Restart your terminal or run: ${CYAN}source ~/.zshrc${NC} (or ~/.bashrc)"
        echo -e "2. Start the daemon: ${CYAN}anfd --start${NC}"
        echo -e "3. Try it out: ${CYAN}anf ask 'What can you help me with?'${NC}"
    else
        log_error "Installation test failed. Please check the errors above."
        exit 1
    fi
}

# Run installation
main "$@"