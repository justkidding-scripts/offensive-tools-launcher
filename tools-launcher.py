#!/usr/bin/env python3
import gi
import os
import json
import glob
import subprocess
import webbrowser
import requests
from pathlib import Path
from urllib.parse import urlparse

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

TOOLS_DIR = os.path.expanduser("~/tools")
CONFIG_DIR = os.path.expanduser("~/.config/tools-launcher")
TOOLS_CONFIG = os.path.join(CONFIG_DIR, "tools.json")
GITHUB_TOKEN_FILE = os.path.join(CONFIG_DIR, "github_token")

DEFAULT_TOOLS = {
    "Empire": {
        "path": "/home/kali/Empire/empire/Empire",
        "url": "https://github.com/BC-SECURITY/Empire",
        "description": "PowerShell and Python post-exploitation framework",
        "help": """Usage: 
        1. Start server: ./empire --rest
        2. Connect client: ./empire-cli
        3. Connect Starkiller: http://localhost:1337
        
        Remote C2:
        empire-cli --username admin --password pass123 --host empire.c2 --port 1337
        
        Starkiller connection:
        URL: https://empire.c2:1337
        """,
        "commands": {
            "Start Server": "./empire --rest",
            "Start Client": "./empire-cli",
            "Connect Remote": "empire-cli --config"
        }
    },
    "Starkiller": {
        "path": "/home/kali/tools/Starkiller",
        "url": "https://github.com/BC-SECURITY/Starkiller",
        "description": "Frontend for Empire C2 Framework",
        "help": """Usage:
        1. Start Starkiller: starkiller
        2. Connect to Empire server:
           - Local: http://localhost:1337
           - Remote: https://empire.c2:1337
        """,
        "commands": {
            "Launch GUI": "starkiller",
            "Config Remote": "starkiller --config"
        }
    },
    "King Phisher": {
        "path": "/home/kali/tools/king-phisher",
        "url": "https://github.com/rsmusllp/king-phisher",
        "description": "Phishing Campaign Toolkit",
        "help": """Usage:
        kp-manage [command] [options]
        
        Commands:
        setup         Initial setup
        start        Start services
        stop         Stop services
        set-domain   Configure domain
        """,
        "commands": {
            "Setup": "kp-manage setup",
            "Start": "kp-manage start",
            "Status": "kp-manage status",
            "Stop": "kp-manage stop"
        }
    }
}

def find_git_repos(start_path):
    """Find all git repositories in path"""
    repos = []
    for git_dir in glob.glob(f"{start_path}/**/.git", recursive=True):
        repo_dir = os.path.dirname(git_dir)
        try:
            remote_url = subprocess.check_output(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=repo_dir
            ).decode().strip()
            if 'github.com' in remote_url:
                repos.append({
                    'path': repo_dir,
                    'url': remote_url.replace('.git', '').replace('git@github.com:', 'https://github.com/')
                })
        except:
            continue
    return repos

class ToolLauncherWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Offensive Tools Launcher")
        self.set_border_width(10)
        self.set_default_size(900, 600)
        
        # Load or create config
        os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(TOOLS_CONFIG):
            with open(TOOLS_CONFIG) as f:
                self.tools = json.load(f)
        else:
            self.tools = DEFAULT_TOOLS
            with open(TOOLS_CONFIG, 'w') as f:
                json.dump(self.tools, f, indent=2)
        
        # Scan for additional repos
        for repo in find_git_repos(os.path.expanduser("~")):
            name = os.path.basename(repo['path'])
            if name not in self.tools:
                self.tools[name] = {
                    'path': repo['path'],
                    'url': repo['url'],
                    'description': 'Found GitHub repository',
                    'help': 'Repository found during scan.\nEdit config to add usage details.',
                    'commands': {}
                }
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        main_box.pack_start(toolbar, False, True, 0)
        
        self.gh_token_btn = Gtk.Button(label="Set GitHub Token")
        self.gh_token_btn.connect("clicked", self.on_token_clicked)
        toolbar.pack_start(self.gh_token_btn, False, False, 0)
        
        self.update_btn = Gtk.Button(label="Update All")
        self.update_btn.connect("clicked", self.on_update_clicked)
        toolbar.pack_start(self.update_btn, False, False, 0)
        
        # Split view
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(paned, True, True, 0)
        
        # Tools list (left)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.tools_list = Gtk.ListBox()
        self.tools_list.connect('row-selected', self.on_tool_selected)
        scrolled.add(self.tools_list)
        
        # Populate tools
        for name in sorted(self.tools.keys()):
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(label=name, xalign=0))
            self.tools_list.add(row)
        
        paned.pack1(scrolled, False, False)
        
        # Details view (right)
        self.details = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Tool info
        self.name_label = Gtk.Label()
        self.name_label.set_markup("<big><b>Select a tool</b></big>")
        self.details.pack_start(self.name_label, False, False, 0)
        
        self.desc_label = Gtk.Label()
        self.desc_label.set_line_wrap(True)
        self.desc_label.set_xalign(0)
        self.details.pack_start(self.desc_label, False, False, 0)
        
        # Help text
        help_frame = Gtk.Frame(label="Help")
        self.help_view = Gtk.TextView()
        self.help_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.help_view.set_editable(False)
        help_scroll = Gtk.ScrolledWindow()
        help_scroll.add(self.help_view)
        help_frame.add(help_scroll)
        self.details.pack_start(help_frame, True, True, 0)
        
        # Buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.details.pack_start(self.button_box, False, False, 0)
        
        # Action buttons
        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.button_box.pack_start(actions, False, False, 0)
        
        self.github_btn = Gtk.Button(label="Open GitHub")
        self.github_btn.connect("clicked", self.on_github_clicked)
        actions.pack_start(self.github_btn, False, False, 0)
        
        self.clone_btn = Gtk.Button(label="Clone Repository")
        self.clone_btn.connect("clicked", self.on_clone_clicked)
        actions.pack_start(self.clone_btn, False, False, 0)
        
        # Command buttons
        self.cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.button_box.pack_start(self.cmd_box, False, False, 0)
        
        paned.pack2(self.details, True, False)
    
    def on_token_clicked(self, button):
        dialog = Gtk.Dialog(
            "GitHub Token", self, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )
        
        box = dialog.get_content_area()
        
        label = Gtk.Label(label="Enter GitHub Token:")
        box.add(label)
        
        entry = Gtk.Entry()
        if os.path.exists(GITHUB_TOKEN_FILE):
            with open(GITHUB_TOKEN_FILE) as f:
                entry.set_text(f.read().strip())
        box.add(entry)
        
        box.show_all()
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            token = entry.get_text().strip()
            with open(GITHUB_TOKEN_FILE, 'w') as f:
                f.write(token)
            os.chmod(GITHUB_TOKEN_FILE, 0o600)
        
        dialog.destroy()
    
    def on_update_clicked(self, button):
        for name, tool in self.tools.items():
            if os.path.exists(os.path.join(tool['path'], '.git')):
                try:
                    subprocess.run(['git', 'pull'], cwd=tool['path'], check=True)
                except subprocess.CalledProcessError as e:
                    dialog = Gtk.MessageDialog(
                        transient_for=self,
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text=f"Failed to update {name}"
                    )
                    dialog.format_secondary_text(str(e))
                    dialog.run()
                    dialog.destroy()
    
    def on_tool_selected(self, list_box, row):
        if not row:
            return
        
        name = row.get_children()[0].get_text()
        tool = self.tools[name]
        
        self.name_label.set_markup(f"<big><b>{name}</b></big>")
        self.desc_label.set_text(tool['description'])
        
        self.help_view.get_buffer().set_text(tool['help'])
        
        for child in self.cmd_box.get_children():
            child.destroy()
        
        for label, cmd in tool.get('commands', {}).items():
            btn = Gtk.Button(label=label)
            btn.connect('clicked', self.on_command_clicked, cmd, tool['path'])
            self.cmd_box.pack_start(btn, False, False, 0)
        
        self.cmd_box.show_all()
        
        self.github_btn.set_sensitive('url' in tool)
        self.clone_btn.set_sensitive(
            'url' in tool and not os.path.exists(tool['path'])
        )
    
    def on_github_clicked(self, button):
        row = self.tools_list.get_selected_row()
        if row:
            name = row.get_children()[0].get_text()
            webbrowser.open(self.tools[name]['url'])
    
    def on_clone_clicked(self, button):
        row = self.tools_list.get_selected_row()
        if not row:
            return
        
        name = row.get_children()[0].get_text()
        tool = self.tools[name]
        
        try:
            subprocess.run(
                ['git', 'clone', tool['url'], tool['path']],
                check=True
            )
            self.clone_btn.set_sensitive(False)
        except subprocess.CalledProcessError as e:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Clone failed"
            )
            dialog.format_secondary_text(str(e))
            dialog.run()
            dialog.destroy()
    
    def on_command_clicked(self, button, cmd, cwd):
        try:
            env = os.environ.copy()
            env['PATH'] = f"{os.path.expanduser('~/.local/bin')}:{env['PATH']}"
            
            subprocess.Popen(
                cmd.split(),
                cwd=cwd,
                env=env,
                start_new_session=True
            )
        except Exception as e:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Command Error"
            )
            dialog.format_secondary_text(str(e))
            dialog.run()
            dialog.destroy()

def main():
    win = ToolLauncherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()