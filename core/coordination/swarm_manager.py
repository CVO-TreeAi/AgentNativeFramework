"""
Swarm Intelligence Coordination System for AgentNativeFramework
Implements collective intelligence, hive-mind, and swarm coordination patterns
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path
import structlog
from prometheus_client import Counter, Histogram, Gauge

class SwarmTopology(Enum):
    HIERARCHICAL = "hierarchical"      # Queen-led coordination
    MESH = "mesh"                      # Peer-to-peer coordination  
    COLLECTIVE = "collective"          # Hive-mind coordination
    ADAPTIVE = "adaptive"              # Dynamic topology switching

class SwarmRole(Enum):
    QUEEN = "queen"                    # Leadership/oversight role
    WORKER = "worker"                  # Task execution role
    SCOUT = "scout"                    # Information gathering role
    COORDINATOR = "coordinator"        # Inter-swarm communication
    SPECIALIST = "specialist"          # Domain expertise role

@dataclass
class SwarmAgent:
    agent_id: str
    role: SwarmRole
    capabilities: List[str]
    load_capacity: float = 1.0
    current_load: float = 0.0
    trust_score: float = 0.8
    coordination_history: List[Dict] = field(default_factory=list)
    swarm_memberships: Set[str] = field(default_factory=set)

@dataclass
class SwarmState:
    swarm_id: str
    topology: SwarmTopology
    active_agents: Dict[str, SwarmAgent]
    task_queue: List[Dict[str, Any]]
    collective_memory: Dict[str, Any]
    consensus_threshold: float = 0.75
    health_score: float = 1.0
    created_at: float = field(default_factory=time.time)

class SwarmManager:
    """
    Manages swarm intelligence coordination across multiple agent collectives
    """
    
    # Metrics for swarm operations
    swarm_formations = Counter('swarm_formations_total', 'Total swarm formations', ['topology'])
    collective_decisions = Counter('collective_decisions_total', 'Collective decisions made', ['outcome'])
    swarm_efficiency = Histogram('swarm_efficiency_score', 'Swarm task completion efficiency')
    active_swarms_gauge = Gauge('active_swarms_count', 'Number of active swarms')
    consensus_time = Histogram('consensus_duration_seconds', 'Time to reach swarm consensus')
    
    def __init__(self, agent_manager=None):
        """Initialize swarm management system"""
        self.logger = structlog.get_logger(__name__)
        self.agent_manager = agent_manager
        
        # Swarm state management
        self.active_swarms: Dict[str, SwarmState] = {}
        self.global_memory: Dict[str, Any] = {}
        self.swarm_history: List[Dict[str, Any]] = []
        
        # Coordination patterns
        self.coordination_patterns = {
            SwarmTopology.HIERARCHICAL: self._hierarchical_coordination,
            SwarmTopology.MESH: self._mesh_coordination,
            SwarmTopology.COLLECTIVE: self._collective_coordination,
            SwarmTopology.ADAPTIVE: self._adaptive_coordination
        }
        
        self.logger.info("swarm_manager_initialized")
    
    async def create_swarm(
        self, 
        swarm_id: str, 
        topology: SwarmTopology,
        initial_agents: List[str],
        task_context: Dict[str, Any]
    ) -> SwarmState:
        """Create a new swarm with specified topology and agents"""
        
        if swarm_id in self.active_swarms:
            self.logger.warning("swarm_already_exists", swarm_id=swarm_id)
            return self.active_swarms[swarm_id]
        
        # Create swarm agents from available agents
        swarm_agents = {}
        for agent_id in initial_agents:
            if self.agent_manager and agent_id in self.agent_manager.agent_registry:
                agent_config = self.agent_manager.agent_registry[agent_id]
                
                # Determine optimal role based on agent capabilities
                role = self._determine_swarm_role(agent_config, topology)
                
                swarm_agent = SwarmAgent(
                    agent_id=agent_id,
                    role=role,
                    capabilities=agent_config.capabilities.specialization_domains if agent_config.capabilities else []
                )
                swarm_agents[agent_id] = swarm_agent
        
        # Create swarm state
        swarm_state = SwarmState(
            swarm_id=swarm_id,
            topology=topology,
            active_agents=swarm_agents,
            task_queue=[],
            collective_memory={"formation_context": task_context}
        )
        
        self.active_swarms[swarm_id] = swarm_state
        self.swarm_formations.labels(topology=topology.value).inc()
        self.active_swarms_gauge.set(len(self.active_swarms))
        
        self.logger.info(
            "swarm_created",
            swarm_id=swarm_id,
            topology=topology.value,
            agent_count=len(swarm_agents)
        )
        
        return swarm_state
    
    def _determine_swarm_role(self, agent_config, topology: SwarmTopology) -> SwarmRole:
        """Determine optimal role for agent in swarm based on capabilities and topology"""
        
        if not agent_config.capabilities:
            return SwarmRole.WORKER
        
        domains = agent_config.capabilities.specialization_domains
        
        # Role assignment logic based on topology and capabilities
        if topology == SwarmTopology.HIERARCHICAL:
            if agent_config.coordination_priority >= 90:
                return SwarmRole.QUEEN
            elif "orchestration" in domains or "coordination" in domains:
                return SwarmRole.COORDINATOR
            elif "research" in domains or "analysis" in domains:
                return SwarmRole.SCOUT
            else:
                return SwarmRole.SPECIALIST
        
        elif topology == SwarmTopology.MESH:
            if "coordination" in domains:
                return SwarmRole.COORDINATOR
            else:
                return SwarmRole.WORKER
        
        elif topology == SwarmTopology.COLLECTIVE:
            # In collective intelligence, all agents contribute equally
            return SwarmRole.WORKER
        
        else:  # ADAPTIVE
            return SwarmRole.COORDINATOR  # Can adapt roles dynamically
    
    async def coordinate_swarm_task(
        self, 
        swarm_id: str, 
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate task execution within a swarm using appropriate topology pattern"""
        
        if swarm_id not in self.active_swarms:
            return {"error": f"Swarm {swarm_id} not found"}
        
        swarm = self.active_swarms[swarm_id]
        
        # Add task to swarm queue
        task["task_id"] = f"{swarm_id}_{int(time.time())}"
        swarm.task_queue.append(task)
        
        start_time = time.time()
        
        try:
            # Use appropriate coordination pattern
            coordination_func = self.coordination_patterns[swarm.topology]
            result = await coordination_func(swarm, task)
            
            # Record coordination time
            coordination_duration = time.time() - start_time
            self.consensus_time.observe(coordination_duration)
            
            # Update swarm memory with results
            swarm.collective_memory[task["task_id"]] = {
                "result": result,
                "duration": coordination_duration,
                "participants": list(swarm.active_agents.keys()),
                "timestamp": time.time()
            }
            
            self.collective_decisions.labels(
                outcome="success" if result.get("status") == "completed" else "partial"
            ).inc()
            
            return result
            
        except Exception as e:
            self.logger.error("swarm_coordination_failed", swarm_id=swarm_id, error=str(e))
            self.collective_decisions.labels(outcome="failed").inc()
            return {"error": f"Swarm coordination failed: {e}"}
    
    async def _hierarchical_coordination(self, swarm: SwarmState, task: Dict[str, Any]) -> Dict[str, Any]:
        """Queen-led hierarchical coordination pattern"""
        
        # Find queen agent
        queen_agents = [agent for agent in swarm.active_agents.values() if agent.role == SwarmRole.QUEEN]
        
        if not queen_agents:
            # Promote highest priority agent to queen temporarily  
            sorted_agents = sorted(
                swarm.active_agents.values(),
                key=lambda a: len(a.capabilities),  # More capabilities = better queen
                reverse=True
            )
            queen_agent = sorted_agents[0] if sorted_agents else None
        else:
            queen_agent = queen_agents[0]
        
        if not queen_agent:
            return {"error": "No suitable queen agent found"}
        
        # Queen makes strategic decisions and delegates
        strategy = await self._generate_task_strategy(queen_agent, task)
        
        # Delegate subtasks to workers
        worker_agents = [agent for agent in swarm.active_agents.values() if agent.role in [SwarmRole.WORKER, SwarmRole.SPECIALIST]]
        
        delegation_results = []
        for subtask in strategy.get("subtasks", []):
            # Find best worker for subtask
            best_worker = self._find_best_worker(worker_agents, subtask)
            if best_worker:
                result = await self._execute_subtask(best_worker, subtask)
                delegation_results.append(result)
        
        # Queen integrates results
        final_result = await self._integrate_results(queen_agent, delegation_results, task)
        
        return {
            "status": "completed",
            "approach": "hierarchical",
            "queen_agent": queen_agent.agent_id,
            "workers_used": [r.get("worker_id") for r in delegation_results],
            "result": final_result
        }
    
    async def _mesh_coordination(self, swarm: SwarmState, task: Dict[str, Any]) -> Dict[str, Any]:
        """Peer-to-peer mesh coordination pattern"""
        
        agents = list(swarm.active_agents.values())
        
        # All agents propose solutions simultaneously
        proposals = []
        proposal_tasks = []
        
        for agent in agents:
            proposal_task = self._get_agent_proposal(agent, task)
            proposal_tasks.append(proposal_task)
        
        # Execute all proposals in parallel
        proposal_results = await asyncio.gather(*proposal_tasks, return_exceptions=True)
        
        for i, result in enumerate(proposal_results):
            if not isinstance(result, Exception):
                proposals.append({
                    "agent_id": agents[i].agent_id,
                    "proposal": result,
                    "trust_score": agents[i].trust_score
                })
        
        # Peer review and consensus building
        consensus_result = await self._build_mesh_consensus(proposals, task)
        
        return {
            "status": "completed",
            "approach": "mesh",
            "participating_agents": [p["agent_id"] for p in proposals],
            "consensus_score": consensus_result.get("consensus_score", 0),
            "result": consensus_result
        }
    
    async def _collective_coordination(self, swarm: SwarmState, task: Dict[str, Any]) -> Dict[str, Any]:
        """Hive-mind collective intelligence coordination pattern"""
        
        agents = list(swarm.active_agents.values())
        
        # Phase 1: Collective problem understanding
        understanding_tasks = [
            self._analyze_task_aspect(agent, task, aspect) 
            for agent in agents
            for aspect in ["requirements", "constraints", "opportunities", "risks"]
        ]
        
        understanding_results = await asyncio.gather(*understanding_tasks, return_exceptions=True)
        
        # Phase 2: Collective solution synthesis
        collective_knowledge = self._synthesize_collective_understanding(understanding_results)
        
        # Phase 3: Distributed execution with shared consciousness
        execution_tasks = []
        for agent in agents:
            agent_task = self._create_collective_subtask(agent, task, collective_knowledge)
            execution_tasks.append(self._execute_collective_task(agent, agent_task))
        
        execution_results = await asyncio.gather(*execution_tasks, return_exceptions=True)
        
        # Phase 4: Collective integration
        integrated_result = self._integrate_collective_results(execution_results, collective_knowledge)
        
        return {
            "status": "completed", 
            "approach": "collective",
            "collective_agents": [agent.agent_id for agent in agents],
            "shared_understanding": collective_knowledge,
            "collective_confidence": integrated_result.get("confidence", 0.8),
            "result": integrated_result
        }
    
    async def _adaptive_coordination(self, swarm: SwarmState, task: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptive coordination that switches topology based on task needs"""
        
        # Analyze task to determine optimal topology
        task_complexity = task.get("complexity", 0.5)
        agent_count = len(swarm.active_agents)
        time_constraints = task.get("time_critical", False)
        
        # Topology selection logic
        if task_complexity > 0.8 and not time_constraints:
            optimal_topology = SwarmTopology.COLLECTIVE  # Complex tasks benefit from collective intelligence
        elif agent_count > 5 and task_complexity > 0.5:
            optimal_topology = SwarmTopology.HIERARCHICAL  # Large teams need hierarchy
        elif time_constraints:
            optimal_topology = SwarmTopology.MESH  # Fast parallel execution
        else:
            optimal_topology = SwarmTopology.HIERARCHICAL  # Default fallback
        
        self.logger.info(
            "adaptive_topology_selected",
            swarm_id=swarm.swarm_id,
            selected_topology=optimal_topology.value,
            task_complexity=task_complexity,
            agent_count=agent_count
        )
        
        # Temporarily switch to optimal topology
        original_topology = swarm.topology
        swarm.topology = optimal_topology
        
        try:
            # Execute with optimal topology
            coordination_func = self.coordination_patterns[optimal_topology]
            result = await coordination_func(swarm, task)
            result["adaptive_topology_used"] = optimal_topology.value
            return result
        finally:
            # Restore original topology
            swarm.topology = original_topology
    
    async def _generate_task_strategy(self, queen_agent: SwarmAgent, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic approach for task (Queen agent logic)"""
        # In a full implementation, this would call the actual agent
        return {
            "approach": f"Strategic decomposition by {queen_agent.agent_id}",
            "subtasks": [
                {"id": "subtask_1", "type": "analysis", "priority": 1},
                {"id": "subtask_2", "type": "implementation", "priority": 2},
                {"id": "subtask_3", "type": "validation", "priority": 3}
            ],
            "estimated_effort": task.get("complexity", 0.5) * 10
        }
    
    def _find_best_worker(self, workers: List[SwarmAgent], subtask: Dict[str, Any]) -> Optional[SwarmAgent]:
        """Find the best worker agent for a specific subtask"""
        if not workers:
            return None
        
        # Score workers based on capabilities and load
        scored_workers = []
        for worker in workers:
            capability_score = 0
            required_caps = subtask.get("required_capabilities", [])
            
            for cap in required_caps:
                if cap in worker.capabilities:
                    capability_score += 1
            
            # Factor in current load (prefer less loaded agents)
            load_penalty = worker.current_load
            total_score = capability_score * worker.trust_score - load_penalty
            
            scored_workers.append((total_score, worker))
        
        # Return highest scoring worker
        scored_workers.sort(key=lambda x: x[0], reverse=True)
        return scored_workers[0][1] if scored_workers else workers[0]
    
    async def _execute_subtask(self, worker: SwarmAgent, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a subtask with a specific worker agent"""
        # Update worker load
        worker.current_load += 0.1
        
        # Simulate task execution
        await asyncio.sleep(0.1)  # Placeholder for actual execution
        
        result = {
            "worker_id": worker.agent_id,
            "subtask_id": subtask.get("id"),
            "status": "completed",
            "confidence": worker.trust_score,
            "output": f"Completed {subtask.get('type', 'task')} by {worker.agent_id}"
        }
        
        # Update worker load
        worker.current_load -= 0.1
        worker.current_load = max(0, worker.current_load)
        
        return result
    
    async def _integrate_results(self, queen_agent: SwarmAgent, results: List[Dict], task: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate subtask results (Queen agent logic)"""
        return {
            "integrated_by": queen_agent.agent_id,
            "subtask_count": len(results),
            "overall_confidence": sum(r.get("confidence", 0.5) for r in results) / len(results) if results else 0,
            "final_output": f"Integrated solution for {task.get('type', 'task')}"
        }
    
    async def _get_agent_proposal(self, agent: SwarmAgent, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get proposal from agent (peer-to-peer)"""
        await asyncio.sleep(0.05)  # Simulate thinking time
        return {
            "approach": f"{agent.agent_id} proposes solution using {', '.join(agent.capabilities)}",
            "confidence": agent.trust_score,
            "estimated_effort": len(agent.capabilities) * 2
        }
    
    async def _build_mesh_consensus(self, proposals: List[Dict], task: Dict[str, Any]) -> Dict[str, Any]:
        """Build consensus from peer proposals"""
        if not proposals:
            return {"error": "No proposals to build consensus from"}
        
        # Weight proposals by trust score
        total_trust = sum(p["trust_score"] for p in proposals)
        
        # Simple consensus: highest weighted confidence
        best_proposal = max(proposals, key=lambda p: p["proposal"]["confidence"] * p["trust_score"])
        
        consensus_score = (best_proposal["trust_score"] / total_trust) if total_trust > 0 else 0
        
        return {
            "selected_proposal": best_proposal["proposal"],
            "consensus_score": consensus_score,
            "contributing_agents": len(proposals)
        }
    
    async def _analyze_task_aspect(self, agent: SwarmAgent, task: Dict[str, Any], aspect: str) -> Dict[str, Any]:
        """Analyze specific aspect of task for collective intelligence"""
        await asyncio.sleep(0.02)  # Simulate analysis time
        return {
            "agent_id": agent.agent_id,
            "aspect": aspect,
            "analysis": f"Agent {agent.agent_id} analysis of {aspect} for task",
            "insights": [f"Insight about {aspect} from {cap}" for cap in agent.capabilities[:2]]
        }
    
    def _synthesize_collective_understanding(self, understanding_results: List) -> Dict[str, Any]:
        """Synthesize collective understanding from all agents"""
        valid_results = [r for r in understanding_results if not isinstance(r, Exception)]
        
        aspects = {}
        for result in valid_results:
            aspect = result.get("aspect")
            if aspect not in aspects:
                aspects[aspect] = []
            aspects[aspect].append(result)
        
        return {
            "collective_insights": aspects,
            "total_perspectives": len(valid_results),
            "synthesis_timestamp": time.time()
        }
    
    def _create_collective_subtask(self, agent: SwarmAgent, task: Dict[str, Any], collective_knowledge: Dict) -> Dict[str, Any]:
        """Create agent-specific subtask based on collective understanding"""
        return {
            "agent_id": agent.agent_id,
            "subtask": f"Execute aspect of {task.get('type', 'task')} using collective insights",
            "shared_knowledge": collective_knowledge,
            "agent_focus": agent.capabilities[0] if agent.capabilities else "general"
        }
    
    async def _execute_collective_task(self, agent: SwarmAgent, collective_task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task with collective consciousness"""
        await asyncio.sleep(0.1)  # Simulate execution
        return {
            "agent_id": agent.agent_id,
            "contribution": f"Collective contribution from {agent.agent_id}",
            "leveraged_insights": len(collective_task.get("shared_knowledge", {}).get("collective_insights", {}))
        }
    
    def _integrate_collective_results(self, results: List, collective_knowledge: Dict) -> Dict[str, Any]:
        """Integrate results from collective intelligence execution"""
        valid_results = [r for r in results if not isinstance(r, Exception)]
        
        return {
            "collective_solution": "Integrated solution from collective intelligence",
            "contributing_agents": len(valid_results),
            "collective_insights_used": len(collective_knowledge.get("collective_insights", {})),
            "confidence": 0.9  # High confidence from collective approach
        }
    
    async def dissolve_swarm(self, swarm_id: str) -> bool:
        """Dissolve a swarm and archive its memory"""
        if swarm_id not in self.active_swarms:
            return False
        
        swarm = self.active_swarms[swarm_id]
        
        # Archive swarm memory
        archive_entry = {
            "swarm_id": swarm_id,
            "topology": swarm.topology.value,
            "duration": time.time() - swarm.created_at,
            "final_memory": swarm.collective_memory,
            "agent_count": len(swarm.active_agents),
            "dissolved_at": time.time()
        }
        
        self.swarm_history.append(archive_entry)
        
        # Update global memory with learnings
        self.global_memory[f"swarm_{swarm_id}_learnings"] = {
            "topology_effectiveness": swarm.health_score,
            "successful_patterns": list(swarm.collective_memory.keys()),
            "agent_combinations": list(swarm.active_agents.keys())
        }
        
        # Remove from active swarms
        del self.active_swarms[swarm_id]
        self.active_swarms_gauge.set(len(self.active_swarms))
        
        self.logger.info("swarm_dissolved", swarm_id=swarm_id, archive_id=len(self.swarm_history))
        return True
    
    def get_swarm_status(self, swarm_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a swarm"""
        if swarm_id not in self.active_swarms:
            return None
        
        swarm = self.active_swarms[swarm_id]
        
        return {
            "swarm_id": swarm_id,
            "topology": swarm.topology.value,
            "agent_count": len(swarm.active_agents),
            "active_agents": [
                {
                    "agent_id": agent.agent_id,
                    "role": agent.role.value,
                    "load": agent.current_load,
                    "trust_score": agent.trust_score
                }
                for agent in swarm.active_agents.values()
            ],
            "task_queue_size": len(swarm.task_queue),
            "health_score": swarm.health_score,
            "uptime": time.time() - swarm.created_at,
            "memory_size": len(swarm.collective_memory)
        }
    
    def get_all_swarms_status(self) -> Dict[str, Any]:
        """Get status of all active swarms"""
        return {
            "active_swarms": len(self.active_swarms),
            "swarms": {
                swarm_id: self.get_swarm_status(swarm_id)
                for swarm_id in self.active_swarms.keys()
            },
            "historical_swarms": len(self.swarm_history),
            "global_memory_size": len(self.global_memory)
        }

# Example usage
if __name__ == "__main__":
    async def main():
        swarm_manager = SwarmManager()
        
        # Create a hierarchical swarm
        swarm = await swarm_manager.create_swarm(
            "test_swarm_1",
            SwarmTopology.HIERARCHICAL,
            ["project_supervisor_orchestrator", "ios_developer", "ai_engineer"],
            {"task_type": "app_development", "complexity": 0.7}
        )
        
        # Execute a task
        task = {
            "type": "build_ios_app",
            "description": "Build AI-powered forestry app",
            "complexity": 0.8,
            "time_critical": False
        }
        
        result = await swarm_manager.coordinate_swarm_task("test_swarm_1", task)
        print("Swarm coordination result:", json.dumps(result, indent=2))
        
        # Check swarm status
        status = swarm_manager.get_swarm_status("test_swarm_1")
        print("Swarm status:", json.dumps(status, indent=2))
        
        # Dissolve swarm
        await swarm_manager.dissolve_swarm("test_swarm_1")
        
    asyncio.run(main())