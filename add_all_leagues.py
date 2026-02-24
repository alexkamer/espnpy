import os
import re
from src.espnpy.constants import LEAGUE_TO_SPORT

def inject_client():
    with open("src/espnpy/client.py", "r") as f:
        content = f.read()

    start_marker = "    # We define the most popular leagues explicitly so IDE Autocomplete (VSCode, PyCharm) works flawlessly.\n"
    end_marker = "    def __getattr__(self, name: str) -> LeagueProxy:"

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    props = []
    # Sort them alphabetically for a clean file
    for league in sorted(LEAGUE_TO_SPORT.keys()):
        py_name = league.replace("-", "_").replace(".", "_")
        if py_name[0].isdigit():
            py_name = "league_" + py_name
        props.append(f'    @property\n    def {py_name}(self) -> "LeagueProxy": return LeagueProxy(self, "{league}")\n\n')

    new_content = content[:start_idx] + "".join(props) + content[end_idx:]
    with open("src/espnpy/client.py", "w") as f:
        f.write(new_content)

def inject_init():
    with open("src/espnpy/__init__.py", "r") as f:
        content = f.read()

    start_marker = "# Expose common leagues explicitly for IDE Auto-complete\n"
    end_marker = "def __getattr__(name: str) -> LeagueProxy:"

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    assignments = []
    exports = ['    "ESPNClient",\n']
    
    for league in sorted(LEAGUE_TO_SPORT.keys()):
        py_name = league.replace("-", "_").replace(".", "_")
        if py_name[0].isdigit():
            py_name = "league_" + py_name
        assignments.append(f'{py_name} = _default_client.{py_name}\n')
        exports.append(f'    "{py_name}",\n')

    exports_str = "__all__ = [\n" + "".join(exports) + "]\n"

    new_content = content[:start_idx] + "".join(assignments) + "\n" + content[end_idx:]
    
    # Replace __all__ block
    all_start = new_content.find("__all__ = [")
    if all_start != -1:
        new_content = new_content[:all_start] + exports_str

    with open("src/espnpy/__init__.py", "w") as f:
        f.write(new_content)

inject_client()
inject_init()
print("Successfully injected 384 explicit proxies into client.py and __init__.py!")
