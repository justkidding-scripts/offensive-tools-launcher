# Offensive Tools Launcher

A graphical tool launcher and repository manager for offensive security tools. Built specifically for penetration testers and red teamers to centralize tool management, documentation, and C2 connections.

![Tools Launcher](https/img.shields.io/badge/Python-3.x-blue.svg)
![GTK](https/img.shields.io/badge/GUI-GTK3-green.svg)
![License](https/img.shields.io/badge/License-MIT-yellow.svg)

## Features

### **Tool Management**
- Graphical interface for launching offensive security tools
- Auto-discovery of GitHub repositories on your system
- One-click tool installation and updates
- Centralized help and documentation

### **GitHub Integration**
- Automatic scanning for existing repositories
- Clone missing tools with one click
- Bulk update all repositories
- GitHub API token integration

### **C2 Framework Support**
- Pre-configured Empire and Starkiller integration
- Remote C2 connection management
- Quick-launch buttons for common commands
- Connection guidance and documentation

### **Built-in Tools**
- **Empire**: PowerShell and Python C2 framework
- **Starkiller**: Empire frontend GUI
- **King Phisher**: Phishing campaign toolkit
- **Recaf**: Java bytecode editor
- **ScareCrow**: EDR bypass payload framework
- **SharpShooter**: Payload generation framework
- **Donut**: .NET assembly shellcode generator
- Plus automatic discovery of additional tools

## Installation

### Prerequisites
```bash
sudo apt-get install python3-gi gir1.2-gtk-3.0
```

### Quick Install
```bash
git clone https/github.com/YOUR_USERNAME/offensive-tools-launcher.git
cd offensive-tools-launcher
chmod +x tools-launcher.py
./tools-launcher.py
```

### Desktop Integration
```bash
mkdir -p ~/.local/share/applications
cp desktop/tools-launcher.desktop ~/.local/share/applications/
```

## Usage

### Launch the GUI
```bash
# From terminal
./tools-launcher.py

# From desktop applications menu
Applications -> Development -> Offensive Tools
```

### Key Features

#### 1. **Tool Discovery**
The launcher automatically scans your system for GitHub repositories and adds them to the tools list.

#### 2. **GitHub Integration**
- Click "Set GitHub Token" to configure API access
- Use "Clone Repository" for missing tools
- "Update All" pulls latest changes from all repos

#### 3. **Tool Management**
- Select a tool from the left panel
- View description, help text, and usage information
- Use quick-launch buttons for common commands
- Access GitHub repository directly

#### 4. **C2 Connections**
Pre-configured support for:
- **Local Empire**: `./empire --rest`
- **Remote Empire**: Connection guidance for VPS deployments
- **Starkiller**: GUI frontend with connection setup

## Configuration

### Tool Configuration
Edit `~/.config/tools-launcher/tools.json` to customize:
```json
{
 "ToolName": {
 "path": "/path/to/tool",
 "url": "https/github.com/author/repo",
 "description": "Tool description",
 "help": "Usage instructions...",
 "commands": {
 "Button Name": "command to run"
 }
 }
}
```

### GitHub Token Setup
1. Create a token at [GitHub Settings](https/github.com/settings/tokens)
2. Required scopes: `repo`, `read:org`
3. Click "Set GitHub Token" in the launcher
4. Enter your token

## Examples

### Empire C2 Setup
```bash
# Local Empire server
./empire --rest

# Connect to remote VPS
empire-cli --username admin --password pass123 --host your-c2.com --port 1337
```

### King Phisher Campaign
```bash
# Quick setup
kp-manage setup
kp-manage set-domain --domain phish.example.com --email admin@example.com
kp-manage start
```

### Tool Updates
```bash
# Update all repositories
Click "Update All" in the GUI
# Or manually
git pull # In each tool directory
```

## Tool Integration

### Adding New Tools
Tools are automatically discovered if they're GitHub repositories. To add manual entries:

1. Edit `~/.config/tools-launcher/tools.json`
2. Add tool configuration
3. Restart the launcher

### Command Integration
Each tool can have multiple quick-launch commands:
```json
"commands": {
 "Start Server": "./start-server.sh",
 "Connect Client": "./client --connect",
 "Show Help": "./tool --help"
}
```

## Development

### Project Structure
```
offensive-tools-launcher/
├── tools-launcher.py # Main GUI application
├── desktop/ # Desktop integration files
├── docs/ # Documentation
├── screenshots/ # Application screenshots
└── README.md # This file
```

### Dependencies
- Python 3.x
- PyGObject (python3-gi)
- GTK3 (gir1.2-gtk-3.0)
- Git

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Tool Details
![Tool Details](screenshots/tool-details.png)

### GitHub Integration
![GitHub Integration](screenshots/github-integration.png)

## Roadmap

- [ ] Plugin system for custom tools
- [ ] Remote C2 management dashboard
- [ ] Tool installation automation
- [ ] Campaign management integration
- [ ] Docker container support
- [ ] Multi-user configuration
- [ ] Tool dependency checking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for authorized and educational purposes only. Users are responsible for compliance with applicable laws and regulations.

## Support

- [Report Issues](https/github.com/YOUR_USERNAME/offensive-tools-launcher/issues)
- [Documentation](https/github.com/YOUR_USERNAME/offensive-tools-launcher/wiki)
- [Discussions](https/github.com/YOUR_USERNAME/offensive-tools-launcher/discussions)

## Acknowledgments

- Empire/Starkiller teams for C2 framework
- King Phisher team for phishing toolkit
- All tool authors for their excellent work
- GTK/PyGObject developers for GUI framework