"""
Hive Intelligence System for AgentNativeFramework
Implements collective decision-making, distributed memory, and emergent behavior patterns
"""

import asyncio
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import structlog
from prometheus_client import Counter, Histogram, Gauge
import numpy as np

class HiveDecisionMethod(Enum):
    CONSENSUS = "consensus"           # Require majority agreement
    WEIGHTED_VOTING = "weighted"     # Weight votes by agent expertise  
    QUORUM = "quorum"               # Minimum participation threshold
    EMERGENT = "emergent"           # Let patterns emerge naturally

class HiveMemoryType(Enum):
    WORKING = "working"             # Short-term task memory
    EPISODIC = "episodic"          # Experience-based memory
    SEMANTIC = "semantic"          # Knowledge and facts
    COLLECTIVE = "collective"      # Shared hive memory

@dataclass
class HiveNode:
    node_id: str
    agent_id: str
    expertise_vector: List[float]
    influence_score: float = 1.0
    participation_history: List[Dict] = field(default_factory=list)
    connections: Set[str] = field(default_factory=set)
    memory_contribution: Dict[str, Any] = field(default_factory=dict)

@dataclass
class HiveMemoryFragment:
    fragment_id: str
    memory_type: HiveMemoryType
    content: Any
    contributors: Set[str]
    confidence_score: float
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    relevance_decay: float = 1.0

@dataclass
class HiveDecision:
    decision_id: str
    question: str
    options: List[Dict[str, Any]]
    method: HiveDecisionMethod
    participants: Set[str]
    votes: Dict[str, Any] = field(default_factory=dict)
    consensus_reached: bool = False
    confidence: float = 0.0
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None

class HiveIntelligence:
    """
    Manages collective intelligence and emergent behavior in agent swarms
    """
    
    # Metrics for hive operations
    hive_decisions = Counter('hive_decisions_total', 'Total hive decisions', ['method', 'outcome'])
    memory_operations = Counter('hive_memory_operations_total', 'Memory operations', ['operation'])
    emergence_events = Counter('emergence_events_total', 'Emergent behavior events', ['type'])
    collective_confidence = Gauge('hive_collective_confidence', 'Overall hive confidence')
    memory_fragments_gauge = Gauge('hive_memory_fragments', 'Number of memory fragments')
    
    def __init__(self, swarm_manager=None):
        """Initialize hive intelligence system"""
        self.logger = structlog.get_logger(__name__)
        self.swarm_manager = swarm_manager
        
        # Hive state
        self.nodes: Dict[str, HiveNode] = {}
        self.memory_store: Dict[str, HiveMemoryFragment] = {}
        self.active_decisions: Dict[str, HiveDecision] = {}
        self.decision_history: List[HiveDecision] = []
        
        # Collective intelligence parameters
        self.collective_threshold = 0.75  # Threshold for collective decisions
        self.memory_decay_rate = 0.95     # Rate of memory relevance decay
        self.emergence_sensitivity = 0.8  # Sensitivity to emergent patterns
        
        # Learning and adaptation
        self.pattern_cache: Dict[str, Any] = {}
        self.behavioral_patterns: Dict[str, List[Dict]] = {}
        
        self.logger.info("hive_intelligence_initialized")
    
    async def initialize_hive_node(
        self, 
        agent_id: str, 
        capabilities: List[str],
        initial_expertise: Optional[List[float]] = None
    ) -> HiveNode:
        """Initialize a new hive node for an agent"""
        
        node_id = f"hive_node_{agent_id}_{int(time.time())}"
        
        # Create expertise vector from capabilities
        if initial_expertise:
            expertise_vector = initial_expertise
        else:
            expertise_vector = self._create_expertise_vector(capabilities)
        
        node = HiveNode(
            node_id=node_id,
            agent_id=agent_id,
            expertise_vector=expertise_vector
        )
        
        self.nodes[node_id] = node
        
        # Connect to similar nodes
        await self._establish_node_connections(node)
        
        self.logger.info(
            "hive_node_created",
            node_id=node_id,
            agent_id=agent_id,
            connections=len(node.connections)
        )
        
        return node
    
    def _create_expertise_vector(self, capabilities: List[str]) -> List[float]:
        """Create numerical expertise vector from capability strings"""
        # Predefined capability domains for vectorization
        domains = [
            "development", "ai_ml", "research", "design", "testing", 
            "security", "deployment", "coordination", "analysis", "business"
        ]
        
        vector = [0.0] * len(domains)
        
        for capability in capabilities:
            for i, domain in enumerate(domains):
                if domain in capability.lower():
                    vector[i] = 1.0
        
        # Add some randomness for unique perspectives
        noise = np.random.normal(0, 0.1, len(vector))
        vector = [max(0, min(1, v + n)) for v, n in zip(vector, noise)]
        
        return vector
    
    async def _establish_node_connections(self, new_node: HiveNode):
        """Establish connections between similar nodes"""
        
        for existing_node in self.nodes.values():
            if existing_node.node_id == new_node.node_id:
                continue
            
            # Calculate similarity between expertise vectors
            similarity = self._calculate_expertise_similarity(
                new_node.expertise_vector,
                existing_node.expertise_vector
            )
            
            # Connect nodes above similarity threshold
            if similarity > 0.6:
                new_node.connections.add(existing_node.node_id)
                existing_node.connections.add(new_node.node_id)
    
    def _calculate_expertise_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between expertise vectors"""
        if len(vector1) != len(vector2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        magnitude1 = sum(a * a for a in vector1) ** 0.5
        magnitude2 = sum(b * b for b in vector2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def store_collective_memory(
        self,
        content: Any,
        memory_type: HiveMemoryType,
        contributors: Set[str],
        confidence: float = 0.8
    ) -> str:
        """Store information in collective hive memory"""
        
        # Generate unique fragment ID
        content_hash = hashlib.sha256(str(content).encode()).hexdigest()[:12]
        fragment_id = f"hive_memory_{memory_type.value}_{content_hash}"
        
        fragment = HiveMemoryFragment(
            fragment_id=fragment_id,
            memory_type=memory_type,
            content=content,
            contributors=contributors,
            confidence_score=confidence
        )
        
        self.memory_store[fragment_id] = fragment
        self.memory_operations.labels(operation="store").inc()
        self.memory_fragments_gauge.set(len(self.memory_store))
        
        # Update node contributions
        for contributor_id in contributors:
            node = self._find_node_by_agent_id(contributor_id)
            if node:
                node.memory_contribution[fragment_id] = {
                    "type": memory_type.value,
                    "timestamp": time.time()
                }
        
        self.logger.info(
            "memory_stored",
            fragment_id=fragment_id,
            type=memory_type.value,
            contributors=len(contributors)
        )
        
        return fragment_id
    
    async def recall_collective_memory(
        self,
        query: str,
        memory_type: Optional[HiveMemoryType] = None,
        min_confidence: float = 0.5
    ) -> List[HiveMemoryFragment]:
        """Recall relevant memory fragments from collective memory"""
        
        relevant_fragments = []
        
        for fragment in self.memory_store.values():
            # Filter by type if specified
            if memory_type and fragment.memory_type != memory_type:
                continue
            
            # Filter by confidence threshold
            if fragment.confidence_score < min_confidence:
                continue
            
            # Calculate relevance (simple string matching for now)
            relevance = self._calculate_memory_relevance(query, fragment)
            
            if relevance > 0.3:  # Relevance threshold
                fragment.access_count += 1
                fragment.last_accessed = time.time()
                relevant_fragments.append(fragment)
        
        # Sort by relevance and confidence
        relevant_fragments.sort(
            key=lambda f: f.confidence_score * f.relevance_decay,
            reverse=True
        )
        
        self.memory_operations.labels(operation="recall").inc()
        
        return relevant_fragments[:10]  # Return top 10 most relevant
    
    def _calculate_memory_relevance(self, query: str, fragment: HiveMemoryFragment) -> float:
        """Calculate relevance of memory fragment to query"""
        query_words = set(query.lower().split())
        content_words = set(str(fragment.content).lower().split())
        
        if not query_words or not content_words:
            return 0.0
        
        intersection = query_words.intersection(content_words)
        return len(intersection) / len(query_words.union(content_words))
    
    async def initiate_hive_decision(
        self,
        question: str,
        options: List[Dict[str, Any]], 
        method: HiveDecisionMethod = HiveDecisionMethod.CONSENSUS,
        timeout_seconds: int = 300
    ) -> str:
        """Initiate a collective decision-making process"""
        
        decision_id = f"hive_decision_{int(time.time())}"
        
        decision = HiveDecision(
            decision_id=decision_id,
            question=question,
            options=options,
            method=method,
            participants=set(node.agent_id for node in self.nodes.values())
        )
        
        self.active_decisions[decision_id] = decision
        
        self.logger.info(
            "hive_decision_initiated",
            decision_id=decision_id,
            method=method.value,
            options=len(options),
            participants=len(decision.participants)
        )
        
        # Start decision process with timeout
        asyncio.create_task(self._process_hive_decision(decision_id, timeout_seconds))
        
        return decision_id
    
    async def _process_hive_decision(self, decision_id: str, timeout_seconds: int):
        """Process hive decision with timeout"""
        
        start_time = time.time()
        decision = self.active_decisions[decision_id]
        
        # Collect votes from all nodes
        voting_tasks = []
        for node in self.nodes.values():
            if node.agent_id in decision.participants:
                task = self._collect_node_vote(node, decision)
                voting_tasks.append(task)
        
        # Wait for votes or timeout
        try:
            await asyncio.wait_for(
                asyncio.gather(*voting_tasks, return_exceptions=True),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            self.logger.warning("hive_decision_timeout", decision_id=decision_id)
        
        # Resolve decision
        await self._resolve_hive_decision(decision_id)
    
    async def _collect_node_vote(self, node: HiveNode, decision: HiveDecision):
        """Collect vote from individual node"""
        
        # Simulate node deliberation time
        deliberation_time = np.random.uniform(0.1, 2.0)
        await asyncio.sleep(deliberation_time)
        
        # Generate vote based on node expertise
        vote = await self._generate_node_vote(node, decision)
        
        decision.votes[node.node_id] = vote
        
        # Update participation history
        node.participation_history.append({
            "decision_id": decision.decision_id,
            "timestamp": time.time(),
            "vote": vote
        })
    
    async def _generate_node_vote(self, node: HiveNode, decision: HiveDecision) -> Dict[str, Any]:
        """Generate vote from node based on expertise and connections"""
        
        # Consider node's expertise for each option
        option_scores = []
        
        for option in decision.options:
            # Base score from expertise alignment
            expertise_score = self._calculate_option_expertise_alignment(node, option)
            
            # Influence from connected nodes (if they've already voted)
            influence_score = self._calculate_connection_influence(node, decision, option)
            
            # Combined score with confidence
            total_score = (expertise_score * 0.7 + influence_score * 0.3) * node.influence_score
            
            option_scores.append({
                "option_id": option.get("id", "unknown"),
                "score": total_score,
                "confidence": min(1.0, expertise_score + 0.2)
            })
        
        # Select highest scoring option
        best_option = max(option_scores, key=lambda x: x["score"])
        
        return {
            "chosen_option": best_option["option_id"],
            "confidence": best_option["confidence"],
            "scores": option_scores,
            "vote_timestamp": time.time()
        }
    
    def _calculate_option_expertise_alignment(self, node: HiveNode, option: Dict[str, Any]) -> float:
        """Calculate how well option aligns with node expertise"""
        
        option_requirements = option.get("required_expertise", [])
        if not option_requirements:
            return 0.5  # Neutral if no requirements specified
        
        # Simple matching for now - could be more sophisticated
        alignment_score = 0.0
        for req in option_requirements:
            req_index = req % len(node.expertise_vector)  # Map requirement to expertise dimension
            alignment_score += node.expertise_vector[req_index]
        
        return min(1.0, alignment_score / len(option_requirements))
    
    def _calculate_connection_influence(self, node: HiveNode, decision: HiveDecision, option: Dict[str, Any]) -> float:
        """Calculate influence from connected nodes that have already voted"""
        
        if not node.connections:
            return 0.5  # Neutral if no connections
        
        influence_sum = 0.0
        influence_count = 0
        
        for connected_node_id in node.connections:
            if connected_node_id in decision.votes:
                connected_vote = decision.votes[connected_node_id]
                if connected_vote["chosen_option"] == option.get("id"):
                    influence_sum += connected_vote["confidence"]
                    influence_count += 1
        
        return influence_sum / influence_count if influence_count > 0 else 0.5
    
    async def _resolve_hive_decision(self, decision_id: str):
        """Resolve hive decision based on collected votes"""
        
        decision = self.active_decisions[decision_id]
        
        if decision.method == HiveDecisionMethod.CONSENSUS:
            result = self._resolve_consensus(decision)
        elif decision.method == HiveDecisionMethod.WEIGHTED_VOTING:
            result = self._resolve_weighted_voting(decision)
        elif decision.method == HiveDecisionMethod.QUORUM:
            result = self._resolve_quorum(decision)
        elif decision.method == HiveDecisionMethod.EMERGENT:
            result = self._resolve_emergent(decision)
        else:
            result = {"error": "Unknown decision method"}
        
        # Update decision state
        decision.consensus_reached = result.get("consensus_reached", False)
        decision.confidence = result.get("confidence", 0.0)
        decision.resolved_at = time.time()
        
        # Move to history
        self.decision_history.append(decision)
        del self.active_decisions[decision_id]
        
        # Update metrics
        outcome = "consensus" if decision.consensus_reached else "no_consensus"
        self.hive_decisions.labels(method=decision.method.value, outcome=outcome).inc()
        self.collective_confidence.set(self._calculate_collective_confidence())
        
        self.logger.info(
            "hive_decision_resolved",
            decision_id=decision_id,
            consensus_reached=decision.consensus_reached,
            confidence=decision.confidence
        )
        
        # Check for emergent patterns
        await self._detect_emergence_patterns(decision)
    
    def _resolve_consensus(self, decision: HiveDecision) -> Dict[str, Any]:
        """Resolve decision using consensus method"""
        
        if not decision.votes:
            return {"consensus_reached": False, "confidence": 0.0}
        
        # Count votes for each option
        option_votes = {}
        total_confidence = 0.0
        
        for vote in decision.votes.values():
            option_id = vote["chosen_option"]
            confidence = vote["confidence"]
            
            if option_id not in option_votes:
                option_votes[option_id] = {"count": 0, "total_confidence": 0.0}
            
            option_votes[option_id]["count"] += 1
            option_votes[option_id]["total_confidence"] += confidence
            total_confidence += confidence
        
        # Check if any option has majority
        total_votes = len(decision.votes)
        majority_threshold = total_votes * self.collective_threshold
        
        for option_id, votes in option_votes.items():
            if votes["count"] >= majority_threshold:
                avg_confidence = votes["total_confidence"] / votes["count"]
                return {
                    "consensus_reached": True,
                    "chosen_option": option_id,
                    "confidence": avg_confidence,
                    "vote_distribution": option_votes
                }
        
        # No consensus reached
        return {
            "consensus_reached": False,
            "confidence": total_confidence / total_votes if total_votes > 0 else 0.0,
            "vote_distribution": option_votes
        }
    
    def _resolve_weighted_voting(self, decision: HiveDecision) -> Dict[str, Any]:
        """Resolve decision using weighted voting based on expertise"""
        
        option_scores = {}
        total_weight = 0.0
        
        for node_id, vote in decision.votes.items():
            node = self._find_node_by_id(node_id)
            if not node:
                continue
            
            weight = node.influence_score * vote["confidence"]
            option_id = vote["chosen_option"]
            
            if option_id not in option_scores:
                option_scores[option_id] = 0.0
            
            option_scores[option_id] += weight
            total_weight += weight
        
        # Find winning option
        if option_scores:
            winning_option = max(option_scores, key=option_scores.get)
            confidence = option_scores[winning_option] / total_weight if total_weight > 0 else 0.0
            
            return {
                "consensus_reached": True,
                "chosen_option": winning_option,
                "confidence": confidence,
                "weighted_scores": option_scores
            }
        
        return {"consensus_reached": False, "confidence": 0.0}
    
    def _resolve_quorum(self, decision: HiveDecision) -> Dict[str, Any]:
        """Resolve decision using quorum method"""
        
        participation_rate = len(decision.votes) / len(decision.participants)
        quorum_threshold = 0.6  # 60% participation required
        
        if participation_rate < quorum_threshold:
            return {
                "consensus_reached": False,
                "confidence": 0.0,
                "reason": f"Insufficient participation: {participation_rate:.2%} < {quorum_threshold:.2%}"
            }
        
        # Use consensus method with quorum validation
        return self._resolve_consensus(decision)
    
    def _resolve_emergent(self, decision: HiveDecision) -> Dict[str, Any]:
        """Resolve decision by detecting emergent patterns"""
        
        # Analyze voting patterns for emergence
        patterns = self._analyze_voting_patterns(decision)
        
        # Look for emergent consensus
        emergent_option = self._detect_emergent_consensus(patterns)
        
        if emergent_option:
            self.emergence_events.labels(type="emergent_consensus").inc()
            return {
                "consensus_reached": True,
                "chosen_option": emergent_option["option_id"],
                "confidence": emergent_option["emergence_strength"],
                "emergence_pattern": emergent_option["pattern"]
            }
        
        # Fall back to weighted voting
        return self._resolve_weighted_voting(decision)
    
    def _analyze_voting_patterns(self, decision: HiveDecision) -> Dict[str, Any]:
        """Analyze patterns in voting behavior"""
        
        patterns = {
            "temporal_clustering": [],
            "expertise_alignment": [],
            "network_effects": []
        }
        
        # Analyze temporal patterns
        vote_times = []
        for vote in decision.votes.values():
            vote_times.append(vote["vote_timestamp"])
        
        if len(vote_times) > 1:
            vote_times.sort()
            time_gaps = [vote_times[i+1] - vote_times[i] for i in range(len(vote_times)-1)]
            patterns["temporal_clustering"] = time_gaps
        
        return patterns
    
    def _detect_emergent_consensus(self, patterns: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect emergent consensus from voting patterns"""
        
        # Simple emergence detection - could be much more sophisticated
        temporal_clustering = patterns.get("temporal_clustering", [])
        
        if temporal_clustering:
            # Check for rapid convergence (emergence indicator)
            avg_gap = sum(temporal_clustering) / len(temporal_clustering)
            if avg_gap < 1.0:  # Quick succession of votes indicates emergence
                return {
                    "option_id": "emergent_consensus",
                    "emergence_strength": min(1.0, 2.0 - avg_gap),
                    "pattern": "rapid_convergence"
                }
        
        return None
    
    def _find_node_by_agent_id(self, agent_id: str) -> Optional[HiveNode]:
        """Find node by agent ID"""
        for node in self.nodes.values():
            if node.agent_id == agent_id:
                return node
        return None
    
    def _find_node_by_id(self, node_id: str) -> Optional[HiveNode]:
        """Find node by node ID"""
        return self.nodes.get(node_id)
    
    def _calculate_collective_confidence(self) -> float:
        """Calculate overall collective confidence"""
        if not self.decision_history:
            return 0.5  # Neutral starting point
        
        recent_decisions = self.decision_history[-10:]  # Last 10 decisions
        total_confidence = sum(d.confidence for d in recent_decisions)
        return total_confidence / len(recent_decisions)
    
    async def _detect_emergence_patterns(self, resolved_decision: HiveDecision):
        """Detect and record emergent patterns from resolved decisions"""
        
        # Pattern detection logic
        decision_signature = {
            "method": resolved_decision.method.value,
            "participant_count": len(resolved_decision.participants),
            "consensus_reached": resolved_decision.consensus_reached,
            "confidence": resolved_decision.confidence
        }
        
        # Store pattern for future learning
        pattern_key = f"pattern_{resolved_decision.method.value}_{len(resolved_decision.participants)}"
        
        if pattern_key not in self.behavioral_patterns:
            self.behavioral_patterns[pattern_key] = []
        
        self.behavioral_patterns[pattern_key].append(decision_signature)
        
        # Detect if this is an emergent behavior
        if len(self.behavioral_patterns[pattern_key]) >= 3:
            recent_patterns = self.behavioral_patterns[pattern_key][-3:]
            if self._is_emergent_pattern(recent_patterns):
                self.emergence_events.labels(type="behavioral_pattern").inc()
                self.logger.info(
                    "emergent_pattern_detected",
                    pattern_key=pattern_key,
                    occurrences=len(self.behavioral_patterns[pattern_key])
                )
    
    def _is_emergent_pattern(self, patterns: List[Dict[str, Any]]) -> bool:
        """Determine if patterns represent emergent behavior"""
        
        # Simple emergence detection: consistent high confidence + consensus
        high_confidence_count = sum(1 for p in patterns if p["confidence"] > 0.8)
        consensus_count = sum(1 for p in patterns if p["consensus_reached"])
        
        return high_confidence_count >= 2 and consensus_count >= 2
    
    async def decay_memory_relevance(self):
        """Apply decay to memory fragment relevance over time"""
        
        current_time = time.time()
        decayed_fragments = []
        
        for fragment in self.memory_store.values():
            # Calculate time-based decay
            time_since_access = current_time - fragment.last_accessed
            decay_factor = self.memory_decay_rate ** (time_since_access / 3600)  # Decay per hour
            
            fragment.relevance_decay *= decay_factor
            
            # Remove fragments that have decayed too much
            if fragment.relevance_decay < 0.1:
                decayed_fragments.append(fragment.fragment_id)
        
        # Remove decayed fragments
        for fragment_id in decayed_fragments:
            del self.memory_store[fragment_id]
            self.memory_operations.labels(operation="decay").inc()
        
        self.memory_fragments_gauge.set(len(self.memory_store))
        
        if decayed_fragments:
            self.logger.info("memory_decay_applied", removed_fragments=len(decayed_fragments))
    
    def get_hive_status(self) -> Dict[str, Any]:
        """Get current status of hive intelligence system"""
        
        return {
            "nodes": len(self.nodes),
            "memory_fragments": len(self.memory_store),
            "active_decisions": len(self.active_decisions),
            "decision_history": len(self.decision_history),
            "collective_confidence": self._calculate_collective_confidence(),
            "behavioral_patterns": len(self.behavioral_patterns),
            "average_node_connections": sum(len(node.connections) for node in self.nodes.values()) / len(self.nodes) if self.nodes else 0
        }

# Example usage
if __name__ == "__main__":
    async def main():
        hive = HiveIntelligence()
        
        # Initialize nodes
        node1 = await hive.initialize_hive_node("agent_1", ["development", "ai"])
        node2 = await hive.initialize_hive_node("agent_2", ["design", "research"]) 
        node3 = await hive.initialize_hive_node("agent_3", ["testing", "deployment"])
        
        # Store collective memory
        memory_id = await hive.store_collective_memory(
            "Best practices for AI development include proper testing and validation",
            HiveMemoryType.SEMANTIC,
            {"agent_1", "agent_3"},
            confidence=0.9
        )
        
        # Initiate decision
        decision_id = await hive.initiate_hive_decision(
            "Which development approach should we use?",
            [
                {"id": "agile", "required_expertise": [0, 1]},
                {"id": "waterfall", "required_expertise": [2, 3]},
                {"id": "hybrid", "required_expertise": [1, 2]}
            ],
            HiveDecisionMethod.CONSENSUS
        )
        
        # Wait for decision resolution
        await asyncio.sleep(5)
        
        # Check status
        status = hive.get_hive_status()
        print("Hive status:", json.dumps(status, indent=2))
        
    asyncio.run(main())