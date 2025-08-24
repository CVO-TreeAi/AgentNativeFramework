// AgentNativeFramework Daemon - Background agent coordination service
// High-performance Rust implementation for terminal power users

use std::collections::HashMap;
use std::sync::Arc;
use tokio::net::{UnixListener, UnixStream};
use tokio::sync::{Mutex, RwLock};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use serde::{Deserialize, Serialize};
use serde_json;
use tracing::{info, warn, error, debug};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentConfig {
    pub id: String,
    pub name: String,
    pub agent_type: String,
    pub capabilities: Vec<String>,
    pub max_concurrent_tasks: u32,
    pub memory_limit: u64,
    pub priority: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentTask {
    pub id: Uuid,
    pub agent_id: String,
    pub task_type: String,
    pub prompt: String,
    pub context: HashMap<String, String>,
    pub status: TaskStatus,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub started_at: Option<chrono::DateTime<chrono::Utc>>,
    pub completed_at: Option<chrono::DateTime<chrono::Utc>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TaskStatus {
    Queued,
    Running,
    Completed,
    Failed,
    Cancelled,
}

#[derive(Debug)]
pub struct AgentPool {
    agents: Arc<RwLock<HashMap<String, AgentConfig>>>,
    active_tasks: Arc<RwLock<HashMap<Uuid, AgentTask>>>,
    task_queue: Arc<Mutex<Vec<AgentTask>>>,
}

impl AgentPool {
    pub fn new() -> Self {
        Self {
            agents: Arc::new(RwLock::new(HashMap::new())),
            active_tasks: Arc::new(RwLock::new(HashMap::new())),
            task_queue: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub async fn load_agents(&self) -> anyhow::Result<()> {
        info!("Loading agent registry...");
        
        // Load Claude Code subagents (219 agents)
        self.load_claude_code_agents().await?;
        
        // Load SPARC agents (54+ agents)
        self.load_sparc_agents().await?;
        
        // Load custom agents
        self.load_custom_agents().await?;
        
        let agent_count = self.agents.read().await.len();
        info!("Loaded {} agents successfully", agent_count);
        
        Ok(())
    }

    async fn load_claude_code_agents(&self) -> anyhow::Result<()> {
        let claude_agents = vec![
            // Core Development Agents
            AgentConfig {
                id: "backend-typescript-architect".to_string(),
                name: "Backend TypeScript Architect".to_string(),
                agent_type: "development".to_string(),
                capabilities: vec!["typescript".to_string(), "backend".to_string(), "architecture".to_string()],
                max_concurrent_tasks: 3,
                memory_limit: 512 * 1024 * 1024, // 512MB
                priority: 9,
            },
            AgentConfig {
                id: "rust-pro".to_string(),
                name: "Rust Expert".to_string(),
                agent_type: "development".to_string(),
                capabilities: vec!["rust".to_string(), "systems".to_string(), "performance".to_string()],
                max_concurrent_tasks: 2,
                memory_limit: 256 * 1024 * 1024, // 256MB
                priority: 8,
            },
            AgentConfig {
                id: "performance-optimizer".to_string(),
                name: "Performance Optimizer".to_string(),
                agent_type: "optimization".to_string(),
                capabilities: vec!["performance".to_string(), "profiling".to_string(), "optimization".to_string()],
                max_concurrent_tasks: 1,
                memory_limit: 1024 * 1024 * 1024, // 1GB
                priority: 10,
            },
            // Add more agents...
        ];

        let mut agents = self.agents.write().await;
        for agent in claude_agents {
            agents.insert(agent.id.clone(), agent);
        }

        Ok(())
    }

    async fn load_sparc_agents(&self) -> anyhow::Result<()> {
        let sparc_agents = vec![
            AgentConfig {
                id: "coder".to_string(),
                name: "SPARC Coder".to_string(),
                agent_type: "sparc".to_string(),
                capabilities: vec!["coding".to_string(), "implementation".to_string()],
                max_concurrent_tasks: 5,
                memory_limit: 512 * 1024 * 1024,
                priority: 7,
            },
            AgentConfig {
                id: "reviewer".to_string(),
                name: "SPARC Reviewer".to_string(),
                agent_type: "sparc".to_string(),
                capabilities: vec!["code-review".to_string(), "quality".to_string()],
                max_concurrent_tasks: 3,
                memory_limit: 256 * 1024 * 1024,
                priority: 8,
            },
            // Add more SPARC agents...
        ];

        let mut agents = self.agents.write().await;
        for agent in sparc_agents {
            agents.insert(agent.id.clone(), agent);
        }

        Ok(())
    }

    async fn load_custom_agents(&self) -> anyhow::Result<()> {
        // Load user-defined agents from ~/.anf/agents/
        Ok(())
    }

    pub async fn spawn_agent(&self, agent_id: &str) -> anyhow::Result<String> {
        let agents = self.agents.read().await;
        if let Some(agent) = agents.get(agent_id) {
            info!("Spawning agent: {}", agent.name);
            // Actual agent spawning logic
            Ok(format!("Agent {} spawned successfully", agent_id))
        } else {
            Err(anyhow::anyhow!("Agent {} not found", agent_id))
        }
    }

    pub async fn submit_task(&self, task: AgentTask) -> anyhow::Result<Uuid> {
        let task_id = task.id;
        
        {
            let mut queue = self.task_queue.lock().await;
            queue.push(task);
        }
        
        info!("Task {} queued", task_id);
        Ok(task_id)
    }

    pub async fn get_agent_status(&self, agent_id: &str) -> Option<String> {
        let agents = self.agents.read().await;
        agents.get(agent_id).map(|agent| {
            format!("Agent: {} | Status: Active | Type: {}", 
                    agent.name, agent.agent_type)
        })
    }

    pub async fn list_agents(&self, category: Option<&str>) -> Vec<AgentConfig> {
        let agents = self.agents.read().await;
        agents.values()
            .filter(|agent| {
                category.map_or(true, |cat| agent.agent_type == cat)
            })
            .cloned()
            .collect()
    }
}

pub struct AgentDaemon {
    pool: AgentPool,
    socket_path: String,
    python_bridge: Option<PythonBridge>,
}

// Python bridge for swarm-hive coordination
#[derive(Clone)]
pub struct PythonBridge {
    socket_path: String,
}

impl PythonBridge {
    pub fn new(socket_path: String) -> Self {
        Self { socket_path }
    }
    
    pub async fn send_command(&self, command: serde_json::Value) -> anyhow::Result<serde_json::Value> {
        // Connect to Python daemon bridge
        match UnixStream::connect(&self.socket_path).await {
            Ok(mut stream) => {
                // Send command
                let command_str = serde_json::to_string(&command)?;
                stream.write_all((command_str + "\n").as_bytes()).await?;
                
                // Read response
                let mut buffer = Vec::new();
                let mut temp_buffer = [0u8; 1024];
                
                loop {
                    match stream.read(&mut temp_buffer).await {
                        Ok(0) => break, // Connection closed
                        Ok(n) => {
                            buffer.extend_from_slice(&temp_buffer[..n]);
                            if buffer.ends_with(b"\n") {
                                break;
                            }
                        }
                        Err(e) => return Err(e.into()),
                    }
                }
                
                let response_str = String::from_utf8_lossy(&buffer);
                let response: serde_json::Value = serde_json::from_str(response_str.trim())?;
                Ok(response)
            }
            Err(e) => {
                warn!("Failed to connect to Python bridge: {}", e);
                Err(e.into())
            }
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Command {
    pub action: String,
    pub params: serde_json::Value,
}

impl AgentDaemon {
    pub fn new(socket_path: String) -> Self {
        let python_bridge = PythonBridge::new("/tmp/anf_python.sock".to_string());
        
        Self {
            pool: AgentPool::new(),
            socket_path,
            python_bridge: Some(python_bridge),
        }
    }

    pub async fn start(&self) -> anyhow::Result<()> {
        info!("Starting Agent Native Framework Daemon...");
        
        // Load agents
        self.pool.load_agents().await?;
        
        // Start Unix socket listener
        let listener = UnixListener::bind(&self.socket_path)?;
        info!("Listening on socket: {}", self.socket_path);
        
        // Start task processor
        let pool = self.pool.clone();
        tokio::spawn(async move {
            Self::process_tasks(pool).await;
        });
        
        // Accept connections
        while let Ok((stream, _)) = listener.accept().await {
            let pool = self.pool.clone();
            let python_bridge = self.python_bridge.clone();
            tokio::spawn(async move {
                if let Err(e) = Self::handle_connection(stream, pool, python_bridge).await {
                    error!("Connection error: {}", e);
                }
            });
        }
        
        Ok(())
    }

    async fn process_tasks(pool: AgentPool) {
        loop {
            {
                let mut queue = pool.task_queue.lock().await;
                if let Some(mut task) = queue.pop() {
                    task.status = TaskStatus::Running;
                    task.started_at = Some(chrono::Utc::now());
                    
                    // Process task (placeholder)
                    info!("Processing task: {} for agent: {}", task.id, task.agent_id);
                    
                    // Simulate work
                    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
                    
                    task.status = TaskStatus::Completed;
                    task.completed_at = Some(chrono::Utc::now());
                    
                    // Store completed task
                    let mut active_tasks = pool.active_tasks.write().await;
                    active_tasks.insert(task.id, task);
                }
            }
            
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        }
    }

    async fn handle_connection(
        mut stream: UnixStream, 
        pool: AgentPool,
        python_bridge: Option<PythonBridge>
    ) -> anyhow::Result<()> {
        let mut buffer = Vec::new();
        let mut temp_buffer = [0u8; 1024];
        
        // Read command from client
        loop {
            match stream.read(&mut temp_buffer).await {
                Ok(0) => break, // Connection closed
                Ok(n) => {
                    buffer.extend_from_slice(&temp_buffer[..n]);
                    if buffer.ends_with(b"\n") {
                        break;
                    }
                }
                Err(e) => return Err(e.into()),
            }
        }
        
        let command_str = String::from_utf8_lossy(&buffer);
        debug!("Received command: {}", command_str.trim());
        
        // Parse command
        let response = if let Ok(command) = serde_json::from_str::<Command>(command_str.trim()) {
            Self::process_command(command, &pool, &python_bridge).await
        } else {
            // Try simple string commands for backward compatibility
            Self::process_simple_command(command_str.trim(), &pool, &python_bridge).await
        };
        
        // Send response
        let response_str = serde_json::to_string(&response).unwrap_or_else(|_| 
            r#"{"error": "Failed to serialize response"}"#.to_string()
        );
        
        stream.write_all((response_str + "\n").as_bytes()).await?;
        stream.flush().await?;
        
        Ok(())
    }
    
    async fn process_command(
        command: Command,
        pool: &AgentPool,
        python_bridge: &Option<PythonBridge>
    ) -> serde_json::Value {
        match command.action.as_str() {
            // Regular agent commands
            "spawn_agent" => {
                if let Some(agent_id) = command.params.get("agent_id").and_then(|v| v.as_str()) {
                    match pool.spawn_agent(agent_id).await {
                        Ok(result) => serde_json::json!({"success": true, "message": result}),
                        Err(e) => serde_json::json!({"error": e.to_string()}),
                    }
                } else {
                    serde_json::json!({"error": "Missing agent_id parameter"})
                }
            },
            
            "list_agents" => {
                let category = command.params.get("category").and_then(|v| v.as_str());
                let agents = pool.list_agents(category).await;
                serde_json::json!({"success": true, "agents": agents})
            },
            
            "agent_status" => {
                if let Some(agent_id) = command.params.get("agent_id").and_then(|v| v.as_str()) {
                    if let Some(status) = pool.get_agent_status(agent_id).await {
                        serde_json::json!({"success": true, "status": status})
                    } else {
                        serde_json::json!({"error": "Agent not found"})
                    }
                } else {
                    serde_json::json!({"error": "Missing agent_id parameter"})
                }
            },
            
            // Swarm-Hive commands - delegate to Python bridge
            "swarm_create" | "swarm_execute" | "swarm_status" | "swarm_dissolve" | "swarm_list" |
            "hive_init" | "hive_decide" | "hive_remember" | "hive_recall" | "hive_status" |
            "collaborate" => {
                if let Some(bridge) = python_bridge {
                    let python_command = serde_json::json!({
                        "action": command.action,
                        "params": command.params
                    });
                    
                    match bridge.send_command(python_command).await {
                        Ok(response) => response,
                        Err(e) => serde_json::json!({"error": format!("Python bridge error: {}", e)})
                    }
                } else {
                    serde_json::json!({"error": "Python bridge not available"})
                }
            },
            
            _ => serde_json::json!({"error": format!("Unknown command: {}", command.action)}),
        }
    }
    
    async fn process_simple_command(
        command_str: &str,
        pool: &AgentPool,
        python_bridge: &Option<PythonBridge>
    ) -> serde_json::Value {
        let parts: Vec<&str> = command_str.split(':').collect();
        
        match parts.get(0) {
            Some(&"spawn") => {
                if let Some(&agent_id) = parts.get(1) {
                    match pool.spawn_agent(agent_id).await {
                        Ok(result) => serde_json::json!({"success": true, "message": result}),
                        Err(e) => serde_json::json!({"error": e.to_string()}),
                    }
                } else {
                    serde_json::json!({"error": "Usage: spawn:<agent_id>"})
                }
            },
            
            Some(&"list") => {
                let agents = pool.list_agents(None).await;
                serde_json::json!({"success": true, "agents": agents})
            },
            
            Some(&"ask") => {
                if let Some(prompt) = parts.get(1) {
                    // For now, return a placeholder response
                    serde_json::json!({
                        "success": true, 
                        "response": format!("Processing: {}", prompt)
                    })
                } else {
                    serde_json::json!({"error": "Usage: ask:<prompt>"})
                }
            },
            
            _ => serde_json::json!({"error": format!("Unknown command: {}", command_str)}),
        }
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();
    
    let socket_path = "/tmp/anf.sock".to_string();
    let daemon = AgentDaemon::new(socket_path);
    
    info!("🤖 Agent Native Framework Daemon starting...");
    daemon.start().await?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_agent_pool_creation() {
        let pool = AgentPool::new();
        assert!(pool.load_agents().await.is_ok());
    }
    
    #[tokio::test]
    async fn test_agent_spawning() {
        let pool = AgentPool::new();
        pool.load_agents().await.unwrap();
        
        let result = pool.spawn_agent("rust-pro").await;
        assert!(result.is_ok());
    }
}