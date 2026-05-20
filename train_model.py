"""Train the Markov chain model from the built-in corpus and resource files.

Run this once to generate models/markov_model.json.
After training, the model file is all you need — no GGUF, no llama-cpp.

Usage:
    python train_model.py
"""

import os
import re
import sys

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.markov_engine import MarkovTrainer
from resources.training_corpus import CORPUS
from resources.shell_corpus import SHELL_CORPUS
from resources.c_os_corpus import C_OS_CORPUS
from resources.new_data_corpus import NEW_DATA_SNIPPETS
from resources.lab_code_corpus import LAB_CODE_SNIPPETS


def extract_code_from_markdown(filepath: str) -> list[tuple[str, str]]:
    """Extract code blocks from a markdown file (Python, Bash, and C).

    Returns list of (description, code) tuples.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    results = []
    # Find headings followed by code blocks
    sections = re.split(r"^(#{1,3}\s+.+)$", content, flags=re.MULTILINE)

    current_heading = os.path.basename(filepath).replace(".md", "")
    for section in sections:
        if re.match(r"^#{1,3}\s+", section):
            current_heading = section.lstrip("# ").strip()
        else:
            # Match python, bash, sh, and c code blocks
            blocks = re.findall(r"```(?:python|bash|sh|c)\s*\n(.*?)```", section, re.DOTALL)
            for block in blocks:
                code = block.strip()
                if code:
                    results.append((current_heading, code))

    return results


def collect_resource_snippets(resource_dir: str) -> list[tuple[str, str]]:
    """Collect all Python code snippets from resource markdown files."""
    snippets = []
    for root, _dirs, files in os.walk(resource_dir):
        for fname in files:
            if fname.endswith(".md"):
                path = os.path.join(root, fname)
                snippets.extend(extract_code_from_markdown(path))
    return snippets


def main() -> None:
    project_root = os.path.dirname(os.path.abspath(__file__))
    resource_dir = os.path.join(project_root, "resources")
    model_path = os.path.join(project_root, "models", "markov_model.json")

    print("Training Markov model...")

    trainer = MarkovTrainer(n=3)

    # Feed the built-in corpus
    print(f"  Adding {len(CORPUS)} built-in Python snippets...")
    for snippet in CORPUS:
        code = snippet.strip()
        # Extract first comment as description
        desc = ""
        for line in code.splitlines():
            if line.strip().startswith("#"):
                desc = line.strip().lstrip("# ").strip()
                break
        trainer.add_snippet(code, desc)

    # Feed the shell scripting corpus
    print(f"  Adding {len(SHELL_CORPUS)} shell/bash snippets...")
    for snippet in SHELL_CORPUS:
        code = snippet.strip()
        desc = ""
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("#!"):
                desc = stripped.lstrip("# ").strip()
                break
        trainer.add_snippet(code, desc)

    # Feed the C OS concepts corpus
    print(f"  Adding {len(C_OS_CORPUS)} C/OS snippets...")
    for snippet in C_OS_CORPUS:
        code = snippet.strip()
        desc = ""
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("//"):
                desc = stripped.lstrip("/ ").strip()
                break
        trainer.add_snippet(code, desc)

    # Feed code from resource markdown files
    resource_snippets = collect_resource_snippets(resource_dir)
    print(f"  Adding {len(resource_snippets)} resource snippets...")
    for description, code in resource_snippets:
        trainer.add_snippet(code, description)

    # Feed new OS lab exam data (from new_data/ guides)
    print(f"  Adding {len(NEW_DATA_SNIPPETS)} new OS lab snippets...")
    for code, description in NEW_DATA_SNIPPETS:
        trainer.add_snippet(code.strip(), description)

    # Feed markdown snippets from the new_data/ directory
    new_data_dir = os.path.join(project_root, "new_data")
    if os.path.isdir(new_data_dir):
        md_snippets = collect_resource_snippets(new_data_dir)
        print(f"  Adding {len(md_snippets)} snippets extracted from new_data/*.md...")
        for description, code in md_snippets:
            trainer.add_snippet(code, description)

    # Feed actual lab source code files (lab1-lab9)
    print(f"  Adding {len(LAB_CODE_SNIPPETS)} actual lab code snippets...")
    for code, description in LAB_CODE_SNIPPETS:
        trainer.add_snippet(code.strip(), description)

    # Also ingest .c files from OS lab directory if available
    os_lab_dir = os.path.join(os.path.expanduser('~'), '0_SYSTEM', '00_Inbox_M1', 'OS lab')
    if os.path.isdir(os_lab_dir):
        md_from_oslab = collect_resource_snippets(os_lab_dir)
        print(f"  Adding {len(md_from_oslab)} snippets from OS lab markdown guides...")
        for description, code in md_from_oslab:
            trainer.add_snippet(code, description)

    # Build and save
    model = trainer.build()
    model.save(model_path)

    file_size = os.path.getsize(model_path)
    n_snippets = len(model.snippets)

    print(f"\nModel saved to: {model_path}")
    print(f"  Size: {file_size / 1024:.1f} KB")
    print(f"  Snippets: {n_snippets}")
    print("\nDone! You can now run the assistant.")


if __name__ == "__main__":
    main()
