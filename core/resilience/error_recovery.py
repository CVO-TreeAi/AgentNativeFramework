"""
AgentNativeFramework - Error Recovery and Resilience System
Implements circuit breakers, retries, and graceful degradation
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import functools
from prometheus_client import Counter, Histogram, Gauge
import structlog

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_multiplier: float = 2.0
    jitter: bool = True

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    success_threshold: int = 3
    timeout: float = 30.0

class AgentError(Exception):
    """Base exception for agent-related errors"""
    def __init__(self, message: str, agent_id: str = None, recoverable: bool = True):
        super().__init__(message)
        self.agent_id = agent_id
        self.recoverable = recoverable

class CoordinationError(AgentError):
    """Error in agent coordination process"""
    pass

class ResourceExhaustionError(AgentError):
    """System resource exhaustion error"""
    def __init__(self, message: str, agent_id: str = None):
        super().__init__(message, agent_id, recoverable=False)

class CircuitBreaker:
    """
    Circuit breaker implementation for agent operations
    """
    
    # Circuit breaker metrics
    circuit_breaker_state = Gauge('circuit_breaker_state', 'Circuit breaker state (0=closed, 1=open, 2=half_open)', ['circuit_name'])
    circuit_breaker_trips = Counter('circuit_breaker_trips_total', 'Total circuit breaker trips', ['circuit_name'])
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.logger = structlog.get_logger(__name__)
        
        # Update initial metric
        self.circuit_breaker_state.labels(circuit_name=name).set(0)
    
    async def call(self, func: Callable, *args, **kwargs):
        """
        Execute function through circuit breaker
        """
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.config.recovery_timeout:
                self._transition_to_half_open()
            else:
                raise AgentError(f"Circuit breaker {self.name} is OPEN")
        
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=self.config.timeout
            )
            
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise AgentError(f"Circuit breaker {self.name} failed: {e}")
    
    def _on_success(self):
        """Handle successful operation"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._transition_to_closed()
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed operation"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self._transition_to_open()
    
    def _transition_to_closed(self):
        """Transition to closed state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.circuit_breaker_state.labels(circuit_name=self.name).set(0)
        self.logger.info("circuit_breaker_closed", circuit=self.name)
    
    def _transition_to_open(self):
        """Transition to open state"""
        self.state = CircuitState.OPEN
        self.circuit_breaker_trips.labels(circuit_name=self.name).inc()
        self.circuit_breaker_state.labels(circuit_name=self.name).set(1)
        self.logger.warning("circuit_breaker_opened", circuit=self.name, failure_count=self.failure_count)
    
    def _transition_to_half_open(self):
        """Transition to half-open state"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.circuit_breaker_state.labels(circuit_name=self.name).set(2)
        self.logger.info("circuit_breaker_half_open", circuit=self.name)

class RetryHandler:
    """
    Retry handler with exponential backoff and jitter
    """
    
    retry_attempts = Counter('retry_attempts_total', 'Total retry attempts', ['operation', 'attempt'])
    retry_duration = Histogram('retry_duration_seconds', 'Total retry duration', ['operation'])
    
    def __init__(self, config: RetryConfig):
        self.config = config
        self.logger = structlog.get_logger(__name__)
    
    async def retry(self, operation: str, func: Callable, *args, **kwargs):
        """
        Execute function with retry logic
        """
        start_time = time.time()
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                self.retry_attempts.labels(operation=operation, attempt=attempt + 1).inc()
                result = await func(*args, **kwargs)
                
                if attempt > 0:
                    duration = time.time() - start_time
                    self.retry_duration.labels(operation=operation).observe(duration)
                    self.logger.info("retry_succeeded", operation=operation, attempt=attempt + 1, duration=duration)
                
                return result
                
            except Exception as e:
                last_exception = e
                
                if attempt + 1 >= self.config.max_attempts:
                    break
                
                # Check if error is retryable
                if isinstance(e, AgentError) and not e.recoverable:
                    self.logger.error("non_retryable_error", operation=operation, error=str(e))
                    break
                
                delay = self._calculate_delay(attempt)
                self.logger.warning("retry_attempt_failed", 
                                  operation=operation, 
                                  attempt=attempt + 1, 
                                  error=str(e), 
                                  next_delay=delay)
                
                await asyncio.sleep(delay)
        
        # All retries failed
        duration = time.time() - start_time
        self.retry_duration.labels(operation=operation).observe(duration)
        self.logger.error("retry_exhausted", operation=operation, attempts=self.config.max_attempts, duration=duration)
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for next retry attempt"""
        delay = min(
            self.config.initial_delay * (self.config.backoff_multiplier ** attempt),
            self.config.max_delay
        )
        
        if self.config.jitter:
            import random
            delay *= (0.5 + random.random())
        
        return delay

class ErrorRecoveryManager:
    """
    Central error recovery and resilience manager
    """
    
    error_recovery_attempts = Counter('error_recovery_attempts_total', 'Error recovery attempts', ['error_type', 'status'])
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_handler = RetryHandler(RetryConfig())
        self.logger = structlog.get_logger(__name__)
        
        # Initialize circuit breakers for key operations
        self._initialize_circuit_breakers()
    
    def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for critical operations"""
        configs = {
            "agent_activation": CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30),
            "agent_coordination": CircuitBreakerConfig(failure_threshold=5, recovery_timeout=60),
            "democratic_decision": CircuitBreakerConfig(failure_threshold=2, recovery_timeout=45),
            "context_management": CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30)
        }
        
        for name, config in configs.items():
            self.circuit_breakers[name] = CircuitBreaker(name, config)
    
    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(name, CircuitBreakerConfig())
        return self.circuit_breakers[name]
    
    async def execute_with_resilience(self, operation: str, func: Callable, *args, **kwargs):
        """
        Execute operation with full resilience (circuit breaker + retry)
        """
        circuit_breaker = self.get_circuit_breaker(operation)
        
        async def wrapped_operation():
            return await circuit_breaker.call(func, *args, **kwargs)
        
        return await self.retry_handler.retry(operation, wrapped_operation)
    
    async def handle_agent_error(self, error: AgentError, agent_id: str = None) -> bool:
        """
        Handle specific agent error and attempt recovery
        """
        try:
            self.error_recovery_attempts.labels(error_type=type(error).__name__, status="attempted").inc()
            
            if isinstance(error, ResourceExhaustionError):
                success = await self._handle_resource_exhaustion(error, agent_id)
            elif isinstance(error, CoordinationError):
                success = await self._handle_coordination_error(error, agent_id)
            else:
                success = await self._handle_generic_error(error, agent_id)
            
            if success:
                self.error_recovery_attempts.labels(error_type=type(error).__name__, status="success").inc()
                self.logger.info("error_recovery_successful", error_type=type(error).__name__, agent_id=agent_id)
            else:
                self.error_recovery_attempts.labels(error_type=type(error).__name__, status="failed").inc()
                self.logger.error("error_recovery_failed", error_type=type(error).__name__, agent_id=agent_id)
            
            return success
            
        except Exception as recovery_error:
            self.error_recovery_attempts.labels(error_type=type(error).__name__, status="error").inc()
            self.logger.error("error_recovery_exception", 
                            original_error=str(error), 
                            recovery_error=str(recovery_error), 
                            agent_id=agent_id)
            return False
    
    async def _handle_resource_exhaustion(self, error: ResourceExhaustionError, agent_id: str = None) -> bool:
        """Handle resource exhaustion errors"""
        self.logger.warning("handling_resource_exhaustion", agent_id=agent_id, error=str(error))
        
        # Attempt to free resources
        import gc
        gc.collect()
        
        # TODO: Implement agent deactivation if needed
        # TODO: Implement resource cleanup
        
        return True  # Assume cleanup successful for now
    
    async def _handle_coordination_error(self, error: CoordinationError, agent_id: str = None) -> bool:
        """Handle coordination errors"""
        self.logger.warning("handling_coordination_error", agent_id=agent_id, error=str(error))
        
        # TODO: Implement coordination recovery
        # - Reset decision state
        # - Restart coordination process
        # - Fallback to single-agent mode
        
        return False  # Not implemented yet
    
    async def _handle_generic_error(self, error: AgentError, agent_id: str = None) -> bool:
        """Handle generic agent errors"""
        self.logger.warning("handling_generic_error", agent_id=agent_id, error=str(error))
        
        # Basic recovery attempt
        await asyncio.sleep(1)  # Brief pause
        return error.recoverable

def with_circuit_breaker(circuit_name: str, config: CircuitBreakerConfig = None):
    """
    Decorator to add circuit breaker to a function
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            recovery_manager = ErrorRecoveryManager()
            circuit_breaker = recovery_manager.get_circuit_breaker(circuit_name)
            return await circuit_breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator

def with_retry(config: RetryConfig = None):
    """
    Decorator to add retry logic to a function
    """
    retry_config = config or RetryConfig()
    retry_handler = RetryHandler(retry_config)
    
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            operation_name = f"{func.__module__}.{func.__name__}"
            return await retry_handler.retry(operation_name, func, *args, **kwargs)
        return wrapper
    return decorator

def with_resilience(circuit_name: str = None, retry_config: RetryConfig = None):
    """
    Decorator to add full resilience (circuit breaker + retry) to a function
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            operation_name = circuit_name or f"{func.__module__}.{func.__name__}"
            recovery_manager = ErrorRecoveryManager()
            return await recovery_manager.execute_with_resilience(operation_name, func, *args, **kwargs)
        return wrapper
    return decorator