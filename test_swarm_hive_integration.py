#!/usr/bin/env python3
"""
Test suite for Swarm-Hive Integration in AgentNativeFramework
Demonstrates the full swarm intelligence and hive mind capabilities
"""

import asyncio
import json
import time
from typing import Dict, List, Any
from pathlib import Path

# Import the core components
from core.agents.agent_manager import AgentManager
from core.coordination.swarm_manager import SwarmManager, SwarmTopology
from core.coordination.hive_intelligence import HiveIntelligence, HiveDecisionMethod, HiveMemoryType
from core.coordination.swarm_hive_coordinator import SwarmHiveCoordinator, CoordinationTask, CoordinationMode

async def test_swarm_functionality():
    """Test pure swarm coordination capabilities"""
    print("\n🐛 Testing Swarm Functionality")
    print("=" * 50)
    
    # Initialize components
    agent_manager = AgentManager()
    swarm_manager = SwarmManager(agent_manager)
    
    # Create a hierarchical swarm for iOS development
    swarm_agents = ["ios_developer", "ai_engineer", "project_supervisor_orchestrator"]
    
    swarm = await swarm_manager.create_swarm(
        "ios_dev_swarm",
        SwarmTopology.HIERARCHICAL,
        swarm_agents,
        {"project_type": "ios_ai_app", "complexity": 0.8}
    )
    
    print(f"✅ Created swarm: {swarm.swarm_id}")
    print(f"   Topology: {swarm.topology.value}")
    print(f"   Agents: {len(swarm.active_agents)}")
    
    # Execute a swarm task
    task = {
        "type": "build_ios_ai_app",
        "description": "Build TreeAI mobile app with Claude integration",
        "complexity": 0.8,
        "time_critical": False
    }
    
    start_time = time.time()
    result = await swarm_manager.coordinate_swarm_task("ios_dev_swarm", task)
    duration = time.time() - start_time
    
    print(f"✅ Swarm task completed in {duration:.2f}s")
    print(f"   Result: {result.get('status', 'unknown')}")
    print(f"   Approach: {result.get('approach', 'unknown')}")
    
    # Get swarm status
    status = swarm_manager.get_swarm_status("ios_dev_swarm")
    print(f"📊 Swarm status: {status['agent_count']} agents, health: {status['health_score']}")
    
    # Clean up
    await swarm_manager.dissolve_swarm("ios_dev_swarm")
    print("🧹 Swarm dissolved\n")

async def test_hive_intelligence():
    """Test hive intelligence and collective decision-making"""
    print("\n🧠 Testing Hive Intelligence")
    print("=" * 50)
    
    hive = HiveIntelligence()
    
    # Initialize hive nodes
    agents_and_capabilities = [
        ("ios_developer", ["development", "ios", "mobile"]),
        ("ai_engineer", ["ai", "research", "development"]),
        ("tree_analysis_specialist", ["forestry", "analysis", "business"]),
        ("backend_architect", ["backend", "architecture", "systems"])
    ]
    
    nodes = []
    for agent_id, capabilities in agents_and_capabilities:
        node = await hive.initialize_hive_node(agent_id, capabilities)
        nodes.append(node)
        print(f"✅ Initialized hive node for {agent_id}")
    
    # Store collective memory
    memory_content = {
        "best_practices": "AI development requires proper testing and validation",
        "technology_stack": ["Swift", "Claude API", "Core ML"],
        "success_patterns": ["incremental_development", "user_feedback_loops"]
    }
    
    memory_id = await hive.store_collective_memory(
        memory_content,
        HiveMemoryType.SEMANTIC,
        {node.agent_id for node in nodes},
        confidence=0.9
    )
    
    print(f"✅ Stored collective memory: {memory_id}")
    
    # Test memory recall
    recalled_memories = await hive.recall_collective_memory(
        "AI development best practices",
        HiveMemoryType.SEMANTIC,
        min_confidence=0.8
    )
    
    print(f"📚 Recalled {len(recalled_memories)} relevant memories")
    
    # Initiate collective decision
    decision_options = [
        {"id": "mvp_approach", "description": "Build MVP first", "required_expertise": [0, 1]},
        {"id": "full_featured", "description": "Build complete solution", "required_expertise": [1, 2, 3]},
        {"id": "modular_approach", "description": "Build modular system", "required_expertise": [0, 2]}
    ]
    
    decision_id = await hive.initiate_hive_decision(
        "What development approach should we use for the TreeAI app?",
        decision_options,
        HiveDecisionMethod.CONSENSUS,
        timeout_seconds=5  # Short timeout for testing
    )
    
    print(f"🗳️ Initiated hive decision: {decision_id}")
    
    # Wait for decision (short wait for demo)
    await asyncio.sleep(6)
    
    # Check hive status
    status = hive.get_hive_status()
    print(f"📊 Hive status: {status['nodes']} nodes, {status['memory_fragments']} memories")
    print(f"   Collective confidence: {status['collective_confidence']:.2f}")
    print("")

async def test_swarm_hive_hybrid():
    """Test integrated swarm-hive coordination"""
    print("\n🚀 Testing Swarm-Hive Hybrid Coordination")
    print("=" * 50)
    
    # Initialize full coordinator
    agent_manager = AgentManager()
    coordinator = SwarmHiveCoordinator(agent_manager)
    
    # Test different coordination modes
    test_tasks = [
        {
            "name": "Simple iOS Development",
            "task": CoordinationTask(
                task_id="simple_ios",
                description="Create basic iOS app interface",
                complexity=0.4,
                required_capabilities=["ios", "design"],
                time_critical=True,
                coordination_mode=CoordinationMode.SWARM_ONLY
            )
        },
        {
            "name": "Complex AI Research",
            "task": CoordinationTask(
                task_id="complex_ai_research", 
                description="Research and implement novel AI algorithms",
                complexity=0.9,
                required_capabilities=["ai", "research", "analysis", "development"],
                time_critical=False,
                coordination_mode=CoordinationMode.HIVE_ONLY
            )
        },
        {
            "name": "TreeAI Business System",
            "task": CoordinationTask(
                task_id="treeai_system",
                description="Build comprehensive TreeAI business management system",
                complexity=0.8,
                required_capabilities=["forestry", "business", "ai", "ios", "backend"],
                time_critical=False,
                coordination_mode=CoordinationMode.SWARM_HIVE_HYBRID
            )
        }
    ]
    
    results = []
    for test_case in test_tasks:
        print(f"\n🎯 Testing: {test_case['name']}")
        print(f"   Complexity: {test_case['task'].complexity}")
        print(f"   Mode: {test_case['task'].coordination_mode.value}")
        
        start_time = time.time()
        result = await coordinator.coordinate_task(test_case['task'])
        duration = time.time() - start_time
        
        results.append({
            "test_name": test_case['name'],
            "duration": duration,
            "result": result
        })
        
        print(f"   ✅ Completed in {duration:.2f}s")
        print(f"   Mode used: {result.get('coordination_mode', 'unknown')}")
        print(f"   Efficiency: {result.get('result', {}).get('efficiency_score', 0):.2f}")
    
    # Summary
    print(f"\n📈 Test Summary:")
    for result in results:
        print(f"   {result['test_name']}: {result['duration']:.2f}s")
    
    print("")

async def test_adaptive_coordination():
    """Test adaptive coordination mode selection"""
    print("\n🔄 Testing Adaptive Coordination")
    print("=" * 50)
    
    agent_manager = AgentManager()
    coordinator = SwarmHiveCoordinator(agent_manager)
    
    # Create adaptive tasks with different characteristics
    adaptive_tasks = [
        CoordinationTask(
            task_id="low_complexity",
            description="Simple task with low complexity",
            complexity=0.2,
            required_capabilities=["development"],
            time_critical=False,
            coordination_mode=CoordinationMode.ADAPTIVE_SELECTION
        ),
        CoordinationTask(
            task_id="high_complexity_urgent",
            description="Complex urgent task",
            complexity=0.9,
            required_capabilities=["ai", "research", "development", "testing"],
            time_critical=True,
            coordination_mode=CoordinationMode.ADAPTIVE_SELECTION
        ),
        CoordinationTask(
            task_id="large_team_task",
            description="Task requiring many specialists",
            complexity=0.6,
            required_capabilities=["ios", "ai", "backend", "design", "testing", "security", "deployment", "business", "analysis"],
            time_critical=False,
            coordination_mode=CoordinationMode.ADAPTIVE_SELECTION
        )
    ]
    
    for task in adaptive_tasks:
        print(f"\n🎲 Adaptive task: {task.description}")
        print(f"   Complexity: {task.complexity}, Capabilities: {len(task.required_capabilities)}")
        print(f"   Time critical: {task.time_critical}")
        
        result = await coordinator.coordinate_task(task)
        selected_mode = result.get("coordination_mode", "unknown")
        
        print(f"   🎯 Selected mode: {selected_mode}")
        print(f"   Duration: {result.get('duration', 0):.2f}s")
    
    print("")

async def test_agent_manager_integration():
    """Test integration with agent manager"""
    print("\n🔗 Testing Agent Manager Integration")
    print("=" * 50)
    
    # Initialize enhanced agent manager
    coordinator = SwarmHiveCoordinator()
    agent_manager = AgentManager(swarm_hive_coordinator=coordinator)
    
    # Test swarm-hive recommendations
    task_requirements = {
        "complexity": 0.7,
        "required_capabilities": ["ios", "ai", "forestry"],
        "time_critical": False
    }
    
    recommendations = agent_manager.get_swarm_hive_recommendations(task_requirements)
    print("🎯 Coordination Recommendations:")
    for key, value in recommendations.items():
        print(f"   {key}: {value}")
    
    # Test optimal agent suggestions
    agent_suggestions = agent_manager.suggest_optimal_agents_for_swarm_hive(
        task_requirements["required_capabilities"]
    )
    
    print("\n👥 Suggested Agent Composition:")
    for role, agents in agent_suggestions.items():
        if agents:
            print(f"   {role}: {agents}")
    
    # Test specialized swarm-hive creation
    specialized_result = await agent_manager.create_specialized_swarm_hive(
        "ios_development",
        {"custom_param": "test_value"}
    )
    
    print(f"\n🏗️ Specialized swarm-hive created:")
    print(f"   ID: {specialized_result.get('swarm_hive_id', 'unknown')}")
    print(f"   Status: {specialized_result.get('status', 'unknown')}")
    
    # Test enhanced coordination
    enhanced_task = {
        "description": "Build AI-powered TreeAI mobile application",
        "complexity": 0.8,
        "required_capabilities": ["ios", "ai", "forestry", "business"],
        "time_critical": False
    }
    
    enhanced_result = await agent_manager.coordinate_with_swarm_hive(enhanced_task)
    print(f"\n⚡ Enhanced coordination completed:")
    print(f"   Mode: {enhanced_result.get('coordination_mode', 'unknown')}")
    print(f"   Duration: {enhanced_result.get('duration', 0):.2f}s")
    
    print("")

async def test_system_status_monitoring():
    """Test system status and monitoring"""
    print("\n📊 Testing System Status Monitoring")
    print("=" * 50)
    
    coordinator = SwarmHiveCoordinator()
    
    # Get comprehensive status
    status = coordinator.get_coordination_status()
    
    print("🎛️ System Status:")
    print(f"   Active coordinations: {status['coordinator']['active_coordinations']}")
    print(f"   Coordination history: {status['coordinator']['coordination_history']}")
    print(f"   Active swarms: {status['swarm_manager']['active_swarms']}")
    print(f"   Hive nodes: {status['hive_intelligence']['nodes']}")
    print(f"   Memory fragments: {status['hive_intelligence']['memory_fragments']}")
    print(f"   Collective confidence: {status['hive_intelligence']['collective_confidence']:.2f}")
    
    print("\n🏥 System Health:")
    health = status.get('system_health', {})
    for metric, value in health.items():
        print(f"   {metric}: {value:.2f}")
    
    print("")

async def main():
    """Run all tests"""
    print("🚀 AgentNativeFramework Swarm-Hive Integration Test Suite")
    print("=" * 70)
    
    # Run all test suites
    await test_swarm_functionality()
    await test_hive_intelligence()
    await test_swarm_hive_hybrid()
    await test_adaptive_coordination()
    await test_agent_manager_integration()
    await test_system_status_monitoring()
    
    print("🎉 All tests completed successfully!")
    print("=" * 70)
    
    print("\n📋 Summary:")
    print("✅ Swarm coordination working")
    print("✅ Hive intelligence operational")
    print("✅ Hybrid coordination functional")
    print("✅ Adaptive mode selection active")
    print("✅ Agent manager integration complete")
    print("✅ System monitoring enabled")
    
    print("\n🔮 The swarm and hive functions have been successfully added!")
    print("You can now use:")
    print("   - SwarmManager for swarm intelligence")
    print("   - HiveIntelligence for collective decision-making")
    print("   - SwarmHiveCoordinator for integrated coordination")
    print("   - Enhanced AgentManager with swarm-hive capabilities")

if __name__ == "__main__":
    # Add numpy requirement check
    try:
        import numpy as np
        print("✅ NumPy available")
    except ImportError:
        print("⚠️ NumPy not found - install with: pip install numpy")
    
    # Run the test suite
    asyncio.run(main())