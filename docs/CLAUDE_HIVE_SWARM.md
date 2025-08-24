# 🧠🐛 Claude Hive Swarm Integration

Transform Claude Code into a collective intelligence powerhouse with swarm coordination and hive mind capabilities.

## 🚀 Quick Start

### Installation
```bash
# Install the integration
./scripts/install-claude-hive-swarm.sh

# Start Claude Code with collective intelligence
claude hive swarm
```

### Your New Superpower
Instead of working with just one AI, you now command a collective of 300+ specialized agents that can:
- **Coordinate as swarms** for complex tasks
- **Make collective decisions** through hive intelligence  
- **Remember and learn** across all interactions
- **Collaborate seamlessly** on multi-faceted problems

## 🎯 Core Concept

**Before**: `claude` → Single AI assistant  
**After**: `claude hive swarm` → Collective AI intelligence with swarm coordination

### The Magic
When you type `claude hive swarm`, you're not just opening Claude Code - you're launching it with access to:
- 🧠 **Hive Intelligence**: Collective decision-making and persistent memory
- 🐛 **Swarm Coordination**: Multi-agent task execution
- 🤝 **Hybrid Coordination**: Strategic hive planning + swarm execution
- 📊 **Real-time Coordination**: Live progress tracking and adaptation

## 📋 Available Commands

### Launch Commands
```bash
claude hive swarm    # Full collective intelligence (recommended)
claude hive          # Hive intelligence only
claude swarm         # Swarm coordination only  
claude               # Standard Claude Code (unchanged)
```

### MCP Tools Available in Claude Code

Once launched, Claude Code has access to these new tools:

#### 🐛 Swarm Tools

**`swarm_create`** - Create agent swarms
```json
{
  "swarm_id": "dev-team",
  "topology": "hierarchical", 
  "agents": ["backend-typescript-architect", "security-auditor", "performance-optimizer"],
  "task_description": "Full-stack development team"
}
```

**`swarm_coordinate`** - Execute tasks with swarm coordination
```json
{
  "swarm_id": "dev-team",
  "task": "Build secure REST API with optimal performance",
  "complexity": 0.8,
  "time_critical": false
}
```

**`collaborate`** - Multi-agent collaboration (combines swarm + hive)
```json
{
  "task_description": "Design and implement user authentication system",
  "agents": ["backend-architect", "security-auditor", "frontend-expert"],
  "coordination_mode": "swarm_hive_hybrid",
  "complexity": 0.7
}
```

#### 🧠 Hive Tools

**`hive_decide`** - Collective decision making
```json
{
  "question": "Which database should we use for high-traffic application?",
  "options": ["PostgreSQL", "MongoDB", "Redis", "Hybrid approach"],
  "agents": ["database-expert", "performance-optimizer", "backend-architect"],
  "method": "consensus"
}
```

**`hive_remember`** - Store in collective memory
```json
{
  "content": "For React apps, use React.memo for expensive components and useMemo for complex calculations",
  "memory_type": "semantic",
  "contributors": ["react-expert", "performance-optimizer"],
  "confidence": 0.9
}
```

**`hive_recall`** - Retrieve from collective memory
```json
{
  "query": "React performance optimization best practices",
  "memory_type": "semantic",
  "min_confidence": 0.7
}
```

#### 📊 Status Tools

**`get_swarm_status`** - Monitor coordination
```json
{
  "swarm_id": "dev-team",
  "detailed": true
}
```

**`list_agents`** - See available agents
```json
{
  "category": "development",
  "capabilities": ["security", "performance"]
}
```

## 🎮 Example Workflows

### 1. Full-Stack Development with Swarm Coordination

**Step 1**: Launch with collective intelligence
```bash
claude hive swarm
```

**Step 2**: In Claude Code, create a development swarm
> I need to build a secure e-commerce API. Can you create a development swarm and coordinate the task?

Claude will use the `swarm_create` tool:
```json
{
  "swarm_id": "ecommerce-dev",
  "topology": "hierarchical",
  "agents": ["backend-architect", "security-auditor", "database-expert", "performance-optimizer"],
  "task_description": "E-commerce API development team"
}
```

**Step 3**: Coordinate the development task
Claude uses `swarm_coordinate`:
```json
{
  "swarm_id": "ecommerce-dev", 
  "task": "Design and implement secure e-commerce API with user auth, product catalog, cart, and payment processing",
  "complexity": 0.9
}
```

**Result**: You get coordinated solutions from multiple expert agents working together!

### 2. Collective Decision Making

**Scenario**: Architecture decision needed

> I'm building a real-time chat application. Help me decide on the best architecture approach using collective intelligence.

Claude uses `hive_decide`:
```json
{
  "question": "What's the best architecture for a scalable real-time chat application?",
  "options": [
    "WebSocket-based monolith with Redis",
    "Microservices with message queues", 
    "Serverless with WebSocket API Gateway",
    "Peer-to-peer with WebRTC"
  ],
  "agents": ["backend-architect", "real-time-specialist", "scalability-expert"],
  "method": "consensus"
}
```

**Result**: Multiple expert agents collaborate to give you the best architectural decision!

### 3. Building Collective Knowledge

**Learning and Memory**: Every interaction builds collective intelligence

> Store this insight: "For high-performance Node.js APIs, use clustering, implement proper error handling, cache frequently accessed data, and use connection pooling for databases."

Claude uses `hive_remember`:
```json
{
  "content": "For high-performance Node.js APIs, use clustering, implement proper error handling, cache frequently accessed data, and use connection pooling for databases",
  "memory_type": "semantic",
  "contributors": ["nodejs-expert", "performance-optimizer"],
  "confidence": 0.95
}
```

**Later retrieval**:
> What are the best practices for Node.js API performance?

Claude uses `hive_recall` and instantly accesses the collective knowledge!

### 4. Complex Project Coordination

**Scenario**: Multi-phase project with different expertise needs

> I need to build a TreeAI mobile app with AI-powered tree analysis, secure user authentication, offline capability, and cloud sync.

Claude uses `collaborate` with hybrid coordination:
```json
{
  "task_description": "Build TreeAI mobile app with AI analysis, auth, offline sync",
  "agents": ["ios-developer", "ai-engineer", "security-expert", "backend-architect"],
  "coordination_mode": "swarm_hive_hybrid",
  "complexity": 0.9
}
```

**Result**: 
1. **Hive Planning Phase**: Collective strategic decisions about architecture
2. **Swarm Execution Phase**: Coordinated implementation across specialties
3. **Hive Validation Phase**: Quality assessment and learning integration

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│           Your Command              │
│         claude hive swarm           │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│       Enhanced Claude Code          │  ← Your familiar interface
│    + MCP Swarm-Hive Integration     │
└─────────────────┬───────────────────┘
                  │ MCP Protocol
┌─────────────────▼───────────────────┐
│       Swarm-Hive MCP Server         │  ← New intelligence layer
│     (swarm_hive_mcp.py)             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│    AgentNativeFramework Core       │  ← 300+ agent ecosystem
│  SwarmManager + HiveIntelligence    │
└─────────────────────────────────────┘
```

## 🎭 Agent Personalities & Specializations

### Available Agent Types

**🏗️ Development Specialists**
- `backend-typescript-architect` - Backend systems and APIs
- `rust-pro` - Systems programming and performance
- `react-expert` - Frontend React applications
- `ios-developer` - Native iOS development
- `fullstack-developer` - End-to-end solutions

**🔒 Security & Quality**
- `security-auditor` - Security analysis and best practices
- `performance-optimizer` - Performance tuning and optimization
- `senior-code-reviewer` - Code quality and architecture review

**🧠 AI & Research**
- `ai-engineer` - Machine learning and AI integration
- `research-orchestrator` - Research coordination and analysis
- `academic-researcher` - Academic research and insights

**📊 Data & Infrastructure**
- `database-expert` - Database design and optimization
- `devops-engineer` - Infrastructure and deployment
- `monitoring-specialist` - System monitoring and observability

### Coordination Topologies

**Hierarchical** (Queen-led)
- Best for: Complex projects with clear leadership
- Agent roles: Queen → Coordinators → Workers → Specialists
- Example: Large application development

**Mesh** (Peer-to-peer) 
- Best for: Parallel tasks and speed
- All agents propose solutions simultaneously
- Example: Code review, quick optimizations

**Collective** (Hive-mind)
- Best for: Complex decision-making
- Shared consciousness across all agents
- Example: Architecture decisions, research

**Adaptive** (Dynamic)
- Automatically selects optimal topology
- Changes based on task characteristics
- Example: Variable complexity tasks

## 🎯 Best Practices

### When to Use What

**Use `claude hive swarm` when:**
- Building complex applications (full-stack, mobile, enterprise)
- Need both strategic planning AND execution coordination
- Want persistent learning across sessions
- Working on multi-faceted problems requiring diverse expertise

**Use `claude hive` when:**
- Making strategic decisions
- Need collective wisdom from multiple perspectives
- Building organizational knowledge base
- Research and analysis tasks

**Use `claude swarm` when:**
- Coordinating specific implementation tasks
- Need parallel execution across specialists
- Time-critical development work
- Clear task delegation scenarios

**Use regular `claude` when:**
- Simple, single-agent tasks
- Quick questions or code snippets
- Don't need coordination overhead
- Working in constrained environments

### Optimization Tips

1. **Start with the right agents**: Choose agents that match your domain
2. **Use appropriate topology**: Let adaptive mode choose, or pick based on task type
3. **Build collective memory**: Store insights for future use
4. **Monitor coordination**: Check swarm status for complex tasks
5. **Iterate with feedback**: Use hive decisions to refine approaches

## 🔧 Advanced Configuration

### Custom Agent Selection
```json
{
  "swarm_id": "custom-team",
  "topology": "collective",
  "agents": ["domain-specific-expert-1", "domain-specific-expert-2"],
  "task_description": "Specialized task requiring domain expertise"
}
```

### Memory Management
- **Working Memory**: 4-hour retention for active tasks
- **Episodic Memory**: 30-day retention for project experiences  
- **Semantic Memory**: 90-day retention for knowledge and facts
- **Collective Memory**: 1-year retention for organizational wisdom

### Decision Methods
- **Consensus**: 75% agreement required (democratic)
- **Weighted Voting**: Based on agent expertise (meritocratic) 
- **Quorum**: Minimum participation threshold (representative)
- **Emergent**: Pattern-based natural consensus (organic)

## 🐛 Troubleshooting

### Common Issues

**"Integration not found"**
```bash
./scripts/start-swarm-hive.sh start
```

**"Dependencies not available"**
```bash
pip3 install structlog prometheus_client pyyaml numpy
```

**"Claude command not found"**
- Install Claude Code first, then run the installation script

**"MCP server not responding"**  
```bash
./scripts/start-swarm-hive.sh restart
```

### Debug Mode
Set environment variable for verbose logging:
```bash
export SWARM_HIVE_DEBUG=1
claude hive swarm
```

## 🚀 What's Next?

You now have access to true collective AI intelligence! Your `claude hive swarm` command gives you:

✅ **300+ specialized agents** at your command  
✅ **4 coordination topologies** for any situation  
✅ **Collective decision-making** with multiple perspectives  
✅ **Persistent memory** that learns and grows  
✅ **Real-time coordination** with beautiful progress tracking  
✅ **Seamless integration** with your familiar Claude Code interface  

**The future of development is collective intelligence - and it's available now with `claude hive swarm`!** 🧠🐛🚀