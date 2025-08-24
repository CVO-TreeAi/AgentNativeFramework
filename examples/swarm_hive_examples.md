# 🐛🧠 Swarm-Hive Integration Examples

This document showcases the swarm intelligence and hive mind capabilities integrated into the Agent Native Framework.

## 🚀 Quick Start

### 1. Start Swarm-Hive Integration
```bash
# Start the Python bridge for swarm-hive coordination
./scripts/start-swarm-hive.sh start

# Check status
./scripts/start-swarm-hive.sh status
```

### 2. Basic Commands Overview
```bash
# Swarm commands
anf swarm create my-swarm --topology=hierarchical --agents=rust-expert,backend-dev
anf swarm execute my-swarm "optimize database queries"
anf swarm status my-swarm --live
anf swarm dissolve my-swarm --save-results

# Hive commands  
anf hive init --agents=ai-engineer,research-expert --capabilities=ai,research
anf hive decide "Which ML framework to use?" --options=pytorch,tensorflow,jax
anf hive remember "PyTorch works best for our use case" --memory-type=semantic
anf hive recall "ML framework recommendations" --min-confidence=0.8

# Collaboration (combines swarm + hive)
anf collaborate "build TreeAI mobile app" --agents=ios-developer,ai-engineer,backend-architect
```

## 🐛 Swarm Coordination Examples

### Hierarchical Swarm (Queen-Led)
Perfect for complex projects with clear leadership structure.

```bash
# Create hierarchical swarm for iOS development
anf swarm create ios-dev-swarm \
  --topology=hierarchical \
  --agents=project-supervisor-orchestrator,ios-developer,ai-engineer,security-auditor

# Execute complex development task
anf swarm execute ios-dev-swarm \
  "Build AI-powered TreeAI mobile app with secure authentication and offline capability"

# Monitor progress with live updates
anf swarm status ios-dev-swarm --live
```

**How it works:**
- **Queen Agent** (project-supervisor-orchestrator): Makes strategic decisions and delegates tasks
- **Worker Agents**: Execute specific tasks based on their specializations
- **Coordination**: Top-down with clear hierarchy and task delegation

### Mesh Swarm (Peer-to-Peer)
Ideal for parallel tasks and time-critical coordination.

```bash
# Create mesh swarm for rapid development
anf swarm create rapid-dev-swarm \
  --topology=mesh \
  --agents=backend-dev,frontend-dev,performance-optimizer

# Execute parallel development task
anf swarm execute rapid-dev-swarm \
  "Implement user authentication system with frontend and backend components"
```

**How it works:**
- **Peer Coordination**: All agents propose solutions simultaneously
- **Parallel Execution**: Tasks run concurrently for speed
- **Consensus Building**: Results merged through democratic process

### Collective Swarm (Hive-Mind)
Best for complex problem-solving requiring collective intelligence.

```bash
# Create collective swarm for research
anf swarm create research-swarm \
  --topology=collective \
  --agents=academic-researcher,technical-researcher,ai-engineer,data-scientist

# Execute research task
anf swarm execute research-swarm \
  "Research and recommend the best AI safety practices for production deployment"
```

**How it works:**
- **Collective Understanding**: All agents contribute to problem analysis
- **Shared Consciousness**: Knowledge is synthesized across the collective
- **Emergent Solutions**: Solutions emerge from collective intelligence

### Adaptive Swarm (Dynamic)
Automatically selects the best topology based on task characteristics.

```bash
# Create adaptive swarm (will choose optimal topology)
anf swarm create adaptive-swarm \
  --topology=adaptive \
  --agents=rust-expert,security-auditor,performance-optimizer,backend-dev

# Execute varied tasks - topology adapts automatically
anf swarm execute adaptive-swarm "Optimize Rust web server performance"     # → Mesh (parallel)
anf swarm execute adaptive-swarm "Design secure microservices architecture" # → Hierarchical (complex)
anf swarm execute adaptive-swarm "Research emerging security threats"       # → Collective (research)
```

## 🧠 Hive Intelligence Examples

### Collective Decision Making
Make decisions using the collective wisdom of multiple agents.

```bash
# Initialize hive with domain experts
anf hive init \
  --agents=backend-architect,security-auditor,performance-optimizer,database-expert \
  --capabilities=architecture,security,performance,database

# Create collective decision about technology stack
anf hive decide \
  "What database technology should we use for high-traffic TreeAI application?" \
  --options="PostgreSQL with read replicas","MongoDB with sharding","Redis with persistence","Hybrid PostgreSQL+Redis" \
  --method=consensus \
  --timeout=300
```

**Decision Methods:**
- **Consensus** (75% agreement required)
- **Weighted Voting** (based on agent expertise)
- **Quorum** (minimum participation threshold)
- **Emergent** (let patterns emerge naturally)

### Collective Memory Management
Build and access shared knowledge across the agent collective.

```bash
# Store best practices in collective memory
anf hive remember \
  "For high-performance Rust web servers, use async/await with tokio, implement connection pooling, and cache frequently accessed data in Redis" \
  --memory-type=semantic \
  --contributors=rust-expert,performance-optimizer,backend-architect \
  --confidence=0.95

# Store project-specific learnings
anf hive remember \
  "TreeAI mobile app requires offline-first architecture due to field work requirements" \
  --memory-type=episodic \
  --contributors=ios-developer,project-supervisor \
  --confidence=1.0

# Recall relevant knowledge
anf hive recall "Rust web server optimization" --memory-type=semantic --min-confidence=0.8
anf hive recall "TreeAI mobile requirements" --memory-type=episodic
anf hive recall "security best practices" --min-confidence=0.7
```

**Memory Types:**
- **Working**: Short-term task memory (4 hours retention)
- **Episodic**: Experience-based memory (30 days retention)
- **Semantic**: Knowledge and facts (90 days retention)
- **Collective**: Shared hive memory (1 year retention)

## 🚀 Multi-Agent Collaboration Examples

### Hybrid Coordination (Swarm + Hive)
Combines strategic hive planning with swarm execution.

```bash
# Complex project with hybrid coordination
anf collaborate \
  "Build comprehensive TreeAI business management system with mobile app, web dashboard, and AI analytics" \
  --agents=project-supervisor,ios-developer,backend-architect,ai-engineer,security-auditor,database-expert \
  --mode=swarm_hive_hybrid \
  --topology=adaptive

# This executes in 3 phases:
# Phase 1: Hive Planning - Collective strategic decisions
# Phase 2: Swarm Execution - Coordinated implementation  
# Phase 3: Hive Validation - Quality assessment and learning
```

### Specialized Task Forces
Create specialized coordination for different types of work.

```bash
# Security-focused collaboration
anf collaborate \
  "Conduct comprehensive security audit of TreeAI platform" \
  --agents=security-auditor,penetration-tester,compliance-expert,backend-architect \
  --mode=hive_only \
  --topology=collective

# Performance optimization task force  
anf collaborate \
  "Optimize TreeAI platform for 10x user growth" \
  --agents=performance-optimizer,database-expert,rust-expert,monitoring-specialist \
  --mode=swarm_only \
  --topology=mesh

# Research and innovation team
anf collaborate \
  "Research and prototype next-generation AI features for TreeAI" \
  --agents=ai-engineer,research-specialist,academic-researcher,innovation-catalyst \
  --mode=adaptive_selection
```

## 🎯 Real-World Use Cases

### 1. Full-Stack Development
```bash
# Create development ecosystem
anf swarm create fullstack-ecosystem \
  --topology=hierarchical \
  --agents=project-supervisor,backend-typescript-architect,react-expert,database-expert,security-auditor

# Build complete application
anf swarm execute fullstack-ecosystem \
  "Build TreeAI SaaS platform with React frontend, Node.js backend, PostgreSQL database, and enterprise security"
```

### 2. Code Review and Quality Assurance
```bash
# Initialize quality assurance hive
anf hive init \
  --agents=senior-code-reviewer,security-auditor,performance-optimizer,test-specialist \
  --capabilities=code-review,security,performance,testing

# Make decision about code quality standards
anf hive decide \
  "What should be our minimum code coverage threshold?" \
  --options="80%","85%","90%","95%" \
  --method=weighted_voting

# Store quality guidelines in collective memory
anf hive remember \
  "All API endpoints must have input validation, error handling, rate limiting, and comprehensive tests" \
  --memory-type=collective \
  --contributors=security-auditor,senior-code-reviewer,backend-architect
```

### 3. Research and Development
```bash
# Create R&D collective
anf collaborate \
  "Research emerging AI technologies and their potential application to TreeAI platform" \
  --agents=ai-researcher,academic-researcher,innovation-specialist,technical-writer \
  --mode=collective \
  --topology=emergent
```

### 4. Incident Response
```bash
# Rapid response swarm for production issues
anf swarm create incident-response \
  --topology=mesh \
  --agents=devops-engineer,database-admin,security-engineer,monitoring-specialist

# Coordinate incident response
anf swarm execute incident-response \
  "Database performance degraded, investigate and resolve immediately"
```

## 📊 Monitoring and Analytics

### Check System Status
```bash
# Overall coordination status
anf dashboard --agents --system --workflows

# Swarm-specific monitoring
anf swarm list --detailed
anf swarm status my-swarm --live

# Hive intelligence metrics
anf hive status --nodes --memory --decisions
```

### Performance Optimization
```bash
# Analyze coordination efficiency
./scripts/start-swarm-hive.sh status

# View coordination logs
./scripts/start-swarm-hive.sh logs

# Test system responsiveness  
./scripts/start-swarm-hive.sh test
```

## 🔧 Advanced Configuration

### Custom Swarm Topologies
Edit `config/swarm_hive_config.yaml`:

```yaml
swarm_configuration:
  topologies:
    custom_topology:
      description: "Custom coordination pattern"
      ideal_size: [4, 8]
      complexity_range: [0.5, 0.9]
      time_critical: false
```

### Memory Management
```yaml
hive_configuration:
  memory_configuration:
    working_memory:
      retention_hours: 8      # Extend for long tasks
      decay_rate: 0.85       # Faster decay
    
    collective_memory:
      retention_days: 730    # 2 years for important knowledge
```

### Agent Role Mapping
```yaml
agent_role_mapping:
  queen_candidates:
    - "project-supervisor-orchestrator"
    - "research-orchestrator"
    - "senior-architect"        # Add custom queen
  
  specialist_roles:
    ai_development:
      - "ai-engineer"
      - "ml-specialist"
      - "neural-network-expert"  # Add custom specialist
```

## 🛠️ Troubleshooting

### Common Issues

**Python Bridge Connection Failed**
```bash
# Restart the bridge
./scripts/start-swarm-hive.sh restart

# Check logs
./scripts/start-swarm-hive.sh logs
```

**Swarm Creation Timeout**
```bash
# Check agent availability
anf agents list --available

# Reduce swarm size or complexity
anf swarm create smaller-swarm --agents=agent1,agent2
```

**Hive Decision Stuck**
```bash
# Check hive status
anf hive status --nodes --decisions

# Initialize more nodes if needed
anf hive init --agents=additional-agent
```

### Debug Mode
```bash
# Enable verbose logging
export ANF_DEBUG=1
anf collaborate "test task" --agents=test-agent
```

## 🎉 Next Steps

1. **Start with simple swarms** - Try hierarchical topology first
2. **Experiment with hive decisions** - Use consensus method initially  
3. **Build collective memory** - Store learnings from each session
4. **Scale gradually** - Add more agents as you get comfortable
5. **Monitor performance** - Use the status commands to optimize

The swarm-hive integration transforms ANF into a true collective intelligence system where agents can collaborate, learn, and evolve together! 🚀🧠🐛