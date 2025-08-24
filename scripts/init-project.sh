#!/bin/bash

# AgentNativeFramework Project Initialization Script
# Initializes new projects with appropriate agent configurations

set -e

# Default values
PROJECT_TYPE=""
PROJECT_NAME=""
OUTPUT_DIR="."
VERBOSE=false

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 --type <project_type> --name <project_name> [options]

Project Types:
  treeai      TreeAI/Forestry business systems with AFISS assessments
  ios         iOS/Swift native development with Claude integration  
  nextjs      Next.js/Convex SaaS platforms with real-time backend
  multi-agent CrewAI orchestration and multi-agent systems
  research    Research projects with academic and technical analysis
  general     General-purpose development with adaptive agents

Options:
  --type, -t      Project type (required)
  --name, -n      Project name (required)
  --output, -o    Output directory (default: current directory)
  --verbose, -v   Verbose output
  --help, -h      Show this help message

Examples:
  $0 --type treeai --name "MyTreeBusiness"
  $0 --type ios --name "MyiOSApp" --output ~/Projects
  $0 --type nextjs --name "MySaaSApp" --verbose
  $0 --type multi-agent --name "MyAgentSystem"

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        -n|--name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$PROJECT_TYPE" ]]; then
    print_error "Project type is required"
    show_usage
    exit 1
fi

if [[ -z "$PROJECT_NAME" ]]; then
    print_error "Project name is required"
    show_usage
    exit 1
fi

# Validate project type
case $PROJECT_TYPE in
    treeai|ios|nextjs|multi-agent|research|general)
        ;;
    *)
        print_error "Invalid project type: $PROJECT_TYPE"
        show_usage
        exit 1
        ;;
esac

# Create project directory
PROJECT_DIR="$OUTPUT_DIR/$PROJECT_NAME"
print_status "Creating project directory: $PROJECT_DIR"

if [[ -d "$PROJECT_DIR" ]]; then
    print_warning "Project directory already exists"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Project initialization cancelled"
        exit 1
    fi
else
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Initialize base project structure
print_status "Setting up base project structure..."

mkdir -p {agents,config,docs,scripts,logs,tools}
mkdir -p agents/{active,configs,memory}
mkdir -p config/{environments,quality-gates,coordination}
mkdir -p docs/{design,api,user-guides}
mkdir -p logs/{agents,system,coordination}

# Create base configuration files
print_status "Creating base configuration files..."

# Create .env template
cat > .env.example << 'EOF'
# AgentNativeFramework Environment Configuration

# Claude API Configuration
ANTHROPIC_API_KEY=your_claude_api_key_here

# Project Configuration
PROJECT_NAME=
PROJECT_TYPE=
ENVIRONMENT=development

# Agent Configuration
MAX_CONCURRENT_AGENTS=8
DEFAULT_MODEL=claude-sonnet-4
ENABLE_FULL_CONTEXT=true
MAX_TOKENS=200000

# Logging
LOG_LEVEL=INFO
ENABLE_AGENT_LOGGING=true
ENABLE_COORDINATION_LOGGING=true

# Quality Gates
MINIMUM_QUALITY_THRESHOLD=0.8
ENABLE_DEMOCRATIC_COORDINATION=true
ESCALATION_THRESHOLD=0.85
EOF

# Create project-specific configurations based on type
print_status "Configuring for project type: $PROJECT_TYPE"

case $PROJECT_TYPE in
    treeai)
        setup_treeai_project
        ;;
    ios)
        setup_ios_project
        ;;
    nextjs)
        setup_nextjs_project
        ;;
    multi-agent)
        setup_multi_agent_project
        ;;
    research)
        setup_research_project
        ;;
    general)
        setup_general_project
        ;;
esac

# Create project README
create_project_readme

# Create initialization scripts
create_project_scripts

# Set up git repository
setup_git_repository

print_success "Project '$PROJECT_NAME' initialized successfully!"
print_status "Next steps:"
echo "  1. cd $PROJECT_DIR"
echo "  2. Copy .env.example to .env and configure your API keys"
echo "  3. Run ./scripts/setup.sh to complete initialization"
echo "  4. Run ./scripts/start-agents.sh to begin development"

# Function implementations

setup_treeai_project() {
    print_status "Setting up TreeAI/Forestry project configuration..."
    
    # TreeAI specific directories
    mkdir -p {business,assessments,pricing,reports}
    mkdir -p business/{workflows,calculations,integrations}
    mkdir -p assessments/{afiss,treescore,risk-analysis}
    mkdir -p pricing/{pph,competitive,optimization}
    
    # TreeAI agent configuration
    cat > config/agents.yaml << 'EOF'
project_type: treeai
primary_agents:
  - tree_analysis_specialist
  - forestry_business_analyst
  - pricing_optimization_agent
  - business_analyst

secondary_agents:
  - ai_engineer
  - data_analyst
  - report_generator
  - quality_auditor

agent_coordination:
  patterns:
    - forestry_business_workflow
    - assessment_to_pricing_pipeline
    - quality_assurance_gates
  
specialized_tools:
  - afiss_assessment_calculator
  - treescore_formula_engine
  - pph_pricing_optimizer
  - docs_workflow_manager
EOF

    # Add TreeAI specific environment variables
    cat >> .env.example << 'EOF'

# TreeAI Specific Configuration
ENABLE_AFISS_ASSESSMENTS=true
TREESCORE_CALCULATION_MODE=advanced
PPH_PRICING_MODEL=dynamic
DOCS_WORKFLOW_INTEGRATION=true

# Business Intelligence
ENABLE_COMPETITIVE_ANALYSIS=true
PRICING_OPTIMIZATION_LEVEL=maximum
RISK_ASSESSMENT_DEPTH=comprehensive
EOF

    # Create TreeAI project documentation
    cat > docs/TREEAI_SETUP.md << 'EOF'
# TreeAI Project Setup

This project is configured for TreeAI/Forestry business operations with AI-powered assessments and pricing.

## Key Components

### AFISS Assessments
- Automated tree assessment protocols
- Risk factor calculations
- Condition scoring systems

### PpH Pricing
- Per-hour pricing calculations
- Dynamic pricing optimization
- Competitive analysis integration

### DOCS Workflow
- LEAD → PROPOSAL → WORK ORDER → INVOICE
- Automated workflow management
- Business process optimization

## Primary Agents

- **tree_analysis_specialist**: AI-powered tree assessments
- **forestry_business_analyst**: Business operations optimization
- **pricing_optimization_agent**: Dynamic pricing strategies

## Getting Started

1. Configure AFISS assessment parameters
2. Set up pricing calculation rules
3. Initialize DOCS workflow integration
4. Activate forestry business intelligence agents
EOF
}

setup_ios_project() {
    print_status "Setting up iOS/Swift project configuration..."
    
    # iOS specific directories
    mkdir -p {ios,swift-packages,resources,ui-designs}
    mkdir -p ios/{views,models,services,extensions}
    mkdir -p swift-packages/{anthropic,utilities,networking}
    
    # iOS agent configuration
    cat > config/agents.yaml << 'EOF'
project_type: ios
primary_agents:
  - ios_developer
  - mobile_developer
  - ui_ux_designer
  - swift_architect

secondary_agents:
  - ai_engineer
  - security_auditor
  - performance_optimizer
  - app_store_specialist

agent_coordination:
  patterns:
    - mobile_development_workflow
    - ui_backend_integration
    - app_store_deployment_pipeline
  
specialized_tools:
  - swift_code_generator
  - swiftui_component_builder
  - anthropic_ios_integration
  - app_store_optimization
EOF

    # Add iOS specific environment variables
    cat >> .env.example << 'EOF'

# iOS Development Configuration
XCODE_PROJECT_NAME=
BUNDLE_IDENTIFIER=
DEVELOPMENT_TEAM_ID=
SWIFT_VERSION=5.9
IOS_DEPLOYMENT_TARGET=17.0

# Claude Integration
ENABLE_NATIVE_CLAUDE_INTEGRATION=true
CLAUDE_STREAMING_RESPONSES=true
KEYCHAIN_SERVICE_NAME=
EOF

    # Create iOS project documentation
    cat > docs/IOS_SETUP.md << 'EOF'
# iOS Project Setup

This project is configured for native iOS development with Claude integration.

## Architecture

### SwiftUI Modern Patterns
- @Observable for state management
- Async/await for concurrency
- Structured concurrency patterns

### Claude Integration
- SwiftAnthropic SDK integration
- Streaming response handling
- Secure API key management

## Primary Agents

- **ios_developer**: Native Swift/SwiftUI development
- **mobile_developer**: Cross-platform considerations
- **ui_ux_designer**: Apple Human Interface Guidelines

## Development Workflow

1. Design phase with UI/UX agents
2. Implementation with iOS development agents
3. Integration testing with security audit
4. App Store deployment with optimization
EOF
}

setup_nextjs_project() {
    print_status "Setting up Next.js/Convex project configuration..."
    
    # Next.js specific directories
    mkdir -p {frontend,backend,database,api}
    mkdir -p frontend/{components,pages,hooks,utils}
    mkdir -p backend/{convex,auth,services,middleware}
    
    # Next.js agent configuration
    cat > config/agents.yaml << 'EOF'
project_type: nextjs
primary_agents:
  - fullstack_developer
  - backend_architect
  - frontend_developer
  - database_optimizer

secondary_agents:
  - ui_ux_designer
  - security_auditor
  - performance_optimizer
  - api_designer

agent_coordination:
  patterns:
    - fullstack_development_workflow
    - real_time_backend_integration
    - authentication_security_pipeline
  
specialized_tools:
  - nextjs_app_router
  - convex_backend_functions
  - clerk_auth_integration
  - vercel_deployment
EOF

    # Add Next.js specific environment variables
    cat >> .env.example << 'EOF'

# Next.js Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_CONVEX_URL=
DATABASE_URL=

# Authentication
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=

# Real-time Backend
CONVEX_DEPLOYMENT_URL=
ENABLE_REAL_TIME_SYNC=true
EOF

    # Create Next.js project documentation  
    cat > docs/NEXTJS_SETUP.md << 'EOF'
# Next.js/Convex Project Setup

This project is configured for modern SaaS development with real-time capabilities.

## Architecture

### Vertical Slice Architecture
- Feature-based organization
- Shared components and utilities
- Clear separation of concerns

### Real-time Backend
- Convex for backend functions
- Real-time subscriptions
- Type-safe mutations and queries

## Primary Agents

- **fullstack_developer**: End-to-end development
- **backend_architect**: System design and APIs
- **database_optimizer**: Performance and scalability

## Development Workflow

1. Architecture planning with backend architect
2. Frontend/backend parallel development
3. Real-time integration and testing
4. Production deployment and optimization
EOF
}

setup_multi_agent_project() {
    print_status "Setting up Multi-Agent project configuration..."
    
    # Multi-agent specific directories
    mkdir -p {crews,orchestration,memory,coordination}
    mkdir -p crews/{development,research,business,operations}
    mkdir -p orchestration/{workflows,decision-making,handoffs}
    
    # Multi-agent configuration
    cat > config/agents.yaml << 'EOF'
project_type: multi_agent
primary_agents:
  - project_supervisor_orchestrator
  - agent_expert
  - mcp_expert
  - workflow_orchestrator

secondary_agents:
  - context_manager
  - quality_auditor
  - performance_optimizer
  - coordination_specialist

agent_coordination:
  patterns:
    - democratic_decision_making
    - hierarchical_orchestration
    - parallel_agent_coordination
  
specialized_tools:
  - crewai_orchestration
  - mcp_server_management
  - agent_memory_systems
  - democratic_voting_system
EOF

    # Add multi-agent specific environment variables
    cat >> .env.example << 'EOF'

# Multi-Agent System Configuration
MAX_PARALLEL_AGENTS=16
ENABLE_DEMOCRATIC_COORDINATION=true
AGENT_MEMORY_PERSISTENCE=true
COORDINATION_COMPLEXITY_THRESHOLD=0.8

# CrewAI Configuration
CREWAI_ORCHESTRATION_MODE=democratic
AGENT_HANDOFF_PROTOCOL=quality_gated
DECISION_CONSENSUS_THRESHOLD=0.7
EOF
}

setup_research_project() {
    print_status "Setting up Research project configuration..."
    
    # Research specific directories
    mkdir -p {literature,analysis,synthesis,reports}
    mkdir -p literature/{academic,technical,market}
    mkdir -p analysis/{quantitative,qualitative,statistical}
    
    # Research agent configuration
    cat > config/agents.yaml << 'EOF'
project_type: research
primary_agents:
  - research_orchestrator
  - academic_researcher
  - technical_researcher
  - data_analyst

secondary_agents:
  - research_synthesizer
  - report_generator
  - fact_checker
  - citation_manager

agent_coordination:
  patterns:
    - multi_phase_research_workflow
    - parallel_research_streams
    - synthesis_and_validation
EOF
}

setup_general_project() {
    print_status "Setting up General project configuration..."
    
    # General project configuration
    cat > config/agents.yaml << 'EOF'
project_type: general
primary_agents:
  - project_supervisor_orchestrator
  - general_purpose_agent
  - context_manager
  - quality_auditor

secondary_agents:
  - code_reviewer
  - documentation_generator
  - testing_specialist
  - deployment_manager

agent_coordination:
  patterns:
    - adaptive_workflow
    - context_driven_coordination
    - quality_first_development
EOF
}

create_project_readme() {
    cat > README.md << EOF
# $PROJECT_NAME

A project built with the AgentNativeFramework - a unified agentic framework for seamless multi-project workflows.

## Project Type: $PROJECT_TYPE

This project is configured for $PROJECT_TYPE development with specialized agent coordination patterns.

## Quick Start

1. **Setup Environment**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

2. **Initialize Project**
   \`\`\`bash
   ./scripts/setup.sh
   \`\`\`

3. **Start Development**
   \`\`\`bash
   ./scripts/start-agents.sh
   \`\`\`

## Agent Configuration

This project uses the following primary agents:
- Configured based on project type: $PROJECT_TYPE
- See \`config/agents.yaml\` for detailed configuration
- Agent coordination patterns optimized for this project type

## Documentation

- [Project Setup](docs/$(echo $PROJECT_TYPE | tr '[:lower:]' '[:upper:]')_SETUP.md)
- [Agent Configuration](docs/AGENTS.md)
- [Development Workflow](docs/WORKFLOW.md)

## AgentNativeFramework

This project is powered by the AgentNativeFramework, providing:
- 300+ specialized agents
- Democratic coordination patterns
- Persistent learning and memory
- Seamless scaling across projects

For more information, see the [AgentNativeFramework documentation](https://github.com/[username]/AgentNativeFramework).
EOF
}

create_project_scripts() {
    print_status "Creating project management scripts..."
    
    # Setup script
    cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# Project setup script

set -e

echo "Setting up AgentNativeFramework project..."

# Check for required environment variables
if [[ ! -f .env ]]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "Please edit .env with your configuration before proceeding."
    exit 1
fi

# Source environment
source .env

# Validate required variables
if [[ -z "$ANTHROPIC_API_KEY" || "$ANTHROPIC_API_KEY" == "your_claude_api_key_here" ]]; then
    echo "Please set ANTHROPIC_API_KEY in .env"
    exit 1
fi

echo "Setup complete! Run ./scripts/start-agents.sh to begin development."
EOF

    # Start agents script
    cat > scripts/start-agents.sh << 'EOF'
#!/bin/bash
# Start the agent system for development

set -e

echo "Starting AgentNativeFramework agent system..."

# Source environment
source .env

# Create logs directory
mkdir -p logs/agents

# Start agent manager
echo "Initializing agent manager..."
python -c "
import sys
sys.path.append('.')
from core.agents.agent_manager import AgentManager
import asyncio

async def start_system():
    manager = AgentManager()
    print('Agent system ready!')
    print('Available agents:', list(manager.get_agent_registry().keys()))
    
asyncio.run(start_system())
"

echo "Agent system started successfully!"
EOF

    # Make scripts executable
    chmod +x scripts/*.sh
}

setup_git_repository() {
    print_status "Initializing git repository..."
    
    # Initialize git if not already initialized
    if [[ ! -d .git ]]; then
        git init
    fi
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Environment
.env
.env.local
*.key
api-keys/

# Agent logs and memory
logs/
agents/memory/
*.log

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/

# Node modules (if applicable)
node_modules/
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.build/
EOF

    # Initial commit
    git add .
    git commit -m "Initial project setup with AgentNativeFramework

Project type: $PROJECT_TYPE
Generated with AgentNativeFramework initialization script"
}