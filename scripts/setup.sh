#!/bin/bash

# AgentNativeFramework Setup Script
# Prepares the framework for development with all dependencies and configurations

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_status "Setting up AgentNativeFramework..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

print_success "Python 3 found: $(python3 --version)"

# Check for required directories
print_status "Ensuring directory structure..."
mkdir -p {core,adapters,agents,tools,scripts,docs,logs,config}
mkdir -p core/{agents,coordination,memory,workflow}
mkdir -p adapters/{treeai,ios,nextjs,multi-agent}
mkdir -p agents/{development,ai-ml,security,research,business}
mkdir -p config/{environments,quality-gates,coordination}
mkdir -p logs/{agents,system,coordination}

print_success "Directory structure verified"

# Create Python virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Create requirements.txt if it doesn't exist
if [[ ! -f "requirements.txt" ]]; then
    print_status "Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
# AgentNativeFramework Dependencies

# Core framework
anthropic>=0.8.0
asyncio-mqtt>=0.11.0
pydantic>=2.0.0
pyyaml>=6.0

# Agent coordination
aiofiles>=23.0.0
aiohttp>=3.8.0
websockets>=11.0.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0

# Logging and monitoring
structlog>=23.0.0
prometheus-client>=0.17.0

# Development tools
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0

# Optional: CrewAI for multi-agent systems
crewai>=0.1.0

# Optional: MCP server support
mcp>=0.1.0
EOF
    print_success "Requirements file created"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Python dependencies installed"

# Create environment file if it doesn't exist
if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        print_status "Creating .env from template..."
        cp .env.example .env
        print_warning "Please edit .env with your API keys and configuration"
    else
        print_status "Creating default .env file..."
        cat > .env << 'EOF'
# AgentNativeFramework Environment Configuration

# Claude API Configuration
ANTHROPIC_API_KEY=your_claude_api_key_here

# Framework Configuration
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
        print_warning "Please edit .env with your API keys and configuration"
    fi
fi

# Create core configuration files
print_status "Creating core configuration files..."

# Agent registry configuration
cat > config/agent_registry.yaml << 'EOF'
# AgentNativeFramework Agent Registry Configuration

agent_tiers:
  tier_1_core:
    description: "Core framework agents for orchestration and coordination"
    max_tokens: 200000
    default_model: "claude-opus-4"
    
  tier_2_specialists:
    description: "Domain specialist agents"
    max_tokens: 200000
    default_model: "claude-sonnet-4"
    
  tier_3_task_specific:
    description: "Task-specific agents"
    max_tokens: 200000
    default_model: "claude-sonnet-4"
    
  tier_4_business_domain:
    description: "Business domain specialists"
    max_tokens: 200000
    default_model: "claude-opus-4"

coordination_patterns:
  democratic_decision_making:
    description: "Agents vote and build consensus on approaches"
    min_agents: 2
    consensus_threshold: 0.7
    
  sequential_handoff:
    description: "Agents work in sequence with quality gates"
    quality_gates: true
    validation_required: true
    
  parallel_coordination:
    description: "Agents work simultaneously on different aspects"
    max_parallel: 8
    synchronization_points: true

quality_gates:
  minimum_output_quality: 0.8
  consensus_requirement: 0.7
  escalation_threshold: 0.85
  validation_required: true
EOF

# Coordination engine configuration
cat > config/coordination.yaml << 'EOF'
# Coordination Engine Configuration

decision_making:
  algorithm: "democratic_weighted"
  voting_weights:
    tier_1_core: 1.5
    tier_2_specialists: 1.2
    tier_3_task_specific: 1.0
    tier_4_business_domain: 1.3
    
  consensus_building:
    timeout_seconds: 300
    minimum_participation: 0.6
    quality_threshold: 0.8
    
resource_allocation:
  max_concurrent_agents: 8
  priority_scheduling: true
  load_balancing: true
  cost_optimization: false  # Accuracy over cost
  
escalation_rules:
  complexity_threshold: 0.85
  uncertainty_threshold: 0.6
  novel_domain_detection: true
  cross_paradigm_synthesis: 0.9
  
learning_system:
  pattern_recognition: true
  decision_history_length: 1000
  continuous_improvement: true
  meta_learning: true
EOF

# Create startup scripts
print_status "Creating startup scripts..."

cat > scripts/start-agents.sh << 'EOF'
#!/bin/bash
# Start the AgentNativeFramework agent system

set -e

# Activate virtual environment
source venv/bin/activate

# Start the agent manager
echo "Starting AgentNativeFramework..."
python -c "
import asyncio
import sys
sys.path.append('.')

from core.agents.agent_manager import AgentManager

async def start_framework():
    print('🤖 Initializing AgentNativeFramework...')
    manager = AgentManager()
    
    print('📋 Available agents:')
    registry = manager.get_agent_registry()
    for tier in ['tier_1_core', 'tier_2_specialists', 'tier_4_business_domain']:
        agents_in_tier = [aid for aid, agent in registry.items() if agent.tier.value == tier]
        if agents_in_tier:
            print(f'  {tier.replace(\"_\", \" \").title()}: {len(agents_in_tier)} agents')
    
    print()
    print('✅ AgentNativeFramework is ready!')
    print('   Use the following to interact with agents:')
    print('   - For TreeAI projects: Activate forestry and business agents')
    print('   - For iOS projects: Activate mobile development agents')
    print('   - For research: Activate research orchestration agents')
    print('   - For complex tasks: Activate project supervisor orchestrator')
    print()
    print('🚀 Framework running and ready for agent coordination!')
    
    return manager

if __name__ == '__main__':
    try:
        manager = asyncio.run(start_framework())
    except KeyboardInterrupt:
        print('\n👋 Shutting down AgentNativeFramework...')
    except Exception as e:
        print(f'❌ Error starting framework: {e}')
        sys.exit(1)
"
EOF

chmod +x scripts/start-agents.sh

# Create development tools
cat > scripts/dev-tools.sh << 'EOF'
#!/bin/bash
# Development tools for AgentNativeFramework

case "$1" in
    "test")
        echo "Running framework tests..."
        source venv/bin/activate
        pytest tests/ -v
        ;;
    "lint")
        echo "Running code linting..."
        source venv/bin/activate
        flake8 core/ adapters/ agents/ --max-line-length=88
        black --check core/ adapters/ agents/
        ;;
    "format")
        echo "Formatting code..."
        source venv/bin/activate
        black core/ adapters/ agents/
        ;;
    "agent-status")
        echo "Checking agent system status..."
        source venv/bin/activate
        python -c "
from core.agents.agent_manager import AgentManager
manager = AgentManager()
active = manager.get_active_agents()
print(f'Active agents: {len(active)}')
for agent_id in active:
    print(f'  - {agent_id}')
"
        ;;
    *)
        echo "Usage: $0 {test|lint|format|agent-status}"
        echo ""
        echo "Available commands:"
        echo "  test         - Run framework tests"
        echo "  lint         - Check code quality"
        echo "  format       - Format code with black"
        echo "  agent-status - Check active agents"
        ;;
esac
EOF

chmod +x scripts/dev-tools.sh

# Create basic test structure
print_status "Setting up test framework..."
mkdir -p tests/{unit,integration,agents}

cat > tests/__init__.py << 'EOF'
"""
AgentNativeFramework Test Suite
"""
EOF

cat > tests/test_agent_manager.py << 'EOF'
"""
Tests for the core agent manager
"""
import pytest
import asyncio
from core.agents.agent_manager import AgentManager, AgentTier

@pytest.mark.asyncio
async def test_agent_manager_initialization():
    """Test that agent manager initializes correctly"""
    manager = AgentManager()
    assert manager is not None
    assert len(manager.get_agent_registry()) > 0

@pytest.mark.asyncio
async def test_agent_activation():
    """Test agent activation functionality"""
    manager = AgentManager()
    
    # Try to activate a core agent
    task_context = {"type": "test", "complexity": 0.5}
    agent = await manager.activate_agent("project_supervisor_orchestrator", task_context)
    
    # Check if activation was successful
    if agent:
        assert agent.agent_id == "project_supervisor_orchestrator"
        assert agent.tier == AgentTier.TIER_1_CORE
    
    # Cleanup
    await manager.shutdown()

def test_agent_registry_structure():
    """Test that agent registry has expected structure"""
    manager = AgentManager()
    registry = manager.get_agent_registry()
    
    # Should have agents from different tiers
    tiers = {agent.tier for agent in registry.values()}
    assert AgentTier.TIER_1_CORE in tiers
    assert AgentTier.TIER_2_SPECIALISTS in tiers
EOF

# Create pytest configuration
cat > pytest.ini << 'EOF'
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
asyncio_mode = auto
EOF

print_success "Test framework configured"

# Validate setup
print_status "Validating setup..."

# Check if we can import the core module
python -c "
import sys
sys.path.append('.')
from core.agents.agent_manager import AgentManager
manager = AgentManager()
print(f'✅ Core module loaded successfully')
print(f'📊 Agent registry has {len(manager.get_agent_registry())} agents')
"

print_success "Setup validation complete!"

echo ""
echo "🎉 AgentNativeFramework setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run ./scripts/start-agents.sh to start the framework"
echo "  3. Use ./scripts/init-project.sh to create new projects"
echo "  4. Run ./scripts/dev-tools.sh test to run tests"
echo ""
echo "For more information, see the documentation in the docs/ directory."