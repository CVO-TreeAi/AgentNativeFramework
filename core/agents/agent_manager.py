"""
AgentNativeFramework - Core Agent Management System
Orchestrates the 300+ agent ecosystem with democratic coordination
Enhanced with swarm intelligence and hive mind capabilities
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
from pathlib import Path
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import structlog
import yaml

class AgentTier(Enum):
    TIER_1_CORE = "tier_1_core"           # Core framework agents
    TIER_2_SPECIALISTS = "tier_2_specialists"  # Domain specialists
    TIER_3_TASK_SPECIFIC = "tier_3_task_specific"  # Task-specific agents
    TIER_4_BUSINESS_DOMAIN = "tier_4_business_domain"  # Business domain agents

class AgentStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    COORDINATING = "coordinating"
    ESCALATING = "escalating"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentCapability:
    name: str
    description: str
    tools: List[str]
    specialization_domains: List[str]
    coordination_patterns: List[str]
    activation_triggers: List[str]

@dataclass
class AgentConfiguration:
    agent_id: str
    name: str
    tier: AgentTier
    model: str = "claude-sonnet-4"
    max_tokens: int = 200000  # Full context by default
    temperature: float = 0.3
    capabilities: AgentCapability = None
    coordination_priority: int = 50  # 1-100, higher = higher priority
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    quality_gates: Dict[str, float] = field(default_factory=dict)

class AgentManager:
    """
    Central orchestrator for the 300+ agent ecosystem
    Handles agent activation, coordination, and democratic decision-making
    """
    
    # Operational metrics
    agent_activations = Counter('agent_activations_total', 'Total agent activations', ['agent_id', 'status'])
    coordination_duration = Histogram('coordination_duration_seconds', 'Time spent coordinating agents')
    active_agents_gauge = Gauge('active_agents_count', 'Number of currently active agents')
    decision_latency = Summary('decision_making_duration_seconds', 'Time to reach consensus')
    error_rate = Counter('agent_errors_total', 'Total agent errors', ['error_type', 'agent_id'])
    
    def __init__(self, config_path: Optional[Path] = None, swarm_hive_coordinator=None):
        # Setup structured logging
        structlog.configure(
            processors=[
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.dev.ConsoleRenderer()
            ],
            logger_factory=structlog.PrintLoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            cache_logger_on_first_use=True,
        )
        self.logger = structlog.get_logger(__name__)
        
        # Start metrics server
        try:
            start_http_server(8000)
            self.logger.info("metrics_server_started", port=8000)
        except Exception as e:
            self.logger.warning("metrics_server_failed", error=str(e))
        
        self.active_agents: Dict[str, AgentConfiguration] = {}
        self.agent_registry: Dict[str, AgentConfiguration] = {}
        self.coordination_patterns: Dict[str, Any] = {}
        self.decision_history: List[Dict[str, Any]] = []
        
        # Swarm-Hive integration
        self.swarm_hive_coordinator = swarm_hive_coordinator
        self.swarm_hive_config = self.load_swarm_hive_config()
        
        # Load configuration
        if config_path:
            self.load_configuration(config_path)
        else:
            self.initialize_default_registry()
    
    def initialize_default_registry(self):
        """Initialize the core agent registry with default configurations"""
        
        # Tier 1: Core Framework Agents
        core_agents = [
            AgentConfiguration(
                agent_id="project_supervisor_orchestrator",
                name="Project Supervisor Orchestrator",
                tier=AgentTier.TIER_1_CORE,
                model="claude-opus-4",
                capabilities=AgentCapability(
                    name="Multi-step workflow management",
                    description="Manages complex workflows coordinating multiple agents",
                    tools=["task_decomposition", "agent_coordination", "quality_gates"],
                    specialization_domains=["orchestration", "workflow_management"],
                    coordination_patterns=["democratic_decision", "sequential_handoff"],
                    activation_triggers=["complex_multi_step", "agent_coordination_needed"]
                ),
                coordination_priority=95
            ),
            
            AgentConfiguration(
                agent_id="research_orchestrator",
                name="Research Orchestrator",
                tier=AgentTier.TIER_1_CORE,
                model="claude-opus-4",
                capabilities=AgentCapability(
                    name="Comprehensive research coordination",
                    description="Coordinates multi-phase research projects",
                    tools=["research_planning", "specialist_coordination", "synthesis"],
                    specialization_domains=["research", "analysis", "synthesis"],
                    coordination_patterns=["specialist_handoff", "parallel_research"],
                    activation_triggers=["research_project", "multi_source_analysis"]
                ),
                coordination_priority=90
            ),
            
            AgentConfiguration(
                agent_id="context_manager",
                name="Context Manager",
                tier=AgentTier.TIER_1_CORE,
                model="claude-sonnet-4",
                capabilities=AgentCapability(
                    name="Cross-agent context preservation",
                    description="Manages context across multiple agents and sessions",
                    tools=["context_preservation", "memory_management", "state_handoff"],
                    specialization_domains=["context_management", "memory_systems"],
                    coordination_patterns=["context_continuity", "state_preservation"],
                    activation_triggers=["context_exceeds_10k_tokens", "multi_session_task"]
                ),
                coordination_priority=85
            )
        ]
        
        # Tier 2: Development Specialists
        development_agents = [
            AgentConfiguration(
                agent_id="ios_developer",
                name="iOS Developer",
                tier=AgentTier.TIER_2_SPECIALISTS,
                model="claude-sonnet-4",
                capabilities=AgentCapability(
                    name="Native iOS development",
                    description="Swift/SwiftUI development with native integrations",
                    tools=["swift", "swiftui", "xcode", "anthropic_api"],
                    specialization_domains=["ios", "swift", "mobile", "apple_ecosystem"],
                    coordination_patterns=["mobile_team", "ui_backend_coordination"],
                    activation_triggers=["ios_development", "swift_code", "mobile_app"]
                ),
                coordination_priority=80
            ),
            
            AgentConfiguration(
                agent_id="backend_architect",
                name="Backend Architect",
                tier=AgentTier.TIER_2_SPECIALISTS,
                model="claude-sonnet-4",
                capabilities=AgentCapability(
                    name="API and system architecture",
                    description="RESTful APIs, microservices, database design",
                    tools=["api_design", "database_modeling", "system_architecture"],
                    specialization_domains=["backend", "api", "architecture", "databases"],
                    coordination_patterns=["full_stack_coordination", "security_integration"],
                    activation_triggers=["backend_development", "api_design", "system_architecture"]
                ),
                coordination_priority=75
            ),
            
            AgentConfiguration(
                agent_id="ai_engineer",
                name="AI Engineer",
                tier=AgentTier.TIER_2_SPECIALISTS,
                model="claude-opus-4",  # Higher tier for AI complexity
                capabilities=AgentCapability(
                    name="LLM applications and RAG systems",
                    description="AI-powered applications, prompt engineering, RAG",
                    tools=["llm_integration", "rag_systems", "prompt_engineering"],
                    specialization_domains=["ai", "ml", "llm", "rag"],
                    coordination_patterns=["ai_ml_team", "research_integration"],
                    activation_triggers=["ai_development", "llm_integration", "rag_system"]
                ),
                coordination_priority=85
            )
        ]
        
        # Tier 3: TreeAI/Forestry Specialists
        treeai_agents = [
            AgentConfiguration(
                agent_id="tree_analysis_specialist",
                name="Tree Analysis Specialist",
                tier=AgentTier.TIER_4_BUSINESS_DOMAIN,
                model="claude-opus-4",
                capabilities=AgentCapability(
                    name="AI-powered tree assessments",
                    description="Tree health analysis, AFISS assessments, TreeScore calculations",
                    tools=["tree_assessment", "afiss_protocol", "treescore_calculation"],
                    specialization_domains=["forestry", "arboriculture", "tree_assessment"],
                    coordination_patterns=["forestry_team", "business_integration"],
                    activation_triggers=["tree_assessment", "afiss_evaluation", "forestry_analysis"]
                ),
                coordination_priority=70
            ),
            
            AgentConfiguration(
                agent_id="forestry_business_analyst",
                name="Forestry Business Analyst",
                tier=AgentTier.TIER_4_BUSINESS_DOMAIN,
                model="claude-sonnet-4",
                capabilities=AgentCapability(
                    name="Forestry business operations",
                    description="PpH pricing, DOCS workflow, business optimization",
                    tools=["pph_calculations", "docs_workflow", "business_metrics"],
                    specialization_domains=["forestry_business", "pricing", "operations"],
                    coordination_patterns=["business_team", "pricing_optimization"],
                    activation_triggers=["forestry_business", "pricing_strategy", "docs_workflow"]
                ),
                coordination_priority=65
            )
        ]
        
        # Register all agents
        all_agents = core_agents + development_agents + treeai_agents
        for agent in all_agents:
            self.agent_registry[agent.agent_id] = agent
    
    async def activate_agent(self, agent_id: str, task_context: Dict[str, Any]) -> Optional[AgentConfiguration]:
        """
        Activate a specific agent for a task
        """
        if agent_id not in self.agent_registry:
            self.logger.error(f"Agent {agent_id} not found in registry")
            return None
        
        agent_config = self.agent_registry[agent_id]
        
        # Check if agent is already active
        if agent_id in self.active_agents:
            self.logger.info(f"Agent {agent_id} already active")
            return self.active_agents[agent_id]
        
        # Validate resource requirements
        if not await self.validate_resource_requirements(agent_config):
            self.logger.warning(f"Resource requirements not met for agent {agent_id}")
            return None
        
        # Activate the agent
        self.active_agents[agent_id] = agent_config
        self.logger.info(f"Activated agent: {agent_id}")
        
        # Update agent status
        await self.update_agent_status(agent_id, AgentStatus.ACTIVE)
        
        return agent_config
    
    async def coordinate_agents(self, task: Dict[str, Any], required_capabilities: List[str]) -> Dict[str, Any]:
        """
        Coordinate multiple agents for complex tasks using democratic decision-making
        """
        # Identify suitable agents based on capabilities
        suitable_agents = self.find_agents_by_capabilities(required_capabilities)
        
        if not suitable_agents:
            return {"error": "No suitable agents found for required capabilities"}
        
        # Activate required agents
        activated_agents = []
        for agent_id in suitable_agents:
            agent = await self.activate_agent(agent_id, task)
            if agent:
                activated_agents.append(agent)
        
        if not activated_agents:
            return {"error": "Failed to activate any suitable agents"}
        
        # Democratic coordination
        coordination_result = await self.democratic_coordination(activated_agents, task)
        
        # Log decision for learning
        self.decision_history.append({
            "task": task,
            "agents": [agent.agent_id for agent in activated_agents],
            "result": coordination_result,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        return coordination_result
    
    async def democratic_coordination(self, agents: List[AgentConfiguration], task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement democratic decision-making among agents
        """
        proposals = []
        
        # Gather proposals from each agent
        for agent in agents:
            proposal = await self.get_agent_proposal(agent, task)
            if proposal:
                proposals.append({
                    "agent_id": agent.agent_id,
                    "proposal": proposal,
                    "confidence": proposal.get("confidence", 0.5),
                    "priority": agent.coordination_priority
                })
        
        if not proposals:
            return {"error": "No proposals received from agents"}
        
        # Evaluate and rank proposals
        ranked_proposals = self.rank_proposals(proposals)
        
        # Build consensus or select best approach
        final_approach = await self.build_consensus(ranked_proposals, task)
        
        return final_approach
    
    def find_agents_by_capabilities(self, required_capabilities: List[str]) -> List[str]:
        """
        Find agents that match required capabilities
        """
        suitable_agents = []
        
        for agent_id, agent_config in self.agent_registry.items():
            if not agent_config.capabilities:
                continue
            
            # Check if agent has any of the required capabilities
            agent_domains = set(agent_config.capabilities.specialization_domains)
            required_set = set(required_capabilities)
            
            if agent_domains.intersection(required_set):
                suitable_agents.append(agent_id)
        
        # Sort by coordination priority
        suitable_agents.sort(
            key=lambda x: self.agent_registry[x].coordination_priority,
            reverse=True
        )
        
        return suitable_agents
    
    async def get_agent_proposal(self, agent: AgentConfiguration, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a proposal from a specific agent for a task
        This would integrate with Claude Code to actually run the agent
        """
        # Placeholder for actual agent execution
        # In practice, this would call Claude Code with the agent's configuration
        return {
            "approach": f"Agent {agent.name} proposes solution for {task.get('type', 'task')}",
            "confidence": 0.8,
            "resources_needed": agent.resource_requirements,
            "expected_quality": 0.85
        }
    
    def rank_proposals(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank proposals based on confidence, priority, and quality
        """
        def proposal_score(proposal):
            return (
                proposal["confidence"] * 0.4 +
                proposal["priority"] / 100 * 0.3 +
                proposal["proposal"].get("expected_quality", 0.5) * 0.3
            )
        
        return sorted(proposals, key=proposal_score, reverse=True)
    
    async def build_consensus(self, ranked_proposals: List[Dict[str, Any]], task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build consensus from ranked proposals
        """
        if not ranked_proposals:
            return {"error": "No proposals to build consensus from"}
        
        # For now, select the top proposal
        # In a full implementation, this would involve more sophisticated consensus building
        top_proposal = ranked_proposals[0]
        
        return {
            "selected_approach": top_proposal["proposal"]["approach"],
            "lead_agent": top_proposal["agent_id"],
            "supporting_agents": [p["agent_id"] for p in ranked_proposals[1:3]],
            "consensus_confidence": top_proposal["confidence"],
            "coordination_plan": self.create_coordination_plan(ranked_proposals[:3])
        }
    
    def create_coordination_plan(self, selected_proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a coordination plan for the selected agents
        """
        return {
            "phases": ["preparation", "execution", "validation", "integration"],
            "agent_roles": {
                proposal["agent_id"]: f"Role based on {proposal['agent_id']} capabilities"
                for proposal in selected_proposals
            },
            "handoff_points": ["phase_completion", "quality_gate_validation"],
            "quality_gates": ["minimum_quality_0.8", "consensus_validation"]
        }
    
    async def validate_resource_requirements(self, agent: AgentConfiguration) -> bool:
        """
        Validate that resources are available for the agent
        """
        # Placeholder for resource validation
        # Would check compute resources, API limits, etc.
        return True
    
    async def update_agent_status(self, agent_id: str, status: AgentStatus):
        """
        Update the status of an agent
        """
        if agent_id in self.active_agents:
            # In a full implementation, this would update persistent storage
            self.logger.info(f"Agent {agent_id} status updated to {status.value}")
    
    def load_configuration(self, config_path: Path):
        """
        Load agent configurations from file
        """
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Parse configuration and populate registry
            for agent_data in config_data.get('agents', []):
                agent_config = AgentConfiguration(**agent_data)
                self.agent_registry[agent_config.agent_id] = agent_config
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.initialize_default_registry()
    
    def get_active_agents(self) -> Dict[str, AgentConfiguration]:
        """
        Get all currently active agents
        """
        return self.active_agents.copy()
    
    def get_agent_registry(self) -> Dict[str, AgentConfiguration]:
        """
        Get the complete agent registry
        """
        return self.agent_registry.copy()
    
    async def deactivate_agent(self, agent_id: str):
        """
        Deactivate a specific agent
        """
        if agent_id in self.active_agents:
            del self.active_agents[agent_id]
            await self.update_agent_status(agent_id, AgentStatus.IDLE)
            self.logger.info(f"Deactivated agent: {agent_id}")
    
    async def shutdown(self):
        """
        Gracefully shutdown all active agents
        """
        for agent_id in list(self.active_agents.keys()):
            await self.deactivate_agent(agent_id)
        
        self.logger.info("Agent manager shutdown complete")
    
    def load_swarm_hive_config(self) -> Dict[str, Any]:
        """Load swarm-hive configuration"""
        config_path = Path(__file__).parent.parent.parent / "config" / "swarm_hive_config.yaml"
        
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                self.logger.info("swarm_hive_config_loaded", path=str(config_path))
                return config
        except Exception as e:
            self.logger.warning("swarm_hive_config_load_failed", error=str(e))
        
        # Return default configuration
        return {
            "swarm_configuration": {"default_topology": "adaptive"},
            "hive_configuration": {"decision_methods": {"consensus": {"threshold": 0.75}}},
            "coordination_modes": {"adaptive_selection": {"complexity_range": [0.0, 1.0]}}
        }
    
    async def coordinate_with_swarm_hive(
        self, 
        task: Dict[str, Any], 
        coordination_mode: str = "adaptive_selection"
    ) -> Dict[str, Any]:
        """Enhanced coordination using swarm-hive intelligence"""
        
        if not self.swarm_hive_coordinator:
            self.logger.warning("swarm_hive_coordinator_not_available")
            # Fall back to traditional coordination
            return await self.coordinate_agents(task, task.get("required_capabilities", []))
        
        # Import here to avoid circular imports
        from ..coordination.swarm_hive_coordinator import CoordinationTask, CoordinationMode
        
        # Create coordination task
        coordination_task = CoordinationTask(
            task_id=f"agent_mgr_{int(time.time())}",
            description=task.get("description", "Agent coordination task"),
            complexity=task.get("complexity", 0.5),
            required_capabilities=task.get("required_capabilities", []),
            time_critical=task.get("time_critical", False),
            coordination_mode=CoordinationMode(coordination_mode) if coordination_mode != "adaptive_selection" else None
        )
        
        # Use swarm-hive coordination
        result = await self.swarm_hive_coordinator.coordinate_task(coordination_task)
        
        # Log the enhanced coordination
        self.logger.info(
            "swarm_hive_coordination_completed",
            task_id=coordination_task.task_id,
            mode=result.get("coordination_mode"),
            duration=result.get("duration")
        )
        
        return result
    
    def get_swarm_hive_recommendations(self, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommendations for swarm-hive coordination based on task requirements"""
        
        config = self.swarm_hive_config
        complexity = task_requirements.get("complexity", 0.5)
        agent_count_needed = len(task_requirements.get("required_capabilities", []))
        time_critical = task_requirements.get("time_critical", False)
        
        recommendations = {}
        
        # Recommend coordination mode
        for mode, mode_config in config.get("coordination_modes", {}).items():
            complexity_range = mode_config.get("complexity_range", [0, 1])
            agent_range = mode_config.get("agent_count", [1, 20])
            
            if (complexity_range[0] <= complexity <= complexity_range[1] and
                agent_range[0] <= agent_count_needed <= agent_range[1]):
                
                recommendations["coordination_mode"] = mode
                recommendations["reason"] = mode_config.get("description", "")
                break
        
        # Recommend swarm topology
        swarm_topologies = config.get("swarm_configuration", {}).get("topologies", {})
        for topology, topo_config in swarm_topologies.items():
            complexity_range = topo_config.get("complexity_range", [0, 1])
            ideal_size = topo_config.get("ideal_size", [1, 20])
            
            if (complexity_range[0] <= complexity <= complexity_range[1] and
                ideal_size[0] <= agent_count_needed <= ideal_size[1] and
                topo_config.get("time_critical") == time_critical):
                
                recommendations["swarm_topology"] = topology
                break
        
        # Recommend hive decision method
        if complexity > 0.7:
            recommendations["hive_decision_method"] = "emergent"
        elif time_critical:
            recommendations["hive_decision_method"] = "weighted_voting"
        elif agent_count_needed > 8:
            recommendations["hive_decision_method"] = "quorum"
        else:
            recommendations["hive_decision_method"] = "consensus"
        
        return recommendations
    
    def suggest_optimal_agents_for_swarm_hive(
        self, 
        required_capabilities: List[str],
        preferred_topology: str = "adaptive"
    ) -> Dict[str, List[str]]:
        """Suggest optimal agent composition for swarm-hive coordination"""
        
        config = self.swarm_hive_config
        role_mapping = config.get("agent_role_mapping", {})
        
        suggestions = {
            "queen_candidates": [],
            "specialists": [],
            "workers": [],
            "coordinators": []
        }
        
        # Find suitable agents for each role
        suitable_agents = self.find_agents_by_capabilities(required_capabilities)
        
        # Categorize agents by swarm-hive roles
        for agent_id in suitable_agents[:12]:  # Limit for performance
            if agent_id in role_mapping.get("queen_candidates", []):
                suggestions["queen_candidates"].append(agent_id)
            
            # Check if agent matches specialist categories
            agent_config = self.agent_registry.get(agent_id)
            if agent_config and agent_config.capabilities:
                domains = agent_config.capabilities.specialization_domains
                
                for domain in domains:
                    for spec_category, spec_agents in role_mapping.get("specialist_roles", {}).items():
                        if agent_id in spec_agents:
                            suggestions["specialists"].append(agent_id)
                            break
            
            # Check coordination capabilities
            if (agent_config and agent_config.capabilities and 
                "coordination" in agent_config.capabilities.specialization_domains):
                suggestions["coordinators"].append(agent_id)
            
            # Add to worker pool if not in other categories
            if (agent_id not in suggestions["queen_candidates"] and
                agent_id not in suggestions["specialists"] and
                agent_id not in suggestions["coordinators"]):
                suggestions["workers"].append(agent_id)
        
        # Remove duplicates and limit sizes
        for role in suggestions:
            suggestions[role] = list(dict.fromkeys(suggestions[role]))  # Remove duplicates
            if role == "queen_candidates":
                suggestions[role] = suggestions[role][:2]  # Max 2 queen candidates
            elif role == "specialists":
                suggestions[role] = suggestions[role][:6]  # Max 6 specialists
            elif role == "coordinators":
                suggestions[role] = suggestions[role][:3]  # Max 3 coordinators
            else:
                suggestions[role] = suggestions[role][:8]  # Max 8 workers
        
        return suggestions
    
    async def create_specialized_swarm_hive(
        self,
        task_type: str,
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create specialized swarm-hive for specific task types"""
        
        if not self.swarm_hive_coordinator:
            return {"error": "Swarm-hive coordinator not available"}
        
        config = self.swarm_hive_config
        task_templates = config.get("task_templates", {})
        
        if task_type not in task_templates:
            return {"error": f"Unknown task type: {task_type}"}
        
        template = task_templates[task_type]
        
        # Merge template with custom requirements
        requirements = dict(template)
        if custom_requirements:
            requirements.update(custom_requirements)
        
        # Find agents based on required capabilities
        agent_capabilities = requirements.get("agent_capabilities", [])
        suitable_agents = self.find_agents_by_capabilities(agent_capabilities)
        
        if not suitable_agents:
            return {"error": f"No suitable agents found for capabilities: {agent_capabilities}"}
        
        # Create persistent swarm-hive
        swarm_hive_id = f"{task_type}_{int(time.time())}"
        
        coordination_config = {
            "swarm_topology": requirements.get("preferred_topology", "adaptive"),
            "coordination_mode": requirements.get("coordination_mode", "adaptive_selection"),
            "task_type": task_type,
            "template": template
        }
        
        result = await self.swarm_hive_coordinator.create_persistent_swarm_hive(
            swarm_hive_id,
            suitable_agents[:10],  # Limit for performance
            coordination_config
        )
        
        self.logger.info(
            "specialized_swarm_hive_created",
            task_type=task_type,
            swarm_hive_id=swarm_hive_id,
            agents_used=len(suitable_agents[:10])
        )
        
        return result

# Example usage and testing
if __name__ == "__main__":
    async def main():
        # Initialize agent manager
        manager = AgentManager()
        
        # Example task requiring multiple agents
        task = {
            "type": "ios_app_development",
            "description": "Build a TreeAI mobile app with Claude integration",
            "requirements": ["ios", "ai", "forestry_business"],
            "complexity": 0.8
        }
        
        # Coordinate agents for the task
        result = await manager.coordinate_agents(task, ["ios", "ai", "forestry_business"])
        print("Coordination result:", json.dumps(result, indent=2))
        
        # Shutdown
        await manager.shutdown()
    
    asyncio.run(main())