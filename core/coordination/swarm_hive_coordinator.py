"""
Swarm-Hive Integration Coordinator for AgentNativeFramework
Integrates swarm intelligence and hive mind functionality with agent management
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging
import structlog
from prometheus_client import Counter, Histogram, Gauge

from .swarm_manager import SwarmManager, SwarmTopology, SwarmState
from .hive_intelligence import HiveIntelligence, HiveDecisionMethod, HiveMemoryType
from ..agents.agent_manager import AgentManager

class CoordinationMode(Enum):
    SWARM_ONLY = "swarm_only"           # Pure swarm coordination
    HIVE_ONLY = "hive_only"             # Pure hive intelligence
    SWARM_HIVE_HYBRID = "hybrid"        # Combined approach
    ADAPTIVE_SELECTION = "adaptive"     # Auto-select best mode

@dataclass
class CoordinationTask:
    task_id: str
    description: str
    complexity: float
    required_capabilities: List[str]
    time_critical: bool = False
    coordination_mode: Optional[CoordinationMode] = None
    metadata: Dict[str, Any] = None

class SwarmHiveCoordinator:
    """
    Master coordinator that integrates swarm intelligence with hive mind capabilities
    """
    
    # Metrics
    coordination_requests = Counter('coordination_requests_total', 'Coordination requests', ['mode'])
    coordination_success = Counter('coordination_success_total', 'Successful coordinations', ['mode'])
    hybrid_decisions = Counter('hybrid_decisions_total', 'Hybrid mode decisions', ['primary_mode'])
    coordination_efficiency = Histogram('coordination_efficiency_score', 'Coordination efficiency')
    
    def __init__(self, agent_manager: Optional[AgentManager] = None):
        """Initialize the swarm-hive coordinator"""
        self.logger = structlog.get_logger(__name__)
        
        # Core components
        self.agent_manager = agent_manager or AgentManager()
        self.swarm_manager = SwarmManager(self.agent_manager)
        self.hive_intelligence = HiveIntelligence(self.swarm_manager)
        
        # Coordination state
        self.active_coordinations: Dict[str, CoordinationTask] = {}
        self.coordination_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {}
        
        # Configuration
        self.hybrid_threshold = 0.7  # Complexity threshold for hybrid mode
        self.adaptive_learning_rate = 0.1
        
        self.logger.info("swarm_hive_coordinator_initialized")
    
    async def coordinate_task(
        self, 
        task: CoordinationTask,
        preferred_agents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Main coordination entry point"""
        
        start_time = time.time()
        self.active_coordinations[task.task_id] = task
        
        try:
            # Determine optimal coordination mode
            if not task.coordination_mode or task.coordination_mode == CoordinationMode.ADAPTIVE_SELECTION:
                coordination_mode = await self._select_coordination_mode(task)
            else:
                coordination_mode = task.coordination_mode
            
            self.coordination_requests.labels(mode=coordination_mode.value).inc()
            
            # Execute coordination based on selected mode
            if coordination_mode == CoordinationMode.SWARM_ONLY:
                result = await self._coordinate_swarm_only(task, preferred_agents)
            elif coordination_mode == CoordinationMode.HIVE_ONLY:
                result = await self._coordinate_hive_only(task, preferred_agents)
            elif coordination_mode == CoordinationMode.SWARM_HIVE_HYBRID:
                result = await self._coordinate_hybrid(task, preferred_agents)
            else:
                result = {"error": f"Unknown coordination mode: {coordination_mode}"}
            
            # Record results
            coordination_time = time.time() - start_time
            self.coordination_efficiency.observe(result.get("efficiency_score", 0.5))
            
            if result.get("status") == "success":
                self.coordination_success.labels(mode=coordination_mode.value).inc()
            
            # Store coordination history
            self.coordination_history.append({
                "task_id": task.task_id,
                "mode": coordination_mode.value,
                "duration": coordination_time,
                "result": result,
                "timestamp": time.time()
            })
            
            # Update performance metrics
            await self._update_performance_metrics(coordination_mode, result, coordination_time)
            
            return {
                "task_id": task.task_id,
                "coordination_mode": coordination_mode.value,
                "duration": coordination_time,
                "result": result
            }
            
        except Exception as e:
            self.logger.error("coordination_failed", task_id=task.task_id, error=str(e))
            return {"error": f"Coordination failed: {e}"}
        finally:
            # Clean up
            if task.task_id in self.active_coordinations:
                del self.active_coordinations[task.task_id]
    
    async def _select_coordination_mode(self, task: CoordinationTask) -> CoordinationMode:
        """Adaptively select the best coordination mode for the task"""
        
        # Decision factors
        complexity = task.complexity
        agent_count_needed = len(task.required_capabilities)
        time_critical = task.time_critical
        
        # Historical performance
        swarm_performance = self.performance_metrics.get("swarm_avg_efficiency", 0.5)
        hive_performance = self.performance_metrics.get("hive_avg_efficiency", 0.5)
        hybrid_performance = self.performance_metrics.get("hybrid_avg_efficiency", 0.5)
        
        # Selection logic
        if complexity > self.hybrid_threshold and not time_critical:
            # Complex, non-urgent tasks benefit from hybrid approach
            selected_mode = CoordinationMode.SWARM_HIVE_HYBRID
            
        elif time_critical and agent_count_needed <= 5:
            # Time-critical tasks with few agents: use swarm for speed
            selected_mode = CoordinationMode.SWARM_ONLY
            
        elif agent_count_needed > 8:
            # Large teams benefit from hive intelligence
            selected_mode = CoordinationMode.HIVE_ONLY
            
        elif complexity < 0.3:
            # Simple tasks: use fastest mode based on history
            if swarm_performance >= hive_performance:
                selected_mode = CoordinationMode.SWARM_ONLY
            else:
                selected_mode = CoordinationMode.HIVE_ONLY
        else:
            # Default to hybrid for moderate complexity
            selected_mode = CoordinationMode.SWARM_HIVE_HYBRID
        
        self.logger.info(
            "coordination_mode_selected",
            task_id=task.task_id,
            mode=selected_mode.value,
            complexity=complexity,
            agent_count=agent_count_needed,
            time_critical=time_critical
        )
        
        return selected_mode
    
    async def _coordinate_swarm_only(self, task: CoordinationTask, preferred_agents: Optional[List[str]]) -> Dict[str, Any]:
        """Pure swarm coordination approach"""
        
        # Determine optimal swarm topology
        if task.complexity > 0.8:
            topology = SwarmTopology.COLLECTIVE  # Complex tasks need collective intelligence
        elif task.time_critical:
            topology = SwarmTopology.MESH  # Fast parallel execution
        elif len(task.required_capabilities) > 6:
            topology = SwarmTopology.HIERARCHICAL  # Large teams need hierarchy
        else:
            topology = SwarmTopology.ADAPTIVE  # Let swarm adapt
        
        # Select agents
        if preferred_agents:
            selected_agents = preferred_agents
        else:
            selected_agents = self.agent_manager.find_agents_by_capabilities(task.required_capabilities)
        
        # Create swarm
        swarm_id = f"swarm_{task.task_id}"
        swarm = await self.swarm_manager.create_swarm(
            swarm_id,
            topology,
            selected_agents[:8],  # Limit swarm size for performance
            {"task": task.description, "complexity": task.complexity}
        )
        
        # Execute task
        swarm_task = {
            "type": task.description,
            "complexity": task.complexity,
            "time_critical": task.time_critical,
            "required_capabilities": task.required_capabilities
        }
        
        result = await self.swarm_manager.coordinate_swarm_task(swarm_id, swarm_task)
        
        # Clean up swarm
        await self.swarm_manager.dissolve_swarm(swarm_id)
        
        return {
            "status": "success",
            "approach": "swarm_only",
            "topology_used": topology.value,
            "agents_used": len(selected_agents),
            "swarm_result": result,
            "efficiency_score": result.get("consensus_confidence", 0.5)
        }
    
    async def _coordinate_hive_only(self, task: CoordinationTask, preferred_agents: Optional[List[str]]) -> Dict[str, Any]:
        """Pure hive intelligence approach"""
        
        # Select agents and initialize hive nodes
        if preferred_agents:
            selected_agents = preferred_agents
        else:
            selected_agents = self.agent_manager.find_agents_by_capabilities(task.required_capabilities)
        
        # Initialize hive nodes for agents
        hive_nodes = []
        for agent_id in selected_agents[:10]:  # Limit for performance
            if agent_id in self.agent_manager.agent_registry:
                agent_config = self.agent_manager.agent_registry[agent_id]
                capabilities = agent_config.capabilities.specialization_domains if agent_config.capabilities else []
                
                node = await self.hive_intelligence.initialize_hive_node(agent_id, capabilities)
                hive_nodes.append(node)
        
        # Store task context in collective memory
        memory_id = await self.hive_intelligence.store_collective_memory(
            {
                "task_description": task.description,
                "required_capabilities": task.required_capabilities,
                "complexity": task.complexity
            },
            HiveMemoryType.WORKING,
            set(node.agent_id for node in hive_nodes),
            confidence=0.8
        )
        
        # Create decision options based on task
        decision_options = await self._generate_hive_decision_options(task)
        
        # Initiate hive decision
        decision_method = self._select_hive_decision_method(task)
        decision_id = await self.hive_intelligence.initiate_hive_decision(
            f"How should we approach: {task.description}",
            decision_options,
            decision_method,
            timeout_seconds=120 if task.time_critical else 300
        )
        
        # Wait for decision resolution
        max_wait = 130 if task.time_critical else 310
        decision_result = await self._wait_for_hive_decision(decision_id, max_wait)
        
        return {
            "status": "success",
            "approach": "hive_only",
            "decision_method": decision_method.value,
            "nodes_participated": len(hive_nodes),
            "hive_result": decision_result,
            "memory_id": memory_id,
            "efficiency_score": decision_result.get("confidence", 0.5)
        }
    
    async def _coordinate_hybrid(self, task: CoordinationTask, preferred_agents: Optional[List[str]]) -> Dict[str, Any]:
        """Hybrid swarm-hive coordination approach"""
        
        # Phase 1: Hive intelligence for strategic planning
        self.hybrid_decisions.labels(primary_mode="hive_planning").inc()
        
        hive_planning_task = CoordinationTask(
            task_id=f"{task.task_id}_hive_planning",
            description=f"Strategic planning for: {task.description}",
            complexity=task.complexity * 0.7,  # Planning is typically less complex than execution
            required_capabilities=["coordination", "planning"] + task.required_capabilities[:3]
        )
        
        hive_result = await self._coordinate_hive_only(hive_planning_task, preferred_agents)
        
        # Phase 2: Swarm execution based on hive strategy
        self.hybrid_decisions.labels(primary_mode="swarm_execution").inc()
        
        swarm_execution_task = CoordinationTask(
            task_id=f"{task.task_id}_swarm_execution",
            description=f"Execute plan for: {task.description}",
            complexity=task.complexity,
            required_capabilities=task.required_capabilities,
            time_critical=task.time_critical
        )
        
        # Use hive insights to inform swarm coordination
        swarm_task_metadata = {
            "hive_strategy": hive_result.get("hive_result"),
            "strategic_insights": hive_result.get("memory_id")
        }
        swarm_execution_task.metadata = swarm_task_metadata
        
        swarm_result = await self._coordinate_swarm_only(swarm_execution_task, preferred_agents)
        
        # Phase 3: Hive validation and learning
        validation_insights = await self._hive_validate_swarm_results(hive_result, swarm_result, task)
        
        return {
            "status": "success",
            "approach": "swarm_hive_hybrid",
            "phases": {
                "hive_planning": hive_result,
                "swarm_execution": swarm_result,
                "hive_validation": validation_insights
            },
            "efficiency_score": (
                hive_result.get("efficiency_score", 0.5) * 0.3 +
                swarm_result.get("efficiency_score", 0.5) * 0.5 +
                validation_insights.get("validation_confidence", 0.5) * 0.2
            )
        }
    
    async def _generate_hive_decision_options(self, task: CoordinationTask) -> List[Dict[str, Any]]:
        """Generate decision options for hive intelligence"""
        
        options = [
            {
                "id": "parallel_approach",
                "description": "Parallel execution with multiple agents",
                "required_expertise": [0, 1, 2],  # Development, coordination, analysis
                "estimated_effort": task.complexity * 0.8,
                "time_estimate": "fast"
            },
            {
                "id": "sequential_approach", 
                "description": "Sequential handoff between specialists",
                "required_expertise": [1, 3, 4],  # Coordination, domain expertise, validation
                "estimated_effort": task.complexity * 1.2,
                "time_estimate": "thorough"
            },
            {
                "id": "hybrid_approach",
                "description": "Mix of parallel and sequential coordination",
                "required_expertise": [0, 1, 2, 3],  # Broad expertise needed
                "estimated_effort": task.complexity * 1.0,
                "time_estimate": "balanced"
            }
        ]
        
        # Add task-specific options based on capabilities
        if "ai" in task.required_capabilities:
            options.append({
                "id": "ai_assisted_approach",
                "description": "AI-first approach with human oversight",
                "required_expertise": [5, 1],  # AI/ML + coordination
                "estimated_effort": task.complexity * 0.6,
                "time_estimate": "efficient"
            })
        
        return options
    
    def _select_hive_decision_method(self, task: CoordinationTask) -> HiveDecisionMethod:
        """Select appropriate hive decision method based on task characteristics"""
        
        if task.time_critical:
            return HiveDecisionMethod.WEIGHTED_VOTING  # Fast weighted decisions
        elif task.complexity > 0.8:
            return HiveDecisionMethod.EMERGENT  # Let complex patterns emerge
        elif len(task.required_capabilities) > 6:
            return HiveDecisionMethod.QUORUM  # Ensure sufficient participation
        else:
            return HiveDecisionMethod.CONSENSUS  # Default consensus building
    
    async def _wait_for_hive_decision(self, decision_id: str, max_wait_seconds: int) -> Dict[str, Any]:
        """Wait for hive decision to be resolved"""
        
        wait_time = 0
        check_interval = 1.0
        
        while wait_time < max_wait_seconds:
            # Check if decision is resolved
            if decision_id not in self.hive_intelligence.active_decisions:
                # Decision is resolved, find it in history
                for decision in self.hive_intelligence.decision_history:
                    if decision.decision_id == decision_id:
                        return {
                            "decision_id": decision_id,
                            "consensus_reached": decision.consensus_reached,
                            "confidence": decision.confidence,
                            "method_used": decision.method.value,
                            "participants": len(decision.participants)
                        }
                break
            
            await asyncio.sleep(check_interval)
            wait_time += check_interval
        
        # Decision not resolved in time
        return {
            "decision_id": decision_id,
            "timeout": True,
            "consensus_reached": False,
            "confidence": 0.0
        }
    
    async def _hive_validate_swarm_results(
        self, 
        hive_result: Dict[str, Any],
        swarm_result: Dict[str, Any], 
        original_task: CoordinationTask
    ) -> Dict[str, Any]:
        """Use hive intelligence to validate swarm execution results"""
        
        # Create validation context
        validation_context = {
            "original_task": original_task.description,
            "hive_strategy": hive_result.get("hive_result"),
            "swarm_execution": swarm_result.get("swarm_result"),
            "complexity_match": abs(original_task.complexity - swarm_result.get("efficiency_score", 0))
        }
        
        # Store validation memory
        validation_memory_id = await self.hive_intelligence.store_collective_memory(
            validation_context,
            HiveMemoryType.EPISODIC,
            {"validation_hive"},  # Virtual validation node
            confidence=0.9
        )
        
        # Calculate validation metrics
        strategy_execution_alignment = min(1.0, 
            1.0 - abs(
                hive_result.get("efficiency_score", 0.5) - 
                swarm_result.get("efficiency_score", 0.5)
            )
        )
        
        return {
            "validation_memory_id": validation_memory_id,
            "strategy_execution_alignment": strategy_execution_alignment,
            "validation_confidence": strategy_execution_alignment * 0.9,
            "learnings": {
                "hive_strategy_effectiveness": hive_result.get("efficiency_score", 0.5),
                "swarm_execution_efficiency": swarm_result.get("efficiency_score", 0.5),
                "hybrid_synergy": strategy_execution_alignment
            }
        }
    
    async def _update_performance_metrics(
        self, 
        mode: CoordinationMode, 
        result: Dict[str, Any], 
        duration: float
    ):
        """Update performance metrics for adaptive learning"""
        
        efficiency_score = result.get("efficiency_score", 0.5)
        
        # Update mode-specific metrics
        mode_key = f"{mode.value}_avg_efficiency"
        
        if mode_key not in self.performance_metrics:
            self.performance_metrics[mode_key] = efficiency_score
        else:
            # Exponential moving average
            old_avg = self.performance_metrics[mode_key]
            self.performance_metrics[mode_key] = (
                old_avg * (1 - self.adaptive_learning_rate) + 
                efficiency_score * self.adaptive_learning_rate
            )
        
        # Update timing metrics
        timing_key = f"{mode.value}_avg_duration"
        if timing_key not in self.performance_metrics:
            self.performance_metrics[timing_key] = duration
        else:
            old_avg = self.performance_metrics[timing_key]
            self.performance_metrics[timing_key] = (
                old_avg * (1 - self.adaptive_learning_rate) +
                duration * self.adaptive_learning_rate
            )
    
    async def create_persistent_swarm_hive(
        self, 
        swarm_hive_id: str,
        agent_ids: List[str],
        coordination_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a persistent swarm-hive that can handle multiple tasks"""
        
        # Create persistent swarm
        swarm_topology = SwarmTopology(coordination_config.get("swarm_topology", "adaptive"))
        swarm = await self.swarm_manager.create_swarm(
            f"persistent_{swarm_hive_id}",
            swarm_topology,
            agent_ids,
            coordination_config
        )
        
        # Initialize hive nodes for all agents
        hive_nodes = []
        for agent_id in agent_ids:
            if agent_id in self.agent_manager.agent_registry:
                agent_config = self.agent_manager.agent_registry[agent_id]
                capabilities = agent_config.capabilities.specialization_domains if agent_config.capabilities else []
                
                node = await self.hive_intelligence.initialize_hive_node(agent_id, capabilities)
                hive_nodes.append(node)
        
        # Store formation in collective memory
        formation_memory = await self.hive_intelligence.store_collective_memory(
            {
                "swarm_hive_id": swarm_hive_id,
                "formation_time": time.time(),
                "agent_composition": agent_ids,
                "configuration": coordination_config
            },
            HiveMemoryType.EPISODIC,
            set(agent_ids),
            confidence=1.0
        )
        
        self.logger.info(
            "persistent_swarm_hive_created",
            swarm_hive_id=swarm_hive_id,
            agents=len(agent_ids),
            swarm_id=swarm.swarm_id
        )
        
        return {
            "swarm_hive_id": swarm_hive_id,
            "swarm_id": swarm.swarm_id,
            "hive_nodes": len(hive_nodes),
            "formation_memory_id": formation_memory,
            "status": "active"
        }
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination system status"""
        
        swarm_status = self.swarm_manager.get_all_swarms_status()
        hive_status = self.hive_intelligence.get_hive_status()
        
        return {
            "coordinator": {
                "active_coordinations": len(self.active_coordinations),
                "coordination_history": len(self.coordination_history),
                "performance_metrics": self.performance_metrics
            },
            "swarm_manager": swarm_status,
            "hive_intelligence": hive_status,
            "system_health": {
                "swarm_efficiency": self.performance_metrics.get("swarm_avg_efficiency", 0.5),
                "hive_efficiency": self.performance_metrics.get("hive_avg_efficiency", 0.5),
                "hybrid_efficiency": self.performance_metrics.get("hybrid_avg_efficiency", 0.5)
            }
        }

# Example usage and integration test
if __name__ == "__main__":
    async def main():
        # Initialize coordinator
        coordinator = SwarmHiveCoordinator()
        
        # Example complex task
        task = CoordinationTask(
            task_id="test_coordination_1",
            description="Build AI-powered forestry assessment system",
            complexity=0.8,
            required_capabilities=["ai", "forestry", "ios", "backend"],
            time_critical=False
        )
        
        # Execute coordination
        result = await coordinator.coordinate_task(task)
        print("Coordination result:", json.dumps(result, indent=2))
        
        # Check system status
        status = coordinator.get_coordination_status()
        print("System status:", json.dumps(status, indent=2))
        
    asyncio.run(main())