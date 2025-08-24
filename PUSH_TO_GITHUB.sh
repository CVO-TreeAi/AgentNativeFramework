#!/bin/bash

# 🚀 Push AgentNativeFramework to GitHub
# Complete terminal agent system ready for deployment

echo "🤖 Pushing Agent Native Framework to GitHub..."
echo "Repository: https://github.com/CVO-TreeAi/AgentNativeFramework.git"
echo ""

# Check current status
echo "📊 Current Repository Status:"
git log --oneline -5
echo ""
git status --short
echo ""

# Authenticate with GitHub (choose one method)
echo "🔐 Choose authentication method:"
echo "1. GitHub CLI (recommended):"
echo "   gh auth login"
echo ""
echo "2. Personal Access Token:"
echo "   Get token from: https://github.com/settings/tokens"
echo "   git remote set-url origin https://[token]@github.com/CVO-TreeAi/AgentNativeFramework.git"
echo ""
echo "3. SSH (if configured):"
echo "   git remote set-url origin git@github.com:CVO-TreeAi/AgentNativeFramework.git"
echo ""

read -p "Press Enter after authenticating to continue pushing..."

# Push everything to GitHub
echo ""
echo "🚀 Pushing main branch..."
if git push origin main; then
    echo "✅ Main branch pushed successfully!"
else
    echo "❌ Failed to push main branch. Check authentication."
    exit 1
fi

echo ""
echo "🌿 Pushing feature branch..."
if git push origin feature/terminal-agent-system; then
    echo "✅ Feature branch pushed successfully!"
else
    echo "❌ Failed to push feature branch."
fi

echo ""
echo "🏷️  Pushing version tags..."
if git push origin --tags; then
    echo "✅ Tags pushed successfully!"
    echo "   - v1.0.0-alpha (Terminal system transformation)"
    echo "   - v1.0.0-beta (Production-ready release)"
else
    echo "❌ Failed to push tags."
fi

echo ""
echo "🎉 AgentNativeFramework successfully pushed to GitHub!"
echo ""
echo "📋 What's now live on GitHub:"
echo "✅ 21 files including complete Rust implementation"
echo "✅ Professional README with installation instructions"
echo "✅ One-line installer: curl -sSL https://raw.githubusercontent.com/CVO-TreeAi/AgentNativeFramework/main/install.sh | bash"
echo "✅ Complete documentation and examples"
echo "✅ Version tags for release management"
echo "✅ Feature branch for development"
echo ""
echo "🔗 Repository URL: https://github.com/CVO-TreeAi/AgentNativeFramework"
echo ""
echo "🚀 Next Steps:"
echo "1. Visit the repository on GitHub"
echo "2. Create a release from v1.0.0-beta tag"
echo "3. Set up GitHub Actions for CI/CD"
echo "4. Share with the community!"