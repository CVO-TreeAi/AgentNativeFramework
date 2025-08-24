// Wave Terminal Integration for ANF
// Enhanced terminal features and seamless integration

use std::collections::HashMap;
use std::env;
use std::process::{Command, Stdio};
use serde::{Deserialize, Serialize};
use tokio::process::Command as AsyncCommand;

#[derive(Debug, Serialize, Deserialize)]
pub struct WaveSession {
    pub session_id: String,
    pub tabs: Vec<WaveTab>,
    pub current_tab: usize,
    pub agents: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct WaveTab {
    pub tab_id: String,
    pub title: String,
    pub agent_id: Option<String>,
    pub context_path: Option<String>,
    pub split_panes: Vec<WavePane>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct WavePane {
    pub pane_id: String,
    pub agent_id: Option<String>,
    pub command: Option<String>,
    pub working_directory: Option<String>,
}

pub struct WaveIntegration {
    config: WaveConfig,
}

#[derive(Debug, Clone)]
pub struct WaveConfig {
    pub wave_app_path: String,
    pub enable_tab_management: bool,
    pub enable_pane_splitting: bool,
    pub auto_spawn_agents: bool,
    pub session_persistence: bool,
}

impl Default for WaveConfig {
    fn default() -> Self {
        Self {
            wave_app_path: "/Applications/Wave.app/Contents/MacOS/Wave".to_string(),
            enable_tab_management: true,
            enable_pane_splitting: true,
            auto_spawn_agents: true,
            session_persistence: true,
        }
    }
}

impl WaveIntegration {
    pub fn new(config: Option<WaveConfig>) -> Self {
        Self {
            config: config.unwrap_or_default(),
        }
    }

    /// Check if running in Wave Terminal
    pub fn is_wave_terminal() -> bool {
        env::var("TERM_PROGRAM")
            .map(|term| term.contains("wave"))
            .unwrap_or(false) ||
        env::var("WAVETERM")
            .map(|_| true)
            .unwrap_or(false)
    }

    /// Get current Wave session information
    pub async fn get_current_session(&self) -> anyhow::Result<Option<WaveSession>> {
        if !Self::is_wave_terminal() {
            return Ok(None);
        }

        // Use Wave's session API if available
        let output = AsyncCommand::new("wave")
            .args(&["session", "info", "--json"])
            .output()
            .await?;

        if output.status.success() {
            let session_data = String::from_utf8(output.stdout)?;
            let session: WaveSession = serde_json::from_str(&session_data)?;
            Ok(Some(session))
        } else {
            Ok(None)
        }
    }

    /// Create new tab with agent
    pub async fn create_agent_tab(&self, agent_id: &str, context_path: Option<&str>) -> anyhow::Result<String> {
        if !Self::is_wave_terminal() {
            return Err(anyhow::anyhow!("Not running in Wave Terminal"));
        }

        let tab_title = format!("🤖 {}", agent_id);
        let mut cmd = AsyncCommand::new("wave");
        cmd.args(&["tab", "create", "--title", &tab_title]);

        if let Some(path) = context_path {
            cmd.args(&["--cwd", path]);
        }

        // Start ANF in the new tab
        cmd.args(&["--command", &format!("anf spawn {}", agent_id)]);

        let output = cmd.output().await?;
        
        if output.status.success() {
            let tab_id = String::from_utf8(output.stdout)?;
            Ok(tab_id.trim().to_string())
        } else {
            Err(anyhow::anyhow!("Failed to create Wave tab: {}", String::from_utf8_lossy(&output.stderr)))
        }
    }

    /// Split pane with different agent
    pub async fn split_pane_with_agent(&self, agent_id: &str, direction: SplitDirection) -> anyhow::Result<String> {
        if !Self::is_wave_terminal() {
            return Err(anyhow::anyhow!("Not running in Wave Terminal"));
        }

        let direction_arg = match direction {
            SplitDirection::Horizontal => "horizontal",
            SplitDirection::Vertical => "vertical",
        };

        let output = AsyncCommand::new("wave")
            .args(&[
                "pane", "split", 
                "--direction", direction_arg,
                "--command", &format!("anf spawn {}", agent_id)
            ])
            .output()
            .await?;

        if output.status.success() {
            let pane_id = String::from_utf8(output.stdout)?;
            Ok(pane_id.trim().to_string())
        } else {
            Err(anyhow::anyhow!("Failed to split pane: {}", String::from_utf8_lossy(&output.stderr)))
        }
    }

    /// Save current session with active agents
    pub async fn save_session(&self, session_name: &str) -> anyhow::Result<()> {
        if !Self::is_wave_terminal() {
            return Ok(()); // Gracefully handle non-Wave environments
        }

        // Get current session state
        let session = self.get_current_session().await?;
        
        if let Some(session) = session {
            // Save session configuration
            let session_file = format!("{}/.anf/sessions/{}.json", 
                env::var("HOME").unwrap_or_default(), 
                session_name
            );

            // Ensure directory exists
            if let Some(parent) = std::path::Path::new(&session_file).parent() {
                std::fs::create_dir_all(parent)?;
            }

            let session_json = serde_json::to_string_pretty(&session)?;
            std::fs::write(&session_file, session_json)?;

            // Also save in Wave's session format if supported
            let _ = AsyncCommand::new("wave")
                .args(&["session", "save", session_name])
                .output()
                .await;
        }

        Ok(())
    }

    /// Restore session with agents
    pub async fn restore_session(&self, session_name: &str) -> anyhow::Result<()> {
        let session_file = format!("{}/.anf/sessions/{}.json", 
            env::var("HOME").unwrap_or_default(), 
            session_name
        );

        if !std::path::Path::new(&session_file).exists() {
            return Err(anyhow::anyhow!("Session file not found: {}", session_file));
        }

        let session_data = std::fs::read_to_string(&session_file)?;
        let session: WaveSession = serde_json::from_str(&session_data)?;

        // Restore tabs and panes with agents
        for tab in &session.tabs {
            if let Some(agent_id) = &tab.agent_id {
                self.create_agent_tab(agent_id, tab.context_path.as_deref()).await?;
            }

            // Restore split panes
            for pane in &tab.split_panes {
                if let Some(agent_id) = &pane.agent_id {
                    self.split_pane_with_agent(agent_id, SplitDirection::Vertical).await?;
                }
            }
        }

        Ok(())
    }

    /// Setup Wave Terminal for optimal ANF experience  
    pub async fn setup_wave_environment(&self) -> anyhow::Result<()> {
        if !Self::is_wave_terminal() {
            return Ok(());
        }

        // Configure Wave for better ANF integration
        let config_commands = vec![
            // Enable better color support
            ("set", "term.colors", "truecolor"),
            // Optimize for agent output
            ("set", "terminal.scrollback", "10000"),
            // Better font for code and symbols
            ("set", "terminal.font", "JetBrains Mono"),
            // Enable mouse support
            ("set", "terminal.mouse", "true"),
        ];

        for (cmd, key, value) in config_commands {
            let _ = AsyncCommand::new("wave")
                .args(&["config", cmd, key, value])
                .output()
                .await;
        }

        Ok(())
    }

    /// Create development environment layout
    pub async fn create_dev_environment(&self, project_path: &str, agents: &[&str]) -> anyhow::Result<()> {
        if !Self::is_wave_terminal() {
            return Err(anyhow::anyhow!("Wave Terminal required for environment creation"));
        }

        // Create main tab for coordination
        let main_tab = self.create_agent_tab("project-supervisor-orchestrator", Some(project_path)).await?;

        // Create specialized tabs for different agents
        for (i, &agent) in agents.iter().enumerate() {
            if i == 0 {
                // Use the main tab for the first agent
                continue;
            }

            // Create additional tabs for other agents
            self.create_agent_tab(agent, Some(project_path)).await?;
        }

        // Split the main tab for monitoring
        self.split_pane_with_agent("performance-optimizer", SplitDirection::Horizontal).await?;

        Ok(())
    }

    /// Get Wave Terminal specific information for better agent display
    pub fn get_wave_display_info(&self) -> WaveDisplayInfo {
        let mut info = WaveDisplayInfo::default();

        if Self::is_wave_terminal() {
            // Get terminal dimensions from Wave
            if let Ok(output) = std::process::Command::new("wave")
                .args(&["info", "terminal", "--json"])
                .output() 
            {
                if output.status.success() {
                    if let Ok(data) = String::from_utf8(output.stdout) {
                        if let Ok(parsed) = serde_json::from_str::<serde_json::Value>(&data) {
                            info.width = parsed.get("width").and_then(|v| v.as_u64()).unwrap_or(80) as u16;
                            info.height = parsed.get("height").and_then(|v| v.as_u64()).unwrap_or(24) as u16;
                            info.supports_truecolor = true;
                            info.supports_mouse = true;
                            info.supports_hyperlinks = true;
                        }
                    }
                }
            }
        }

        info
    }
}

#[derive(Debug)]
pub enum SplitDirection {
    Horizontal,
    Vertical,
}

#[derive(Debug)]
pub struct WaveDisplayInfo {
    pub width: u16,
    pub height: u16,
    pub supports_truecolor: bool,
    pub supports_mouse: bool,
    pub supports_hyperlinks: bool,
    pub supports_images: bool,
}

impl Default for WaveDisplayInfo {
    fn default() -> Self {
        Self {
            width: 80,
            height: 24,
            supports_truecolor: false,
            supports_mouse: false,
            supports_hyperlinks: false,
            supports_images: false,
        }
    }
}

/// Wave Terminal specific UI enhancements
pub struct WaveUI {
    display_info: WaveDisplayInfo,
}

impl WaveUI {
    pub fn new() -> Self {
        let integration = WaveIntegration::new(None);
        Self {
            display_info: integration.get_wave_display_info(),
        }
    }

    /// Create enhanced agent status display for Wave
    pub fn render_agent_status_wave(&self, agent_id: &str, status: &str) -> String {
        let width = self.display_info.width as usize;
        
        if self.display_info.supports_truecolor {
            // Use full RGB colors for better visual appeal
            format!(
                "\x1b[38;2;0;255;255m┌─ Agent: {} \x1b[38;2;100;100;100m{}\x1b[0m\n\
                 \x1b[38;2;0;150;255m│ Status: {} │ Memory: 45MB │ Tasks: 2 │ Queue: 0 {}\x1b[0m\n\
                 \x1b[38;2;0;255;255m└{}\x1b[0m",
                agent_id,
                "─".repeat(width.saturating_sub(agent_id.len() + 12)),
                status,
                " ".repeat(width.saturating_sub(50)),
                "─".repeat(width.saturating_sub(2))
            )
        } else {
            // Fallback for basic color support
            format!(
                "┌─ Agent: {} {}\n\
                 │ Status: {} │ Memory: 45MB │ Tasks: 2 │ Queue: 0\n\
                 └{}",
                agent_id,
                "─".repeat(width.saturating_sub(agent_id.len() + 12)),
                status,
                "─".repeat(width.saturating_sub(2))
            )
        }
    }

    /// Create interactive agent picker for Wave Terminal
    pub fn create_agent_picker(&self, agents: &[(&str, &str, &str)]) -> String {
        let mut output = String::new();
        
        if self.display_info.supports_truecolor {
            output.push_str("\x1b[38;2;255;100;50m🚀 Agent Selection\x1b[0m\n\n");
        } else {
            output.push_str("🚀 Agent Selection\n\n");
        }

        for (i, (id, name, category)) in agents.iter().enumerate() {
            let color_code = if self.display_info.supports_truecolor {
                match i % 4 {
                    0 => "\x1b[38;2;100;200;255m", // Blue
                    1 => "\x1b[38;2;100;255;100m", // Green  
                    2 => "\x1b[38;2;255;200;100m", // Orange
                    _ => "\x1b[38;2;255;100;200m", // Pink
                }
            } else {
                "\x1b[36m" // Cyan fallback
            };

            output.push_str(&format!(
                "{}[{}] {:<25} │ {:<35} │ {}\x1b[0m\n",
                color_code,
                i + 1,
                id,
                name,
                category
            ));
        }

        output.push_str("\nEnter number or type agent name: ");
        output
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wave_config_default() {
        let config = WaveConfig::default();
        assert!(config.enable_tab_management);
        assert!(config.enable_pane_splitting);
    }

    #[tokio::test]
    async fn test_wave_integration_creation() {
        let integration = WaveIntegration::new(None);
        assert!(integration.config.enable_tab_management);
    }

    #[test]
    fn test_wave_ui_creation() {
        let ui = WaveUI::new();
        assert!(ui.display_info.width > 0);
        assert!(ui.display_info.height > 0);
    }
}