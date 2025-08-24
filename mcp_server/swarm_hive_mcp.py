#!/usr/bin/env python3
"""
MCP Server for AgentNativeFramework Swarm-Hive Integration
Provides swarm intelligence and hive mind capabilities to Claude Code
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.coordination.swarm_hive_coordinator import (
    SwarmHiveCoordinator, 
    CoordinationTask, 
    CoordinationMode
)
from core.agents.agent_manager import AgentManager

# MCP imports (these would be from the MCP SDK when available)
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource, 
        Tool, 
        TextContent, 
        ImageContent, 
        EmbeddedResource, 
        CallToolRequest, 
        CallToolResult,
        ListResourcesResult,
        ListToolsResult,
        ReadResourceResult,
    )
    MCP_AVAILABLE = True
except ImportError:
    # Fallback for systems without MCP
    MCP_AVAILABLE = False

class SwarmHiveMCPServer:
    """MCP Server providing swarm-hive capabilities to Claude Code"""
    
    def __init__(self):
        self.coordinator = None
        self.agent_manager = None
        self.server = None
        self.active_swarms = {}
        self.active_hive_sessions = {}
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize the swarm-hive coordinator"""
        try:
            self.coordinator = SwarmHiveCoordinator()
            self.agent_manager = AgentManager(swarm_hive_coordinator=self.coordinator)
            self.logger.info("Swarm-Hive MCP Server initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize coordinator: {e}")
            raise
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available MCP tools"""
        return [
            {
                "name": "swarm_create",
                "description": "Create a new agent swarm with specified topology and agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "swarm_id": {
                            "type": "string",
                            "description": "Unique identifier for the swarm"
                        },
                        "topology": {
                            "type": "string", 
                            "enum": ["hierarchical", "mesh", "collective", "adaptive"],
                            "description": "Swarm coordination topology"
                        },
                        "agents": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of agent IDs to include in swarm"
                        },
                        "task_description": {
                            "type": "string",
                            "description": "Optional description of the swarm's purpose"
                        }
                    },
                    "required": ["swarm_id", "agents"]
                }
            },
            {
                "name": "swarm_coordinate",
                "description": "Execute a task using swarm coordination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "swarm_id": {
                            "type": "string",
                            "description": "ID of the swarm to use"
                        },
                        "task": {
                            "type": "string",
                            "description": "Task for the swarm to coordinate on"
                        },
                        "complexity": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Task complexity (0-1)"
                        },
                        "time_critical": {
                            "type": "boolean",
                            "description": "Whether the task is time-critical"
                        }
                    },
                    "required": ["swarm_id", "task"]
                }
            },
            {
                "name": "hive_decide",
                "description": "Make a collective decision using hive intelligence",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Decision question to ask the hive"
                        },
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Available options for the decision"
                        },
                        "agents": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Agents to participate in decision"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["consensus", "weighted_voting", "quorum", "emergent"],
                            "description": "Decision-making method"
                        },
                        "timeout": {
                            "type": "number",
                            "description": "Decision timeout in seconds"
                        }
                    },
                    "required": ["question", "options", "agents"]
                }
            },
            {
                "name": "hive_remember",
                "description": "Store information in collective hive memory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Information to store"
                        },
                        "memory_type": {
                            "type": "string",
                            "enum": ["working", "episodic", "semantic", "collective"],
                            "description": "Type of memory to store"
                        },
                        "contributors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Agents contributing this information"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Confidence level (0-1)"
                        }
                    },
                    "required": ["content", "contributors"]
                }
            },
            {
                "name": "hive_recall",
                "description": "Retrieve information from collective memory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search memory"
                        },
                        "memory_type": {
                            "type": "string",
                            "enum": ["working", "episodic", "semantic", "collective"],
                            "description": "Type of memory to search"
                        },
                        "min_confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Minimum confidence threshold"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Maximum number of results"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "collaborate",
                "description": "Multi-agent collaboration using hybrid swarm-hive coordination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the collaboration task"
                        },
                        "agents": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Agents to collaborate"
                        },
                        "coordination_mode": {
                            "type": "string",
                            "enum": ["swarm_only", "hive_only", "swarm_hive_hybrid", "adaptive_selection"],
                            "description": "Coordination mode to use"
                        },
                        "complexity": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Task complexity (0-1)"
                        },
                        "time_critical": {
                            "type": "boolean",
                            "description": "Whether task is time-critical"
                        }
                    },
                    "required": ["task_description", "agents"]
                }
            },
            {
                "name": "get_swarm_status",
                "description": "Get status of active swarms and hive intelligence",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "swarm_id": {
                            "type": "string",
                            "description": "Specific swarm ID (optional)"
                        },
                        "detailed": {
                            "type": "boolean",
                            "description": "Return detailed status"
                        }
                    }
                }
            },
            {
                "name": "list_agents",
                "description": "List available agents for swarm coordination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter agents by category"
                        },
                        "capabilities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by required capabilities"
                        }
                    }
                }
            }
        ]
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool calls"""
        try:
            if name == "swarm_create":
                return await self._handle_swarm_create(arguments)
            elif name == "swarm_coordinate":
                return await self._handle_swarm_coordinate(arguments)
            elif name == "hive_decide":
                return await self._handle_hive_decide(arguments)
            elif name == "hive_remember":
                return await self._handle_hive_remember(arguments)
            elif name == "hive_recall":
                return await self._handle_hive_recall(arguments)
            elif name == "collaborate":
                return await self._handle_collaborate(arguments)
            elif name == "get_swarm_status":
                return await self._handle_get_swarm_status(arguments)
            elif name == "list_agents":
                return await self._handle_list_agents(arguments)
            else:
                return {"error": f"Unknown tool: {name}"}
                
        except Exception as e:
            self.logger.error(f"Tool call error ({name}): {e}")
            return {"error": f"Tool execution failed: {str(e)}"}
    
    async def _handle_swarm_create(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm creation"""
        from core.coordination.swarm_manager import SwarmTopology
        
        swarm_id = args["swarm_id"]
        topology_str = args.get("topology", "adaptive")
        agents = args["agents"]
        task_description = args.get("task_description", "")
        
        # Map topology string to enum
        topology_map = {
            "hierarchical": SwarmTopology.HIERARCHICAL,
            "mesh": SwarmTopology.MESH,
            "collective": SwarmTopology.COLLECTIVE,
            "adaptive": SwarmTopology.ADAPTIVE
        }
        
        topology = topology_map.get(topology_str, SwarmTopology.ADAPTIVE)
        
        # Create swarm
        swarm = await self.coordinator.swarm_manager.create_swarm(
            swarm_id,
            topology,
            agents,
            {"description": task_description, "created_via": "claude_code"}
        )
        
        self.active_swarms[swarm_id] = swarm
        
        return {
            "success": True,
            "swarm_id": swarm_id,
            "topology": topology_str,
            "agents": len(agents),
            "message": f"Swarm '{swarm_id}' created with {len(agents)} agents using {topology_str} topology"
        }
    
    async def _handle_swarm_coordinate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm task coordination"""
        swarm_id = args["swarm_id"]
        task_description = args["task"]
        complexity = args.get("complexity", 0.7)
        time_critical = args.get("time_critical", False)
        
        if swarm_id not in self.active_swarms:
            return {"error": f"Swarm '{swarm_id}' not found. Create it first."}
        
        # Execute coordination
        task = {
            "type": "claude_code_task",
            "description": task_description,
            "complexity": complexity,
            "time_critical": time_critical
        }
        
        result = await self.coordinator.swarm_manager.coordinate_swarm_task(swarm_id, task)
        
        return {
            "success": True,
            "swarm_id": swarm_id,
            "task": task_description,
            "coordination_result": result,
            "message": f"Swarm coordination completed for: {task_description}"
        }
    
    async def _handle_hive_decide(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hive collective decision"""
        question = args["question"]
        options = args["options"]
        agents = args["agents"]
        method = args.get("method", "consensus")
        timeout = args.get("timeout", 300)
        
        # Initialize hive nodes for agents
        for agent_id in agents:
            if agent_id in self.agent_manager.agent_registry:
                agent_config = self.agent_manager.agent_registry[agent_id]
                capabilities = agent_config.capabilities.specialization_domains if agent_config.capabilities else []
                await self.coordinator.hive_intelligence.initialize_hive_node(agent_id, capabilities)
        
        # Create decision options
        decision_options = []
        for i, option in enumerate(options):
            decision_options.append({
                "id": f"option_{i}",
                "description": option,
                "required_expertise": [i % 3]
            })
        
        # Map method string to enum
        from core.coordination.hive_intelligence import HiveDecisionMethod
        method_map = {
            "consensus": HiveDecisionMethod.CONSENSUS,
            "weighted_voting": HiveDecisionMethod.WEIGHTED_VOTING,
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
        
        return {
            "success": True,
            "decision_id": decision_id,
            "question": question,
            "options": options,
            "method": method,
            "agents": agents,
            "message": f"Hive decision initiated: {question}"
        }
    
    async def _handle_hive_remember(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle storing information in collective memory"""
        content = args["content"]
        memory_type = args.get("memory_type", "semantic")
        contributors = args["contributors"]
        confidence = args.get("confidence", 0.8)
        
        # Map memory type string to enum
        from core.coordination.hive_intelligence import HiveMemoryType
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
            "content": content[:100] + "..." if len(content) > 100 else content,
            "memory_type": memory_type,
            "contributors": contributors,
            "message": f"Information stored in {memory_type} memory"
        }
    
    async def _handle_hive_recall(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle recalling information from collective memory"""
        query = args["query"]
        memory_type = args.get("memory_type")
        min_confidence = args.get("min_confidence", 0.5)
        limit = args.get("limit", 10)
        
        # Map memory type if specified
        mem_type = None
        if memory_type:
            from core.coordination.hive_intelligence import HiveMemoryType
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
        for memory in memories[:limit]:
            results.append({
                "fragment_id": memory.fragment_id,
                "content": str(memory.content),
                "confidence": memory.confidence_score,
                "type": memory.memory_type.value,
                "contributors": list(memory.contributors),
                "access_count": memory.access_count
            })
        
        return {
            "success": True,
            "query": query,
            "memories_found": len(results),
            "results": results,
            "message": f"Found {len(results)} relevant memories for: {query}"
        }
    
    async def _handle_collaborate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle multi-agent collaboration"""
        task_description = args["task_description"]
        agents = args["agents"]
        coordination_mode = args.get("coordination_mode", "adaptive_selection")
        complexity = args.get("complexity", 0.7)
        time_critical = args.get("time_critical", False)
        
        # Create coordination task
        coordination_task = CoordinationTask(
            task_id=f"claude_code_collab_{int(asyncio.get_event_loop().time())}",
            description=task_description,
            complexity=complexity,
            required_capabilities=agents,
            time_critical=time_critical,
            coordination_mode=CoordinationMode(coordination_mode) if coordination_mode != "adaptive_selection" else None
        )
        
        # Execute coordination
        result = await self.coordinator.coordinate_task(coordination_task, agents)
        
        return {
            "success": True,
            "task": task_description,
            "agents": agents,
            "mode_used": result.get("coordination_mode", coordination_mode),
            "duration": result.get("duration", 0),
            "efficiency": result.get("result", {}).get("efficiency_score", 0),
            "result": result.get("result", {}),
            "message": f"Collaboration completed: {task_description}"
        }
    
    async def _handle_get_swarm_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting swarm status"""
        swarm_id = args.get("swarm_id")
        detailed = args.get("detailed", False)
        
        if swarm_id:
            # Get specific swarm status
            if swarm_id in self.active_swarms:
                status = self.coordinator.swarm_manager.get_swarm_status(swarm_id)
                return {
                    "success": True,
                    "swarm_id": swarm_id,
                    "status": status
                }
            else:
                return {"error": f"Swarm '{swarm_id}' not found"}
        else:
            # Get all swarms status
            all_status = self.coordinator.get_coordination_status()
            hive_status = self.coordinator.hive_intelligence.get_hive_status()
            
            return {
                "success": True,
                "coordination_status": all_status,
                "hive_status": hive_status,
                "active_swarms": list(self.active_swarms.keys()),
                "message": "System status retrieved"
            }
    
    async def _handle_list_agents(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle listing available agents"""
        category = args.get("category")
        capabilities = args.get("capabilities", [])
        
        # Get agents from registry
        registry = self.agent_manager.get_agent_registry()
        agents = []
        
        for agent_id, config in registry.items():
            # Filter by category if specified
            if category and config.tier.value != category:
                continue
            
            # Filter by capabilities if specified
            if capabilities and config.capabilities:
                agent_caps = set(config.capabilities.specialization_domains)
                required_caps = set(capabilities)
                if not agent_caps.intersection(required_caps):
                    continue
            
            agents.append({
                "id": agent_id,
                "name": config.name,
                "tier": config.tier.value,
                "capabilities": config.capabilities.specialization_domains if config.capabilities else [],
                "priority": config.coordination_priority
            })
        
        return {
            "success": True,
            "agents": agents,
            "total": len(agents),
            "filtered_by_category": category,
            "filtered_by_capabilities": capabilities
        }

# MCP Server setup (if MCP is available)
if MCP_AVAILABLE:
    async def run_mcp_server():
        """Run the MCP server"""
        swarm_hive_server = SwarmHiveMCPServer()
        await swarm_hive_server.initialize()
        
        server = Server("swarm-hive-mcp")
        
        @server.list_tools()
        async def list_tools() -> List[Tool]:
            tools = swarm_hive_server.get_tools()
            return [Tool(**tool) for tool in tools]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            result = await swarm_hive_server.handle_tool_call(name, arguments)
            
            if result.get("error"):
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {result['error']}")]
                )
            else:
                return CallToolResult(
                    content=[TextContent(
                        type="text", 
                        text=json.dumps(result, indent=2)
                    )]
                )
        
        # Run server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="swarm-hive-mcp",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities={}
                    ),
                )
            )

# Fallback standalone server (if MCP is not available)
async def run_standalone_server():
    """Run as standalone server for testing"""
    swarm_hive_server = SwarmHiveMCPServer()
    await swarm_hive_server.initialize()
    
    print("🧠🐛 Swarm-Hive Server Started")
    print("Available tools:")
    for tool in swarm_hive_server.get_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\nServer ready for Claude Code integration...")
    
    # Keep server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    if MCP_AVAILABLE:
        asyncio.run(run_mcp_server())
    else:
        print("MCP not available, running in standalone mode...")
        asyncio.run(run_standalone_server())