# bios_loader.py
import importlib.util
import sys
from pathlib import Path
from time import sleep
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from typing import Dict

class Loader:
    def __init__(self):
        self.console = Console()
        self.modules: Dict[str, dict] = {}
        self.status_table = Table.grid(padding=(0, 2))
        self.status_table.add_column("Module", width=30)
        self.status_table.add_column("Status", width=10)
        self.status_table.add_column("Message", width=40)

    def _module_status(self, name: str, success: bool, message: str = ""):
        status = Text("[OKAY]", style="bold green") if success else Text("[FAIL]", style="bold red")
        self.status_table.add_row(
            Text(name, style="cyan"),
            status,
            Text(message, style="yellow" if success else "red")
        )

    def _load_module(self, path: Path):
        module_name = path.stem
        try:
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None:
                self._module_status(module_name, False, "Invalid module spec")
                return

            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)  # type: ignore

            # Check for required attributes
            required = ['NAME', 'DESCRIPTION', 'calculate', 'get_requirements']
            missing = [attr for attr in required if not hasattr(mod, attr)]
            if missing:
                self._module_status(module_name, False, f"Missing: {', '.join(missing)}")
                return

            self.modules[module_name] = {
                'name': mod.NAME,
                'description': mod.DESCRIPTION,
                'module': mod
            }
            self._module_status(module_name, True, "Loaded successfully")
            sleep(0.1)

        except Exception as e:
            self._module_status(module_name, False, str(e))

    def scan_directory(self, directory: str):
        dir_path = Path(directory)
        if not dir_path.exists():
            self._module_status(directory, False, "Directory not found")
            return

        with Live(self.status_table, refresh_per_second=20, transient=True):
            for path in dir_path.glob("**/*.py"):
                if path.name == "__init__.py":
                    continue
                self._load_module(path)

    def show_summary(self):
        table = Table(title="Loaded Modules Summary", show_header=True, header_style="bold magenta")
        table.add_column("Module", style="cyan")
        table.add_column("Version" if hasattr(sys, 'version') else "Status", style="yellow")
        table.add_column("Description")

        for name, data in self.modules.items():
            table.add_row(
                Text(data['name'], style="bold green"),
                Text("v1.0", style="dim"),  # Could get real version from modules
                Text(data['description'])
            )

        self.console.print(table)