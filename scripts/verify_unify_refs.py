import re
import os

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

# Patterns to find potential misses
miss_patterns = [
    re.compile(r"(?i)fig(?:ure)?\.?\s*\\ref"),
    re.compile(r"(?i)tab(?:le)?\.?\s*\\ref"),
    re.compile(r"图\\ref"),
    re.compile(r"表\\ref"),
    re.compile(r"\\ref\{fig:[^}]+\}(?!~)"),
    re.compile(r"\\ref\{tab:[^}]+\}(?!~)")
]

# Correct patterns to double check
correct_fig = re.compile(r"图~\\ref\{fig:[^}]+\}~")
correct_tab = re.compile(r"表~\\ref\{tab:[^}]+\}~")

for file_name in files:
    full_path = os.path.join(base_dir, file_name)
    if not os.path.exists(full_path):
        continue
    
    print(f"Verifying {file_name}...")
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for potential misses
    for i, pattern in enumerate(miss_patterns):
        matches = pattern.findall(content)
        if matches:
            print(f"  [MISS/INCONSISTENT] Pattern {i} found: {matches}")
    
    # Optional: check if anything remains that looks like Fig/Tab ref but isn't prefixed correctly
    all_refs = re.findall(r"\\ref\{[^}]+\}", content)
    for ref in all_refs:
        # Simple check: search for the ref in content and look at context
        # This is more for manual assurance in output
        pass

print("Verification script finished.")
