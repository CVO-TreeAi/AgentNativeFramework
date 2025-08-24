"""
AgentNativeFramework - Health Check and Monitoring System
Provides comprehensive health monitoring for agent operations
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import psutil
from prometheus_client import Gauge, Counter, Histogram
import structlog

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    timestamp: float
    duration_ms: float
    metadata: Dict[str, Any] = None

class HealthMonitor:
    """
    Comprehensive health monitoring for agent operations
    """
    
    # Health metrics
    health_check_duration = Histogram('health_check_duration_seconds', 'Health check execution time', ['check_name'])
    health_status_gauge = Gauge('health_status', 'Current health status (1=healthy, 0=unhealthy)', ['component'])
    failed_health_checks = Counter('failed_health_checks_total', 'Total failed health checks', ['check_name'])
    
    def __init__(self, agent_manager=None):
        self.logger = structlog.get_logger(__name__)
        self.agent_manager = agent_manager
        self.health_checks: List[HealthCheck] = []
        self.last_full_check = 0
        
    async def perform_full_health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of all components
        """
        start_time = time.time()
        checks = []
        
        # Core system health
        checks.append(await self._check_system_resources())
        checks.append(await self._check_agent_manager())
        checks.append(await self._check_memory_usage())
        checks.append(await self._check_coordination_health())
        
        # Agent-specific health
        if self.agent_manager:
            checks.append(await self._check_active_agents())
            checks.append(await self._check_agent_memory())
            checks.append(await self._check_coordination_performance())
        
        # Overall health determination
        overall_status = self._determine_overall_health(checks)
        
        duration = time.time() - start_time
        self.last_full_check = time.time()
        
        health_report = {
            "status": overall_status.value,
            "timestamp": time.time(),
            "duration_ms": duration * 1000,
            "checks": [self._serialize_check(check) for check in checks],
            "summary": self._generate_health_summary(checks)
        }
        
        # Update metrics
        self.health_status_gauge.labels(component="overall").set(1 if overall_status == HealthStatus.HEALTHY else 0)
        
        self.logger.info("health_check_completed", 
                        status=overall_status.value, 
                        duration_ms=duration * 1000,
                        checks_count=len(checks))
        
        return health_report
    
    async def _check_system_resources(self) -> HealthCheck:
        """Check system resource utilization"""
        start_time = time.time()
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Determine health based on resource usage
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
                status = HealthStatus.CRITICAL
                message = f"High resource usage: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%"
            elif cpu_percent > 70 or memory.percent > 70 or disk.percent > 80:
                status = HealthStatus.DEGRADED
                message = f"Moderate resource usage: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal resource usage: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%"
            
            metadata = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3)
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Failed to check system resources: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="system_resources").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="system_resources").observe(duration / 1000)
        
        return HealthCheck("system_resources", status, message, time.time(), duration, metadata)
    
    async def _check_agent_manager(self) -> HealthCheck:
        """Check agent manager health"""
        start_time = time.time()
        
        try:
            if not self.agent_manager:
                status = HealthStatus.UNHEALTHY
                message = "Agent manager not initialized"
                metadata = {}
            else:
                registry_size = len(self.agent_manager.get_agent_registry())
                active_count = len(self.agent_manager.get_active_agents())
                
                if registry_size == 0:
                    status = HealthStatus.CRITICAL
                    message = "No agents in registry"
                elif active_count > 20:  # Too many active agents
                    status = HealthStatus.DEGRADED
                    message = f"High active agent count: {active_count}"
                else:
                    status = HealthStatus.HEALTHY
                    message = f"Agent manager healthy: {registry_size} registered, {active_count} active"
                
                metadata = {
                    "registry_size": registry_size,
                    "active_agents": active_count,
                    "decision_history_length": len(self.agent_manager.decision_history)
                }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Agent manager check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="agent_manager").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="agent_manager").observe(duration / 1000)
        
        return HealthCheck("agent_manager", status, message, time.time(), duration, metadata)
    
    async def _check_memory_usage(self) -> HealthCheck:
        """Check application memory usage"""
        start_time = time.time()
        
        try:
            import gc
            gc.collect()
            
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            
            # Memory thresholds
            if memory_mb > 2048:  # 2GB
                status = HealthStatus.CRITICAL
                message = f"High memory usage: {memory_mb:.1f}MB"
            elif memory_mb > 1024:  # 1GB
                status = HealthStatus.DEGRADED
                message = f"Moderate memory usage: {memory_mb:.1f}MB"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal memory usage: {memory_mb:.1f}MB"
            
            metadata = {
                "memory_mb": memory_mb,
                "memory_percent": process.memory_percent(),
                "gc_objects": len(gc.get_objects())
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Memory check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="memory_usage").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="memory_usage").observe(duration / 1000)
        
        return HealthCheck("memory_usage", status, message, time.time(), duration, metadata)
    
    async def _check_coordination_health(self) -> HealthCheck:
        """Check agent coordination system health"""
        start_time = time.time()
        
        try:
            if not self.agent_manager:
                status = HealthStatus.UNHEALTHY
                message = "No agent manager for coordination check"
                metadata = {}
            else:
                decision_count = len(self.agent_manager.decision_history)
                
                # Check recent decision success rate
                recent_decisions = self.agent_manager.decision_history[-10:] if decision_count >= 10 else self.agent_manager.decision_history
                
                if not recent_decisions:
                    status = HealthStatus.HEALTHY
                    message = "No coordination decisions yet"
                else:
                    failed_decisions = sum(1 for d in recent_decisions if 'error' in d.get('result', {}))
                    success_rate = (len(recent_decisions) - failed_decisions) / len(recent_decisions)
                    
                    if success_rate < 0.5:
                        status = HealthStatus.CRITICAL
                        message = f"Low coordination success rate: {success_rate:.2%}"
                    elif success_rate < 0.8:
                        status = HealthStatus.DEGRADED
                        message = f"Moderate coordination success rate: {success_rate:.2%}"
                    else:
                        status = HealthStatus.HEALTHY
                        message = f"Good coordination success rate: {success_rate:.2%}"
                
                metadata = {
                    "total_decisions": decision_count,
                    "recent_decisions": len(recent_decisions),
                    "success_rate": success_rate if recent_decisions else 1.0
                }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Coordination health check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="coordination_health").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="coordination_health").observe(duration / 1000)
        
        return HealthCheck("coordination_health", status, message, time.time(), duration, metadata)
    
    async def _check_active_agents(self) -> HealthCheck:
        """Check active agent health"""
        start_time = time.time()
        
        try:
            active_agents = self.agent_manager.get_active_agents()
            agent_count = len(active_agents)
            
            if agent_count == 0:
                status = HealthStatus.HEALTHY
                message = "No active agents (idle state)"
            elif agent_count > 16:
                status = HealthStatus.DEGRADED
                message = f"High active agent count: {agent_count}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Normal active agent count: {agent_count}"
            
            # Check agent distribution by tier
            tier_distribution = {}
            for agent in active_agents.values():
                tier = agent.tier.value
                tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
            
            metadata = {
                "active_count": agent_count,
                "tier_distribution": tier_distribution,
                "agent_ids": list(active_agents.keys())
            }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Active agent check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="active_agents").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="active_agents").observe(duration / 1000)
        
        return HealthCheck("active_agents", status, message, time.time(), duration, metadata)
    
    async def _check_agent_memory(self) -> HealthCheck:
        """Check agent memory and context usage"""
        start_time = time.time()
        
        try:
            # This would check agent-specific memory usage
            # For now, it's a placeholder
            status = HealthStatus.HEALTHY
            message = "Agent memory check not implemented"
            metadata = {"note": "Placeholder for agent memory monitoring"}
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Agent memory check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="agent_memory").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="agent_memory").observe(duration / 1000)
        
        return HealthCheck("agent_memory", status, message, time.time(), duration, metadata)
    
    async def _check_coordination_performance(self) -> HealthCheck:
        """Check coordination system performance"""
        start_time = time.time()
        
        try:
            # Analyze recent coordination performance
            if not self.agent_manager.decision_history:
                status = HealthStatus.HEALTHY
                message = "No coordination history to analyze"
                metadata = {}
            else:
                recent_decisions = self.agent_manager.decision_history[-5:]
                avg_duration = sum(d.get('result', {}).get('duration', 0) for d in recent_decisions) / len(recent_decisions)
                
                if avg_duration > 30:  # 30 seconds
                    status = HealthStatus.DEGRADED
                    message = f"Slow coordination: {avg_duration:.1f}s average"
                else:
                    status = HealthStatus.HEALTHY
                    message = f"Good coordination performance: {avg_duration:.1f}s average"
                
                metadata = {
                    "avg_coordination_duration": avg_duration,
                    "recent_decisions_count": len(recent_decisions)
                }
            
        except Exception as e:
            status = HealthStatus.UNHEALTHY
            message = f"Coordination performance check failed: {e}"
            metadata = {"error": str(e)}
            self.failed_health_checks.labels(check_name="coordination_performance").inc()
        
        duration = (time.time() - start_time) * 1000
        self.health_check_duration.labels(check_name="coordination_performance").observe(duration / 1000)
        
        return HealthCheck("coordination_performance", status, message, time.time(), duration, metadata)
    
    def _determine_overall_health(self, checks: List[HealthCheck]) -> HealthStatus:
        """Determine overall health status from individual checks"""
        if any(check.status == HealthStatus.CRITICAL for check in checks):
            return HealthStatus.CRITICAL
        elif any(check.status == HealthStatus.UNHEALTHY for check in checks):
            return HealthStatus.UNHEALTHY
        elif any(check.status == HealthStatus.DEGRADED for check in checks):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
    
    def _serialize_check(self, check: HealthCheck) -> Dict[str, Any]:
        """Serialize health check for JSON output"""
        return {
            "name": check.name,
            "status": check.status.value,
            "message": check.message,
            "timestamp": check.timestamp,
            "duration_ms": check.duration_ms,
            "metadata": check.metadata or {}
        }
    
    def _generate_health_summary(self, checks: List[HealthCheck]) -> Dict[str, Any]:
        """Generate summary statistics from health checks"""
        status_counts = {}
        for check in checks:
            status = check.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_checks": len(checks),
            "status_distribution": status_counts,
            "failed_checks": [check.name for check in checks if check.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL]],
            "degraded_checks": [check.name for check in checks if check.status == HealthStatus.DEGRADED]
        }
    
    async def get_readiness_probe(self) -> Dict[str, Any]:
        """Kubernetes readiness probe endpoint"""
        try:
            # Quick checks for readiness
            ready = True
            message = "Service ready"
            
            if self.agent_manager is None:
                ready = False
                message = "Agent manager not initialized"
            
            return {
                "ready": ready,
                "message": message,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "ready": False,
                "message": f"Readiness check failed: {e}",
                "timestamp": time.time()
            }
    
    async def get_liveness_probe(self) -> Dict[str, Any]:
        """Kubernetes liveness probe endpoint"""
        try:
            # Basic liveness check
            alive = time.time() - self.last_full_check < 300  # 5 minutes
            message = "Service alive" if alive else "Service may be stuck"
            
            return {
                "alive": alive,
                "message": message,
                "timestamp": time.time(),
                "last_health_check": self.last_full_check
            }
        except Exception as e:
            return {
                "alive": False,
                "message": f"Liveness check failed: {e}",
                "timestamp": time.time()
            }