"""
Daemon Bridge for AgentNativeFramework
Connects Python agent management with Rust daemon for swarm/hive coordination
"""

import asyncio
import json
import socket
import time
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import structlog

from .agents.agent_manager import AgentManager
from .coordination.swarm_hive_coordinator import SwarmHiveCoordinator, CoordinationTask, CoordinationMode

class DaemonBridge:
    """
    Bridge between Rust daemon and Python agent coordination system
    """
    
    def __init__(self, socket_path: str = "/tmp/anf_python.sock"):
        self.logger = structlog.get_logger(__name__)
        self.socket_path = socket_path
        
        # Initialize core components
        self.coordinator = SwarmHiveCoordinator()
        self.agent_manager = AgentManager(swarm_hive_coordinator=self.coordinator)
        
        # Active operations
        self.active_swarms: Dict[str, Any] = {}
        self.active_hive_operations: Dict[str, Any] = {}
        self.running = False
        
        self.logger.info("daemon_bridge_initialized", socket_path=socket_path)
    
    async def start(self):
        """Start the daemon bridge"""
        self.running = True
        
        # Ensure socket directory exists
        socket_dir = Path(self.socket_path).parent
        socket_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove existing socket if it exists
        if Path(self.socket_path).exists():
            Path(self.socket_path).unlink()
        
        # Start Unix socket server
        server = await asyncio.start_unix_server(
            self.handle_client,
            path=self.socket_path
        )
        
        self.logger.info("daemon_bridge_started", socket=self.socket_path)
        
        async with server:
            await server.serve_forever()
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle client connections from Rust daemon"""
        try:
            while not reader.at_eof():
                # Read command from client
                data = await reader.readline()
                if not data:
                    break
                
                try:
                    command = json.loads(data.decode().strip())
                    response = await self.process_command(command)
                    
                    # Send response back
                    response_data = json.dumps(response) + "\n"
                    writer.write(response_data.encode())
                    await writer.drain()
                    
                except json.JSONDecodeError:
                    error_response = {"error": "Invalid JSON command"}
                    writer.write(json.dumps(error_response).encode() + b"\n")
                    await writer.drain()
                    
        except Exception as e:
            self.logger.error("client_handler_error", error=str(e))
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def process_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Process commands from the Rust daemon"""
        
        action = command.get("action")
        params = command.get("params", {})
        
        self.logger.info("processing_command", action=action, params=params)
        
        try:
            if action == "swarm_create":
                return await self.handle_swarm_create(params)
            elif action == "swarm_execute":
                return await self.handle_swarm_execute(params)
            elif action == "swarm_status":
                return await self.handle_swarm_status(params)
            elif action == "swarm_dissolve":
                return await self.handle_swarm_dissolve(params)
            elif action == "swarm_list":
                return await self.handle_swarm_list(params)
                
            elif action == "hive_init":
                return await self.handle_hive_init(params)
            elif action == "hive_decide":
                return await self.handle_hive_decide(params)
            elif action == "hive_remember":
                return await self.handle_hive_remember(params)
            elif action == "hive_recall":
                return await self.handle_hive_recall(params)
            elif action == "hive_status":
                return await self.handle_hive_status(params)
                
            elif action == "collaborate":
                return await self.handle_collaborate(params)
            elif action == "agent_list":
                return await self.handle_agent_list(params)
            elif action == "agent_info":
                return await self.handle_agent_info(params)
                
            else:
                return {"error": f"Unknown action: {action}"}
                
        except Exception as e:
            self.logger.error("command_processing_error", action=action, error=str(e))
            return {"error": f"Command processing failed: {str(e)}"}
    
    # Swarm coordination handlers
    async def handle_swarm_create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm creation"""
        swarm_id = params.get("id", f"swarm_{int(time.time())}")
        topology = params.get("topology", "adaptive")
        agents = params.get("agents", [])
        task_description = params.get("task", "")
        
        # Map string topology to enum
        from .coordination.swarm_manager import SwarmTopology
        topology_map = {
            "hierarchical": SwarmTopology.HIERARCHICAL,
            "mesh": SwarmTopology.MESH,
            "collective": SwarmTopology.COLLECTIVE,
            "adaptive": SwarmTopology.ADAPTIVE
        }
        
        swarm_topology = topology_map.get(topology, SwarmTopology.ADAPTIVE)
        
        # Create swarm
        swarm = await self.coordinator.swarm_manager.create_swarm(
            swarm_id,
            swarm_topology,
            agents,
            {"description": task_description, "created_via": "cli"}
        )
        
        self.active_swarms[swarm_id] = swarm
        
        return {
            "success": True,
            "swarm_id": swarm_id,
            "topology": topology,
            "agents": len(agents),
            "status": "created"
        }
    
    async def handle_swarm_execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm task execution"""
        swarm_id = params.get("swarm_id")
        task_description = params.get("task", "")
        timeout = params.get("timeout", 300)
        
        if swarm_id not in self.active_swarms:
            return {"error": f"Swarm {swarm_id} not found"}
        
        # Execute task with swarm
        task = {
            "type": "cli_task",
            "description": task_description,
            "complexity": 0.7,
            "time_critical": False
        }
        
        result = await self.coordinator.swarm_manager.coordinate_swarm_task(swarm_id, task)
        
        return {
            "success": True,
            "swarm_id": swarm_id,
            "task": task_description,
            "result": result
        }
    
    async def handle_swarm_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm status request"""
        swarm_id = params.get("swarm_id")
        
        if swarm_id not in self.active_swarms:
            return {"error": f"Swarm {swarm_id} not found"}
        
        status = self.coordinator.swarm_manager.get_swarm_status(swarm_id)
        
        if status:
            return {
                "success": True,
                "status": status
            }
        else:
            return {"error": f"Failed to get status for swarm {swarm_id}"}
    
    async def handle_swarm_dissolve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm dissolution"""
        swarm_id = params.get("swarm_id")
        save_results = params.get("save_results", False)
        
        if swarm_id not in self.active_swarms:
            return {"error": f"Swarm {swarm_id} not found"}
        
        success = await self.coordinator.swarm_manager.dissolve_swarm(swarm_id)
        
        if success:
            del self.active_swarms[swarm_id]
            return {
                "success": True,
                "swarm_id": swarm_id,
                "results_saved": save_results
            }
        else:
            return {"error": f"Failed to dissolve swarm {swarm_id}"}
    
    async def handle_swarm_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm list request"""
        detailed = params.get("detailed", False)
        
        swarms = []
        for swarm_id, swarm in self.active_swarms.items():
            swarm_info = {
                "id": swarm_id,
                "topology": swarm.topology.value,
                "agents": len(swarm.active_agents),
                "status": "active"
            }
            
            if detailed:
                status = self.coordinator.swarm_manager.get_swarm_status(swarm_id)
                if status:
                    swarm_info.update(status)
            
            swarms.append(swarm_info)
        
        return {
            "success": True,
            "swarms": swarms,
            "total": len(swarms)
        }
    
    # Hive intelligence handlers
    async def handle_hive_init(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hive node initialization"""
        agents = params.get("agents", [])
        capabilities = params.get("capabilities", [])
        
        nodes_created = []
        
        for agent_id in agents:
            # Get agent capabilities from registry
            if agent_id in self.agent_manager.agent_registry:
                agent_config = self.agent_manager.agent_registry[agent_id]
                agent_capabilities = agent_config.capabilities.specialization_domains if agent_config.capabilities else capabilities
            else:
                agent_capabilities = capabilities
            
            # Create hive node
            node = await self.coordinator.hive_intelligence.initialize_hive_node(
                agent_id, 
                agent_capabilities
            )
            nodes_created.append(node.node_id)
        
        return {
            "success": True,
            "nodes_created": len(nodes_created),
            "node_ids": nodes_created
        }
    
    async def handle_hive_decide(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hive collective decision"""
        question = params.get("question", "")
        options = params.get("options", [])
        method = params.get("method", "consensus")
        timeout = params.get("timeout", 300)
        
        # Convert options to decision format
        decision_options = []
        for i, option in enumerate(options):
            decision_options.append({
                "id": f"option_{i}",
                "description": option,
                "required_expertise": [i % 3]  # Simple distribution
            })
        
        # Map method string to enum
        from .coordination.hive_intelligence import HiveDecisionMethod
        method_map = {
            "consensus": HiveDecisionMethod.CONSENSUS,
            "weighted": HiveDecisionMethod.WEIGHTED_VOTING,
            "quorum": HiveDecisionMethod.QUORUM,
            "emergent": HiveDecisionMethod.EMERGENT
        }
        
        decision_method = method_map.get(method, HiveDecisionMethod.CONSENSUS)
        
        # Initiate decision
        decision_id = await self.coordinator.hive_intelligence.initiate_hive_decision(
            question,
            decision_options,
            decision_method,
            timeout_seconds=timeout
        )
        
        self.active_hive_operations[decision_id] = {
            "type": "decision",
            "question": question,
            "started_at": time.time()
        }
        
        return {
            "success": True,
            "decision_id": decision_id,
            "question": question,
            "options": len(decision_options),
            "method": method
        }
    
    async def handle_hive_remember(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle collective memory storage"""
        content = params.get("content", "")
        memory_type = params.get("memory_type", "semantic")
        contributors = params.get("contributors", [])
        confidence = params.get("confidence", 0.8)
        
        # Map memory type string to enum
        from .coordination.hive_intelligence import HiveMemoryType
        type_map = {
            "working": HiveMemoryType.WORKING,
            "episodic": HiveMemoryType.EPISODIC,
            "semantic": HiveMemoryType.SEMANTIC,
            "collective": HiveMemoryType.COLLECTIVE
        }
        
        mem_type = type_map.get(memory_type, HiveMemoryType.SEMANTIC)
        
        # Store memory
        memory_id = await self.coordinator.hive_intelligence.store_collective_memory(
            content,
            mem_type,
            set(contributors),
            confidence
        )
        
        return {
            "success": True,
            "memory_id": memory_id,
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "type": memory_type,
            "contributors": len(contributors)
        }
    
    async def handle_hive_recall(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle collective memory recall"""
        query = params.get("query", "")
        memory_type = params.get("memory_type")
        min_confidence = params.get("min_confidence", 0.5)
        
        # Map memory type if specified
        mem_type = None
        if memory_type:
            from .coordination.hive_intelligence import HiveMemoryType
            type_map = {
                "working": HiveMemoryType.WORKING,
                "episodic": HiveMemoryType.EPISODIC,
                "semantic": HiveMemoryType.SEMANTIC,
                "collective": HiveMemoryType.COLLECTIVE
            }
            mem_type = type_map.get(memory_type)
        
        # Recall memories
        memories = await self.coordinator.hive_intelligence.recall_collective_memory(
            query,
            mem_type,
            min_confidence
        )
        
        # Format results
        results = []
        for memory in memories[:10]:  # Limit to top 10
            results.append({
                "fragment_id": memory.fragment_id,
                "content_preview": str(memory.content)[:200] + "..." if len(str(memory.content)) > 200 else str(memory.content),
                "confidence": memory.confidence_score,
                "type": memory.memory_type.value,
                "contributors": len(memory.contributors),
                "access_count": memory.access_count
            })
        
        return {
            "success": True,
            "query": query,
            "memories_found": len(results),
            "results": results
        }
    
    async def handle_hive_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hive status request"""
        show_nodes = params.get("nodes", False)
        show_memory = params.get("memory", False)
        show_decisions = params.get("decisions", False)
        
        status = self.coordinator.hive_intelligence.get_hive_status()
        
        # Add additional details if requested
        if show_nodes or show_memory or show_decisions:
            if show_nodes:
                status["node_details"] = [
                    {
                        "node_id": node.node_id,
                        "agent_id": node.agent_id,
                        "connections": len(node.connections),
                        "influence_score": node.influence_score
                    }
                    for node in list(self.coordinator.hive_intelligence.nodes.values())[:10]
                ]
        
        return {
            "success": True,
            "status": status
        }
    
    # General handlers
    async def handle_collaborate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle multi-agent collaboration"""
        task_description = params.get("task", "")
        agents = params.get("agents", "").split(",") if params.get("agents") else []
        mode = params.get("mode", "adaptive_selection")
        topology = params.get("topology", "adaptive")
        
        # Create coordination task
        coordination_task = CoordinationTask(
            task_id=f"cli_collaborate_{int(time.time())}",
            description=task_description,
            complexity=0.7,  # Default complexity
            required_capabilities=agents if agents else ["development", "coordination"],
            time_critical=False,
            coordination_mode=CoordinationMode(mode) if mode != "adaptive_selection" else None
        )
        
        # Execute coordination
        result = await self.coordinator.coordinate_task(coordination_task, agents if agents else None)
        
        return {
            "success": True,
            "task": task_description,
            "agents": agents,
            "mode": result.get("coordination_mode", mode),
            "duration": result.get("duration", 0),
            "result": result.get("result", {})
        }
    
    async def handle_agent_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle agent list request"""
        category = params.get("category")
        available = params.get("available", True)
        active = params.get("active", False)
        
        agents = []
        
        if active:
            # List active agents
            active_agents = self.agent_manager.get_active_agents()
            for agent_id, config in active_agents.items():
                agents.append({
                    "id": agent_id,
                    "name": config.name,
                    "tier": config.tier.value,
                    "status": "active"
                })
        else:
            # List available agents
            registry = self.agent_manager.get_agent_registry()
            for agent_id, config in registry.items():
                # Filter by category if specified
                if category and config.capabilities:
                    if category not in config.capabilities.specialization_domains:
                        continue
                
                agents.append({
                    "id": agent_id,
                    "name": config.name,
                    "tier": config.tier.value,
                    "capabilities": config.capabilities.specialization_domains if config.capabilities else [],
                    "status": "available"
                })
        
        return {
            "success": True,
            "agents": agents,
            "total": len(agents),
            "filtered_by": category
        }
    
    async def handle_agent_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle agent info request"""
        agent_id = params.get("agent")
        show_capabilities = params.get("capabilities", False)
        show_status = params.get("status", False)
        
        if agent_id not in self.agent_manager.agent_registry:
            return {"error": f"Agent {agent_id} not found"}
        
        config = self.agent_manager.agent_registry[agent_id]
        
        info = {
            "id": agent_id,
            "name": config.name,
            "tier": config.tier.value,
            "model": config.model,
            "coordination_priority": config.coordination_priority
        }
        
        if show_capabilities and config.capabilities:
            info["capabilities"] = {
                "name": config.capabilities.name,
                "description": config.capabilities.description,
                "tools": config.capabilities.tools,
                "domains": config.capabilities.specialization_domains,
                "patterns": config.capabilities.coordination_patterns,
                "triggers": config.capabilities.activation_triggers
            }
        
        if show_status:
            is_active = agent_id in self.agent_manager.active_agents
            info["status"] = {
                "active": is_active,
                "last_used": "recently" if is_active else "not active"
            }
        
        return {
            "success": True,
            "agent": info
        }
    
    async def stop(self):
        """Stop the daemon bridge"""
        self.running = False
        
        # Clean up active swarms
        for swarm_id in list(self.active_swarms.keys()):
            await self.coordinator.swarm_manager.dissolve_swarm(swarm_id)
        
        self.logger.info("daemon_bridge_stopped")

# Entry point for standalone daemon bridge
async def main():
    bridge = DaemonBridge()
    
    try:
        await bridge.start()
    except KeyboardInterrupt:
        print("\nShutting down daemon bridge...")
        await bridge.stop()

if __name__ == "__main__":
    # Configure logging
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
    
    asyncio.run(main())