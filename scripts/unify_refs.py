import re
import os

# Define the target files
base_dir = r"c:\学习\研究生学习\毕设\body"
files = [
    "chap01.tex",
    "chap02.tex",
    "chap03.tex",
    "chap04.tex",
    "chap05.tex",
    "chap06.tex",
    "cover.tex"
]

# Regex patterns
# Group 1: Figure labels (图, Fig., etc.)
# Group 2: \ref{...}
figure_regex = re.compile(r"(图|Fig\.|Figure|Fig)(?:\.|\b)\s*~?\s*(\\ref\{[^}]+\})\s*~?\s*")
# Group 1: Table labels (表, Tab., etc.)
# Group 2: \ref{...}
table_regex = re.compile(r"(表|Tab\.|Table|Tab)(?:\.|\b)\s*~?\s*(\\ref\{[^}]+\})\s*~?\s*")

def unify_refs(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replacement logic
    new_content = figure_regex.sub(r"图~\2~", content)
    new_content = table_regex.sub(r"表~\2~", new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes needed for {file_path}")

for file_name in files:
    full_path = os.path.join(base_dir, file_name)
    if os.path.exists(full_path):
        unify_refs(full_path)
    else:
        print(f"File not found: {full_path}")
