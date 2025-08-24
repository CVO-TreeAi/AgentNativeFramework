# 🧠🐛 Agent Native Framework (ANF)

**Collective AI Intelligence for Developers** - Transform Claude Code into a swarm coordination powerhouse.

ANF enables 300+ specialized AI agents to work together through swarm intelligence and hive mind coordination. Instead of working with one AI, command entire teams of expert agents collaborating on your coding challenges.

## 🎯 **NEW**: Claude Hive Swarm Integration

**The game-changer:** Simply type `claude hive swarm` and Claude Code becomes a collective intelligence system!

```bash
# One command to rule them all
claude --dangerously-skip-permissions hive swarm

# Claude Code opens with 300+ agents ready for coordination
# Ask: "Create a development swarm and help me build a secure API"
# Watch: Multiple expert agents coordinate to solve your task!
```

## 📖 **[🌟 START HERE: Interactive How-To Guide 🌟](docs/how-to-guide.html)**

**Click above for the complete interactive guide** with:
- ✅ Step-by-step setup from fresh terminal
- ✅ Copy-paste examples you can use immediately  
- ✅ Interactive simulations of swarm coordination
- ✅ Real-world workflows and use cases
- ✅ Comprehensive troubleshooting help

> **🎯 TL;DR**: Want to jump straight in? Run `./scripts/install-claude-hive-swarm.sh` then `claude --dangerously-skip-permissions hive swarm` and you're ready to command 300+ AI agents!

---

## 🌟 **Alternative Entry Points:**

- **📖 [Interactive How-To Guide](docs/how-to-guide.html)** - Complete hands-on tutorial *(Recommended)*
- **🎮 [Live Demo](index.html)** - Visual introduction with examples
- **📋 [Quick Reference](docs/CLAUDE_HIVE_SWARM.md)** - Command reference and workflows
- **🔧 [Installation Only](scripts/install-claude-hive-swarm.sh)** - Just run the installer

---

## ⚡ Core Features

### **Lightning-Fast Agent Access**
```bash
anf ask "optimize this Rust code"           # Natural language
anf s rust-expert --context=./src          # Quick spawn
anf collaborative "build REST API"         # Multi-agent coordination
```

### **Jarvis-Style Intelligence**  
- **Natural language commands** with auto agent selection
- **Context-aware responses** using project understanding
- **Conversational interface** with persistent memory
- **Proactive suggestions** based on your workflow patterns

### **Power User Workflows**
```bash
# Global hotkeys (works anywhere)
Ctrl+Shift+A        # Activate ANF instantly
Ctrl+A, A          # Quick ask mode
Ctrl+A, S          # Agent spawn menu

# Command composition  
anf analyze-code src/ | anf optimize | anf test | anf deploy

# Parallel coordination
anf collaborate "security audit" --agents=security-auditor,performance-optimizer
```

### **Wave Terminal Integration**
```bash
# Multi-pane development environment
anf wave create-layout development --agents=backend-dev,frontend-dev

# Session management
anf wave save-session "my-project-dev"
anf wave restore-session "my-project-dev"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Terminal Interface (anf)           │  
│  Rich output • Keyboard shortcuts • Themes  │
└─────────────────┬───────────────────────────┘
                  │ Unix Socket (< 1ms latency)
┌─────────────────▼───────────────────────────┐
│         Background Daemon (anfd)            │
│  • 300+ agents ready • Democratic coordination
│  • Resource monitoring • Context management │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  Agent Registry (219 Claude Code + 54 SPARC) │
│  • Performance optimizers • Security auditors
│  • Full-stack developers • Domain specialists │
└─────────────────────────────────────────────┘
```

### **Technology Stack**
- **Rust Core** - High-performance daemon and CLI
- **Tokio Async** - Concurrent agent coordination  
- **Python Integration** - Enhanced agent management
- **Unix Sockets** - Minimal communication latency
- **Terminal UI** - Rich colors, progress bars, live updates

## 📦 Agent Ecosystem

### **Immediate Access** (219 Claude Code Agents)
```bash
anf agents list --category=development
# backend-typescript-architect, rust-pro, react-expert, 
# security-auditor, performance-optimizer, database-expert...
```

### **Coordination Specialists** (54+ SPARC Agents)
- **Swarm coordinators** - Hierarchical, mesh, adaptive
- **Performance analyzers** - Bottleneck identification
- **Consensus builders** - Democratic decision making

### **Domain Experts** (300+ Total Capacity)
- **Development** - Full-stack, mobile, AI/ML specialists
- **Security** - Auditors, compliance, penetration testing  
- **Research** - Academic, technical, market analysis
- **Operations** - DevOps, monitoring, incident response

## 🎯 Use Cases

### **Development Workflows**
```bash
# Morning routine
anfd --start
anf context set $(pwd)
anf spawn backend-dev --background
anf spawn security-auditor --background
anf dashboard --live

# Code review pipeline
anf review-changes --pre-commit --auto-fix-minor
anf analyze-pr #123 --comprehensive
```

### **Performance Optimization**  
```bash
# Real-time monitoring
anf monitor-project . --continuous --alert-on-degradation

# Bottleneck investigation
anf investigate-slowness --trace-requests --suggest-optimizations
```

### **Research & Documentation**
```bash
# Multi-source research  
anf research "AI safety 2024" --comprehensive --agents=academic,technical

# Auto-generate docs
anf document-codebase . --format=markdown,openapi
```

## ⌨️ Keyboard Shortcuts

### **Global Access** (works anywhere in terminal)
- `Ctrl+Shift+A` - Activate ANF from any location
- `Ctrl+A, A` - Quick ask mode
- `Ctrl+A, S` - Spawn agent menu
- `Ctrl+A, R` - Run workflow
- `Ctrl+A, L` - List active agents

### **Interactive Mode**
- `Tab` - Auto-complete commands and agent names
- `Ctrl+R` - Search command history  
- `Ctrl+L` - Clear screen, keep context
- `Ctrl+D` - Background current task

## 🛠️ Configuration

### **Personal Setup** (`~/.anf/config.toml`)
```toml
[agents]
favorites = ["rust-expert", "security-auditor", "performance-optimizer"]

[workflows]
morning_dev = "spawn backend-dev && spawn react-pro && dashboard"
quick_review = "review-code . --agents=security,performance"

[hotkeys]
quick_deploy = "Ctrl+A, D"
emergency_stop = "Ctrl+A, Ctrl+C"
```

### **Team Collaboration**
```bash
# Share team configurations
anf config export team-standards.toml
anf config import team-standards.toml --merge
```

## 📊 Monitoring & Performance

### **Real-time Dashboard**
```bash
anf dashboard --live --agents --system --performance
anf monitor rust-expert --performance-graph --memory-usage
```

### **Resource Optimization**
```bash
anf resources --by-agent --bottlenecks --optimize-suggestions
anf diagnose --connectivity --performance --configuration
```

## 🔧 Advanced Features

### **Custom Agent Creation**
```bash
anf agents create my-stack-expert \
  --base=fullstack-developer \
  --capabilities=nextjs,postgres,redis \
  --memory-persistent
```

### **Workflow Automation**
```bash
anf workflow create deployment-check \
  --steps="test,security-audit,performance-check" \
  --parallel --save-results
```

### **Git Integration**
```bash
anf git setup-hooks --pre-commit="security,performance" 
anf git smart-commit --analyze-changes --auto-message
```

## 📚 Documentation

- **[Installation Guide](install.sh)** - One-line setup process
- **[CLI System Design](CLI_SYSTEM_DESIGN.md)** - Complete architecture
- **[Power User Workflows](examples/workflows.md)** - Advanced patterns
- **[Agent Inventory](COMPREHENSIVE_AGENT_INVENTORY.md)** - All 370+ agents
- **[Operations Guide](docs/operations/runbooks/README.md)** - Production deployment

## 🤝 Contributing

ANF is designed to grow with contributions of new agents, workflows, and integrations:

```bash
# Create custom agent
anf agents create custom-agent --inherit=existing-agent

# Share workflow
anf workflow export my-workflow --publish

# Report issues
anf diagnose --report --submit-feedback
```

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Transform your terminal into an intelligent development companion.**  
*ANF: Where AI agents meet terminal efficiency.*

## Project Types Supported

- **TreeAI/Forestry**: AI-powered business management and pricing
- **iOS/Swift**: Native Apple ecosystem development
- **Next.js/Convex**: Real-time SaaS applications
- **Multi-Agent Systems**: CrewAI orchestration platforms
- **Cross-Platform**: Unified agent coordination

## Agent Categories

- **Development**: ios-developer, backend-architect, fullstack-developer
- **AI/ML**: ai-engineer, ml-engineer, prompt-engineer
- **Security**: security-auditor, mcp-security-auditor
- **Research**: academic-researcher, technical-researcher
- **Business**: business-analyst, market-research-analyst
- **Operations**: devops-engineer, database-optimizer

## Framework Principles

1. **Agent-First Design**: Every workflow starts with agent capabilities
2. **Democratic Coordination**: Agents collaborate on decisions
3. **Persistent Learning**: Knowledge accumulates across projects
4. **Seamless Scaling**: From single agent to 300+ coordination
5. **Project Agnostic**: Framework adapts to any development context

## Contributing

The framework is designed to grow with contributions of new agents, coordination patterns, and project adapters.

## License

MIT License - see LICENSE file for details.