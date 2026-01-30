
import os
import shutil
import re
import glob

# Configuration
TEX_DIR = r"c:\学习\研究生学习\毕设\body"
BIB_FILE = r"c:\学习\研究生学习\毕设\ref\refs.bib"
BACKUP_DIR = r"c:\学习\研究生学习\毕设\backup_before_fix"

# Fix Data
KEY_REPLACEMENTS = {
    'zhang2025safety': 'liu2024safety',
    'inan2024safety': 'asgari2025framework',
    'thapa2024large': 'liu2024benchhealth',
    'liu2024comprehensive': 'ura2024open',
    'kweon2024publicly': 'kweon2023asclepius',
    'katt2023search': 'zakka2024search',
    'chen2024benchmarking': 'chen2023meditron',
    # Note: wang2023comprehensive, nazi2024large, etc. kept same key, just bib update
}

BIB_UPDATES = {
    'nazi2024large': {
        'journal': 'Big Data and Cognitive Computing',
        'title': 'Large language models in healthcare and medical domain: A review',
        'author': 'Nazi, Zain Abdin and others', # Simplify for replace, usually author field is complex
    },
    'ji2023survey': {
        'author': 'Huang, Lei and Yu, Weijiang and Ma, Weitao and others',
        'title': 'A Survey on Hallucination in Large Language Models: Principles, Taxonomy, and Detection'
    },
    'ganguli2022red': {
        'author': 'Ganguli, Deep and Lovitt, Liane and Kernion, Jackson and others'
    },
    'guan2024deliberative': {
        'author': 'Guan, Melody Y. and others'
    },
    'qi2023safe': {
        'author': 'Dai, Josef and Pan, Xuehai and Sun, Ruiyang and others'
    },
    'singhal2025nature': {
        'journal': 'NEJM AI',
        'year': '2024',
        'doi': '10.1056/AIoa2300031',
        'title': 'Toward Expert-Level Medical Question Answering with Large Language Models'
    },
    'wang2023comprehensive': {
        'author': 'Wang, Xuan and others',
        'title': 'A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare',
        'year': '2025'
    },
    'zeng2023meddialog': {
        'year': '2020'
    }
}

NEW_ENTRIES = {
    'liu2024safety': """@article{liu2024safety,
  title={A Comprehensive Survey on Safety Evaluation of Large Language Models},
  author={Liu, Yepeng and Li, Yuheng and Bu, Yuheng and others},
  journal={arXiv preprint arXiv:2402.18663},
  year={2024}
}""",
    'asgari2025framework': """@article{asgari2025framework,
  title={A Framework to Assess Clinical Safety and Hallucination Rates of LLMs for Medical Text Summarisation},
  author={Asgari, Elham and and others},
  journal={arXiv preprint arXiv:2402.14088},
  year={2025}
}""",
    'liu2024benchhealth': """@article{liu2024benchhealth,
  title={BenchHealth: Large Language Models in Healthcare: A Comprehensive Benchmark},
  author={Liu, Fenglin and others},
  journal={arXiv preprint arXiv:2406.18579},
  year={2024}
}""",
    'ura2024open': """@article{ura2024open,
  title={The Open Medical-LLM Leaderboard: Benchmarking Large Language Models in Healthcare},
  author={Ura, Aaditya and others},
  journal={arXiv preprint arXiv:2405.10098},
  year={2024}
}""",
    'kweon2023asclepius': """@article{kweon2023asclepius,
  title={Asclepius: The Era of Existing Medical LLMs for Clinical Notes},
  author={Kweon, Sunjun and others},
  journal={arXiv preprint arXiv:2312.15883},
  year={2023}
}""",
    'zakka2024search': """@article{zakka2024search,
  title={SearchRAG: Can Search Engines Be Helpful for LLM-based Medical Question Answering?},
  author={Zakka, Cyril and others},
  journal={arXiv preprint arXiv:2402.13867},
  year={2024}
}""",
    'chen2023meditron': """@article{chen2023meditron,
  title={MEDITRON-70B: Scaling Medical Pretraining with Large Language Models},
  author={Chen, Zeming and others},
  journal={arXiv preprint arXiv:2311.16079},
  year={2023}
}"""
}

def backup_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Backup tex files
    for tex_file in glob.glob(os.path.join(TEX_DIR, '*.tex')):
        shutil.copy(tex_file, BACKUP_DIR)
    
    # Backup bib file
    if os.path.exists(BIB_FILE):
        shutil.copy(BIB_FILE, BACKUP_DIR)
    print(f"Backed up files to {BACKUP_DIR}")

def update_bib_file():
    if not os.path.exists(BIB_FILE):
        print(f"Error: {BIB_FILE} not found")
        return

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Existing Entries (Regex substitution)
    for key, updates in BIB_UPDATES.items():
        # Find entry start
        entry_pattern = re.compile(r'@\w+\s*{\s*' + re.escape(key) + r',', re.IGNORECASE)
        match = entry_pattern.search(content) 
        if match:
            # We found the entry, now simple approach: replace specific fields if precise, 
            # OR brute force replace fields within the block.
            # Given bibtex variability, let's use a safer "replace field line" approach if possible.
            # Or just warn manually? No, we need to fix it.
            # Strategy: find `field = {old_val}` inside lines until next @ or end.
            start_idx = match.start()
            # Find next @ or EOF
            next_at = content.find('@', start_idx + 1)
            end_idx = next_at if next_at != -1 else len(content)
            entry_block = content[start_idx:end_idx]
            
            new_entry_block = entry_block
            for field, new_value in updates.items():
                # Regex to replace field line: `field \s*=\s*{.*?}` or `field \s*=\s*".*?"`
                # Be careful with multi-line content.
                field_regex = re.compile(r'(\s*' + field + r'\s*=\s*)([\{"])(.*?)([\}"])(,?\s*\n)', re.IGNORECASE | re.DOTALL)
                
                # Check if field exists
                if field_regex.search(new_entry_block):
                   # We only want to replace the FIRST occurrence in this block
                   # But regex on block is tricky if multiple matches (shouldn't be for same field).
                   # To be safe, we reconstruct the line?
                   # Let's use sub but strict about matching only this field
                   new_entry_block = field_regex.sub(r'\1{\3}\5'.replace(r'{\3}', r'{' + new_value + r'}'), new_entry_block, count=1)
                   print(f"Updated {key}: {field} -> {new_value}")
                else:
                    # Field doesn't exist, insert it before insertion point (last closing brace?)
                    # Getting complex. Let's append to end of entry before closing brace '}'?
                    # This is risky. 
                    # Alternative: Print warning to manual fix or just append fields?
                    # Let's assume most fields exist. If Year is missing, we might fail.
                    print(f"Warning: Field {field} not found in {key}, skipping update (manual check needed).")

            content = content[:start_idx] + new_entry_block + content[end_idx:]
        else:
            print(f"Warning: Entry {key} not found in bib, cannot update metadata.")

    # 2. Add New Entries
    # Check if key already exists to avoid duplicates
    existing_keys = set()
    for m in re.finditer(r'@\w+\s*{\s*([^,]+),', content):
        existing_keys.add(m.group(1).strip())

    for key, entry_str in NEW_ENTRIES.items():
        if key not in existing_keys:
            content += "\n\n" + entry_str
            print(f"Added new entry: {key}")
        else:
            print(f"Entry {key} already exists, skipping add.")

    with open(BIB_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Bib file updated.")

def update_tex_files():
    tex_files = glob.glob(os.path.join(TEX_DIR, '*.tex'))
    for tex_file in tex_files:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        for old_key, new_key in KEY_REPLACEMENTS.items():
            if old_key in content:
                # Replace strict word boundary? tex keys usually delimited by comma or brace
                # e.g. \cite{old_key} or \cite{a, old_key, b}
                # Regex: (?<=[{,])\s*old_key\s*(?=[,}])
                # simplified: replace string literal if it's likely a key usage
                if content.replace(old_key, new_key) != content:
                     content = content.replace(old_key, new_key)
                     modified = True
                     print(f"Replaced {old_key} -> {new_key} in {os.path.basename(tex_file)}")
        
        if modified:
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    backup_files()
    update_bib_file()
    update_tex_files()
    print("Citation fixes applied.")
