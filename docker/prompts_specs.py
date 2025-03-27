from banks.registries import directory
from typing import Dict, Any
from pathlib import Path

path = Path("./prompts")
registry = directory.DirectoryPromptRegistry(path, force_reindex=True)

action2prompt = {"Create Issue": "issue", "Create Pull Request": "pr", "Create Comment under Issue": "comment_issue", "Create Comment under Pull Request": "comment_pr"}

def choose_prompt(action: str, arguments: Dict[str, Any]):
    actual_action = action2prompt[action]
    print(actual_action)
    prompt = registry.get(name=actual_action)
    actual_prompt = prompt.text(arguments)
    print(actual_prompt)
    return actual_prompt
