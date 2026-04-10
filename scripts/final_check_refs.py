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

def check_context(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find ALL \ref{fig:...} or \ref{tab:...}
    all_refs = re.finditer(r"\\ref\{(fig|tab):[^}]+\}", content)
    
    issues = []
    for match in all_refs:
        start = match.start()
        end = match.end()
        
        # Check preceding context (approx 5 chars)
        pre = content[max(0, start-5):start]
        # Check succeeding context (approx 5 chars)
        post = content[end:min(len(content), end+5)]
        
        # Consistent format check: 图~\ref{...}~ or 表~\ref{...}~
        if match.group(1) == 'fig':
            if not (pre.endswith('图~') and post.startswith('~')):
                issues.append(f"  [ISSUE] Fig ref at {start}: ...{pre}[REF]{post}...")
        elif match.group(1) == 'tab':
            if not (pre.endswith('表~') and post.startswith('~')):
                issues.append(f"  [ISSUE] Tab ref at {start}: ...{pre}[REF]{post}...")
                
    return issues

for file_name in files:
    full_path = os.path.join(base_dir, file_name)
    if os.path.exists(full_path):
        print(f"Checking {file_name}...")
        issues = check_context(full_path)
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("  OK")
