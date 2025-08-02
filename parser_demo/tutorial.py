#!/usr/bin/env python3
"""
Demo Parser CLI Tutorial Navigator
Simple tool to browse documentation and explore project structure
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree
from rich import print as rprint

# Rich console
console = Console()

ALLOWED_EXTENSIONS = {'.py', '.html', '.md', '.json', '.sqlite3', '.db'}

def is_allowed_file(path: Path) -> bool:
    return path.suffix in ALLOWED_EXTENSIONS


class TreeBuilder:
    """Helper class to build hierarchical tree structure"""
    
    def __init__(self, root_label: str):
        self.tree = Tree(root_label)
    
    def add_file(self, rel_path: Path, icon: str):
        """Add file to tree with proper hierarchy"""
        parts = rel_path.parts
        
        if len(parts) == 1:
            # File in root directory
            self.tree.add(f"{icon} {parts[0]}")
        else:
            # File in subdirectory
            current_node = self.tree
            
            # Create or find directory nodes
            for i, part in enumerate(parts[:-1]):
                # Find existing directory node
                existing_node = None
                for child in current_node.children:
                    if child.label == f"📁 {part}":
                        existing_node = child
                        break
                
                if existing_node is None:
                    # Create new directory node
                    existing_node = current_node.add(f"📁 {part}")
                
                current_node = existing_node
            
            # Add file to the deepest directory
            current_node.add(f"{icon} {parts[-1]}")
    
    def get_tree(self) -> Tree:
        """Get the built tree"""
        return self.tree


class DemoTutorialNavigator:
    """Simple CLI navigator for Demo Parser documentation and structure"""

    def __init__(self):
        self.base_path = Path(__file__).parent
        self.docs_path = self.base_path / "@docs"
        self.module_path = self.base_path / "module"
        
    def get_docs_files(self) -> List[Path]:
        """Get all markdown files from @docs directory"""
        if not self.docs_path.exists():
            return []
        
        md_files = list(self.docs_path.glob("*.md"))
        return sorted(md_files, key=lambda x: x.name)
    
    def read_markdown_file(self, file_path: Path) -> str:
        """Read markdown file content"""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading file: {e}"
    
    def get_project_tree(self) -> Tree:
        """Generate project structure tree (filtered)"""
        tree_builder = TreeBuilder("📁 parser_demo")

        # Module structure
        if self.module_path.exists():
            for item in sorted(self.module_path.rglob("*")):
                if (
                    item.is_file()
                    and is_allowed_file(item)
                    and "__pycache__" not in item.parts
                ):
                    rel_path = item.relative_to(self.module_path)
                    if rel_path.parts[0] == "database":
                        tree_builder.add_file(rel_path, "🗄️")
                    elif "parser" in str(rel_path):
                        tree_builder.add_file(rel_path, "🔍")
                    elif "adapter" in str(rel_path):
                        tree_builder.add_file(rel_path, "🔗")
                    elif "config" in str(rel_path):
                        tree_builder.add_file(rel_path, "⚙️")
                    else:
                        tree_builder.add_file(rel_path, "📄")

        # Tests structure
        tests_path = self.base_path / "tests"
        if tests_path.exists():
            for item in sorted(tests_path.rglob("*.py")):
                if (
                    item.is_file()
                    and is_allowed_file(item)
                    and "__pycache__" not in item.parts
                ):
                    rel_path = item.relative_to(self.base_path)
                    tree_builder.add_file(rel_path, "🔬")

        # CLI files
        for cli_file in ["cli.py", "cli_db.py"]:
            cli_path = self.base_path / cli_file
            if cli_path.exists() and is_allowed_file(cli_path):
                tree_builder.add_file(Path(cli_file), "💻")

        # Documentation
        for md_file in self.get_docs_files():
            if is_allowed_file(md_file):
                tree_builder.add_file(Path("@docs") / md_file.name, "📄")

        # Samples
        samples_path = self.base_path / "samples"
        if samples_path.exists():
            for item in sorted(samples_path.rglob("*")):
                if (
                    item.is_file()
                    and is_allowed_file(item)
                    and "__pycache__" not in item.parts
                ):
                    rel_path = item.relative_to(self.base_path)
                    tree_builder.add_file(rel_path, "🌐")

        return tree_builder.get_tree()
    
    def show_markdown_file(self, file_path: Path):
        """Display markdown file with rich formatting"""
        content = self.read_markdown_file(file_path)
        
        console.clear()
        console.print(Panel(f"📄 {file_path.name}", style="bold blue"))
        console.print()
        
        # Display markdown content
        md = Markdown(content)
        console.print(md)
        
        console.print()
        console.print(Panel("Press Enter to continue...", style="dim"))
        input()
    
    def show_project_structure(self):
        """Display project structure tree"""
        console.clear()
        console.print(Panel("🌳 Demo Parser Project Structure", style="bold green"))
        console.print()
        
        tree = self.get_project_tree()
        console.print(tree)
        
        console.print()
        console.print(Panel("Press Enter to continue...", style="dim"))
        input()
    
    def show_file_content(self, file_path: Path):
        """Display file content with syntax highlighting"""
        try:
            content = file_path.read_text(encoding='utf-8')
            syntax = Syntax(content, "python", theme="monokai")
            
            console.clear()
            console.print(Panel(f"📄 {file_path.name}", style="bold blue"))
            console.print()
            console.print(syntax)
            
        except Exception as e:
            console.print(f"Error reading file: {e}", style="red")
        
        console.print()
        console.print(Panel("Press Enter to continue...", style="dim"))
        input()
    
    def main_menu(self):
        """Main navigation menu"""
        while True:
            console.clear()
            console.print(Panel("🚀 Demo Parser Tutorial Navigator", style="bold cyan"))
            console.print()
            
            choices = [
                "📚 Browse Documentation",
                "🌳 Show Project Structure", 
                "🔍 Explore Module Files",
                "🧪 View Test Files",
                "💻 View CLI Files",
                "🌐 View Sample HTML",
                "❌ Exit"
            ]
            
            choice = questionary.select(
                "What would you like to explore?",
                choices=choices
            ).ask()
            
            if choice == "📚 Browse Documentation":
                self.browse_documentation()
            elif choice == "🌳 Show Project Structure":
                self.show_project_structure()
            elif choice == "🔍 Explore Module Files":
                self.explore_module_files()
            elif choice == "🧪 View Test Files":
                self.explore_test_files()
            elif choice == "💻 View CLI Files":
                self.explore_cli_files()
            elif choice == "🌐 View Sample HTML":
                self.explore_sample_files()
            elif choice == "❌ Exit":
                console.print("👋 Goodbye!", style="bold green")
                break
    
    def browse_documentation(self):
        """Browse documentation files"""
        md_files = self.get_docs_files()
        
        if not md_files:
            console.print("No documentation files found!", style="red")
            input("Press Enter to continue...")
            return
        
        choices = [f"📄 {f.name}" for f in md_files] + ["🔙 Back"]
        
        while True:
            choice = questionary.select(
                "Select documentation to view:",
                choices=choices
            ).ask()
            
            if choice == "🔙 Back":
                break
            
            # Extract filename from choice
            filename = choice.replace("📄 ", "")
            file_path = self.docs_path / filename
            
            if file_path.exists():
                self.show_markdown_file(file_path)
    
    def explore_module_files(self):
        """Explore module files"""
        if not self.module_path.exists():
            console.print("Module directory not found!", style="red")
            input("Press Enter to continue...")
            return
        
        # Get all Python files
        py_files = list(self.module_path.rglob("*.py"))
        py_files = [f for f in py_files if f.name != "__pycache__"]
        
        if not py_files:
            console.print("No Python files found in module!", style="red")
            input("Press Enter to continue...")
            return
        
        choices = [f"🐍 {f.relative_to(self.module_path)}" for f in sorted(py_files)] + ["🔙 Back"]
        
        while True:
            choice = questionary.select(
                "Select module file to view:",
                choices=choices
            ).ask()
            
            if choice == "🔙 Back":
                break
            
            # Extract filepath from choice
            filepath = choice.replace("🐍 ", "")
            file_path = self.module_path / filepath
            
            if file_path.exists():
                self.show_file_content(file_path)
    
    def explore_test_files(self):
        """Explore test files"""
        tests_path = self.base_path / "tests"
        
        if not tests_path.exists():
            console.print("Tests directory not found!", style="red")
            input("Press Enter to continue...")
            return
        
        # Get all test files
        test_files = list(tests_path.rglob("test_*.py"))
        
        if not test_files:
            console.print("No test files found!", style="red")
            input("Press Enter to continue...")
            return
        
        choices = [f"🧪 {f.relative_to(tests_path)}" for f in sorted(test_files)] + ["🔙 Back"]
        
        while True:
            choice = questionary.select(
                "Select test file to view:",
                choices=choices
            ).ask()
            
            if choice == "🔙 Back":
                break
            
            # Extract filepath from choice
            filepath = choice.replace("🧪 ", "")
            file_path = tests_path / filepath
            
            if file_path.exists():
                self.show_file_content(file_path)
    
    def explore_cli_files(self):
        """Explore CLI files"""
        cli_files = []
        for cli_file in ["cli.py", "cli_db.py"]:
            if (self.base_path / cli_file).exists():
                cli_files.append(self.base_path / cli_file)
        
        if not cli_files:
            console.print("No CLI files found!", style="red")
            input("Press Enter to continue...")
            return
        
        choices = [f"💻 {f.name}" for f in cli_files] + ["🔙 Back"]
        
        while True:
            choice = questionary.select(
                "Select CLI file to view:",
                choices=choices
            ).ask()
            
            if choice == "🔙 Back":
                break
            
            # Extract filename from choice
            filename = choice.replace("💻 ", "")
            file_path = self.base_path / filename
            
            if file_path.exists():
                self.show_file_content(file_path)
    
    def explore_sample_files(self):
        """Explore sample HTML files"""
        samples_path = self.base_path / "samples"
        
        if not samples_path.exists():
            console.print("Samples directory not found!", style="red")
            input("Press Enter to continue...")
            return
        
        # Get all HTML files
        html_files = list(samples_path.rglob("*.html"))
        
        if not html_files:
            console.print("No HTML sample files found!", style="red")
            input("Press Enter to continue...")
            return
        
        choices = [f"🌐 {f.relative_to(samples_path)}" for f in sorted(html_files)] + ["🔙 Back"]
        
        while True:
            choice = questionary.select(
                "Select HTML sample to view:",
                choices=choices
            ).ask()
            
            if choice == "🔙 Back":
                break
            
            # Extract filepath from choice
            filepath = choice.replace("🌐 ", "")
            file_path = samples_path / filepath
            
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    syntax = Syntax(content, "html", theme="monokai")
                    
                    console.clear()
                    console.print(Panel(f"🌐 {file_path.name}", style="bold blue"))
                    console.print()
                    console.print(syntax)
                    
                except Exception as e:
                    console.print(f"Error reading file: {e}", style="red")
                
                console.print()
                console.print(Panel("Press Enter to continue...", style="dim"))
                input()


def main():
    """Main entry point"""
    try:
        navigator = DemoTutorialNavigator()
        navigator.main_menu()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="bold green")
    except Exception as e:
        console.print(f"Error: {e}", style="red")


if __name__ == "__main__":
    main() 