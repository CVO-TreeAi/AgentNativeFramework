# ANF Power User Workflows

## Quick Reference Commands

### Lightning Fast Agent Spawning
```bash
# Quick spawn with context
anf s rust-expert --context=./src/lib.rs

# Background agent with pipe to file  
anf spawn performance-optimizer --background --pipe-to=perf_report.md

# Multi-agent coordination
anf collaborate "optimize API performance" --agents=backend-dev,performance-optimizer,security-auditor
```

### Jarvis-Style Interactions
```bash
# Natural language with auto agent selection
anf ask "how do I make this Rust code faster?"
# → Automatically selects rust-expert + performance-optimizer

# Context-aware questions
anf context set ./my-project
anf ask "review this codebase for security issues"
# → Uses security-auditor with project context

# Follow-up conversations
anf chat rust-expert
> "How do I optimize this function?"
> *shows optimized code*
> "Now benchmark the improvements"
Agent: *runs benchmarks and shows results*
```

## Advanced Workflow Patterns

### 1. Full-Stack Development Workflow
```bash
# Setup development environment
anf workflow dev-environment --stack=nextjs,postgres --agents=8

# This creates:
# Tab 1: backend-typescript-architect (API development)
# Tab 2: react-pro (Frontend components)  
# Tab 3: postgres-expert (Database design)
# Tab 4: security-auditor (Security review)
# Split pane: performance-optimizer (Live monitoring)
```

### 2. Code Review & Optimization Pipeline
```bash
# Parallel code analysis
anf chain "analyze → optimize → test → deploy" --parallel --context=.

# Sequential review with handoffs
anf review-pipeline src/ \
  --agents=senior-code-reviewer,security-auditor,performance-optimizer \
  --output=review_report.md
```

### 3. Research & Documentation Generation
```bash
# Multi-source research
anf research "AI safety best practices 2024" \
  --depth=comprehensive \
  --agents=academic-researcher,technical-researcher \
  --output=research_report.md

# Auto-generate documentation
anf document-codebase . \
  --agents=documentation-specialist,api-documenter \
  --format=markdown,openapi
```

## Keyboard Shortcuts & Power User Tricks

### Global Hotkeys (Works anywhere in terminal)
```bash
Ctrl+Shift+A        # Activate ANF from anywhere
Ctrl+A, A           # Quick ask mode
Ctrl+A, S           # Agent spawn menu
Ctrl+A, R           # Run workflow
Ctrl+A, L           # List active agents
Ctrl+A, H           # Help overlay
Ctrl+A, Q           # Quick exit all agents
```

### Interactive Mode Navigation
```bash
# In anf interactive mode:
Tab                 # Auto-complete commands/agents
Ctrl+R              # Search command history
Ctrl+L              # Clear screen but keep context
Ctrl+D              # Send current task to background
Ctrl+Z              # Suspend agent (resume with 'fg')

# Quick commands in interactive mode:
/spawn rust-expert  # Quick spawn
/list active        # Show active agents
/context ./src      # Set context
/save session dev   # Save current session
```

### Advanced Command Composition
```bash
# Pipe agents together
anf analyze-code src/ | anf optimize | anf test | anf deploy

# Conditional execution  
anf test --on-success="anf deploy staging" --on-fail="anf debug"

# Background processing with notifications
anf run security-audit --background --notify-when-done

# Agent clustering
anf cluster create backend-team --agents=backend-dev,database-optimizer,api-designer
anf cluster run backend-team "implement user authentication"
```

## Wave Terminal Specific Features

### Multi-Pane Agent Coordination
```bash
# Create development layout
anf wave create-layout development \
  --main-agent=fullstack-developer \
  --split-horizontal=performance-optimizer \
  --split-vertical=security-auditor

# Session management
anf wave save-session "my-project-dev"
anf wave restore-session "my-project-dev"

# Dynamic pane management
anf wave split-with-agent rust-expert --direction=vertical
anf wave new-tab-with-agent backend-typescript-architect --context=./api
```

### Enhanced Visual Output
```bash
# Rich terminal output (Wave Terminal)
anf dashboard --live --agents --performance --visual

# Agent status with live updates
anf monitor rust-expert --live --performance-graph

# Interactive agent picker
anf quick-spawn --interactive --visual
```

## Productivity Workflows

### 1. Morning Development Routine
```bash
#!/bin/bash
# ~/.anf/workflows/morning-dev.sh

# Start daemon if not running
anfd --start

# Set context to current project
anf context set $(pwd)

# Start development agents
anf spawn backend-typescript-architect --background
anf spawn react-pro --background  
anf spawn security-auditor --background

# Show dashboard
anf dashboard --agents --system

echo "🚀 Development environment ready!"
```

### 2. Code Review Automation
```bash
# Pre-commit hook integration
anf review-changes --pre-commit \
  --agents=security-auditor,performance-optimizer,senior-code-reviewer \
  --auto-fix-minor-issues \
  --block-on-security-issues

# Pull request analysis
anf analyze-pr #123 \
  --comprehensive \
  --agents=senior-code-reviewer,security-auditor,documentation-specialist \
  --output=pr_analysis.md
```

### 3. Performance Monitoring Workflow
```bash
# Continuous performance monitoring
anf monitor-project . \
  --agents=performance-optimizer \
  --metrics=cpu,memory,response-time \
  --alert-on-degradation \
  --background

# Performance investigation
anf investigate-slowness \
  --agents=performance-optimizer,database-optimizer \
  --trace-requests \
  --suggest-optimizations
```

## Custom Agent Creation

### Creating Specialized Agents
```bash
# Create custom agent profile
anf agents create my-stack-expert \
  --base=fullstack-developer \
  --add-capabilities=nextjs,postgres,redis \
  --context-size=large \
  --memory-persistent

# Deploy custom agent
anf agents deploy my-stack-expert \
  --description="Expert in my specific tech stack" \
  --priority=high
```

### Agent Collaboration Patterns
```bash
# Define custom collaboration pattern
anf patterns create code-review-team \
  --agents=senior-code-reviewer,security-auditor,performance-optimizer \
  --coordination=sequential \
  --decision-method=majority-vote

# Use custom pattern
anf run code-review-team "review changes in src/"
```

## Integration with External Tools

### Git Integration
```bash
# Git hooks with ANF
anf git setup-hooks \
  --pre-commit="security-auditor,performance-optimizer" \
  --pre-push="senior-code-reviewer" \
  --post-merge="update context"

# Smart git workflows
anf git smart-commit \
  --analyze-changes \
  --generate-message \
  --run-tests-first
```

### CI/CD Integration
```bash
# GitHub Actions integration
anf github setup-workflows \
  --on-pr="comprehensive code review" \
  --on-push="security and performance check" \
  --agents=security-auditor,performance-optimizer,senior-code-reviewer

# Deploy with validation
anf deploy staging \
  --validate-with=security-auditor,performance-optimizer \
  --rollback-on-issues
```

### IDE Integration
```bash
# VS Code integration
anf vscode setup-extension \
  --auto-spawn-on-project-open \
  --preferred-agents=fullstack-developer,security-auditor

# Real-time code assistance
anf vscode enable-real-time \
  --agents=performance-optimizer \
  --show-suggestions-inline
```

## Configuration Customization

### Personal Configuration
```toml
# ~/.anf/config.toml

[workflows]
# Custom workflow shortcuts
morning_dev = "spawn backend-dev && spawn react-pro && dashboard"
quick_review = "review-code . --agents=security,performance --format=summary"
deploy_check = "test && security-audit && performance-check"

[agents]
# Favorite agent aliases
be = "backend-typescript-architect"  
fe = "react-pro"
sec = "security-auditor"
perf = "performance-optimizer"

[hotkeys]
# Custom keyboard shortcuts
quick_deploy = "Ctrl+A, D"
emergency_stop = "Ctrl+A, Ctrl+C"
```

### Team Configuration
```bash
# Share team configurations
anf config export team-config.toml \
  --include=workflows,agents,patterns

# Import team standards
anf config import team-config.toml \
  --merge-with-existing
```

## Troubleshooting & Debugging

### Debug Mode
```bash
# Enable debug logging
anf --debug ask "why is this slow?"

# Agent introspection
anf inspect rust-expert \
  --show-state \
  --show-memory \
  --show-recent-tasks

# System diagnostics
anf diagnose \
  --check-connectivity \
  --check-performance \
  --check-configuration
```

### Performance Tuning
```bash
# Optimize daemon performance
anfd --optimize \
  --max-agents=20 \
  --memory-limit=2GB \
  --cpu-limit=4

# Agent resource monitoring
anf resources \
  --by-agent \
  --show-bottlenecks \
  --suggest-optimizations
```

This workflow system transforms ANF into a true "Jarvis for developers" - intelligent, responsive, and incredibly powerful while maintaining the hacker aesthetic and keyboard-driven efficiency you want.