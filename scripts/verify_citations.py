import re
import glob
import os

# Configuration
THESIS_DIR = r"c:/学习/研究生学习/毕设"
BODY_DIR = os.path.join(THESIS_DIR, "body")
BIB_FILE = os.path.join(THESIS_DIR, "ref/refs.bib")
OUTPUT_FILE = r"c:\学习\研究生学习\毕设\citation_verification_results.md"

def extract_citations_with_context(directory):
    citation_data = {} # key -> list of {file, line, context}
    tex_files = glob.glob(os.path.join(directory, "*.tex"))
    
    print(f"Scanning {len(tex_files)} tex files for context...")
    
    # Regex to find citation
    cite_iter_pattern = re.compile(r'\\cite\{([^}]+)\}')
    
    for file_path in tex_files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        content = "".join(lines)
        # Remove comments for matching purposes (simple approach)
        # But we want to keep line numbers, so we iterate lines or keep track of indices.
        # Simpler: Iterate matches in full content, calculate line number by counting newlines before match.
        
        for match in cite_iter_pattern.finditer(content):
            start, end = match.span()
            key_group = match.group(1)
            
            # Calculate line number
            line_num = content.count('\n', 0, start) + 1
            
            # Get context +/- 100 chars
            c_start = max(0, start - 100)
            c_end = min(len(content), end + 100)
            
            raw_context = content[c_start:c_end]
            context = re.sub(r'\s+', ' ', raw_context).strip()
            
            # Highlight match
            match_str = match.group(0)
            context = context.replace(match_str, f"**{match_str}**")
            
            keys = [k.strip() for k in key_group.split(',')]
            for key in keys:
                if key not in citation_data:
                    citation_data[key] = []
                
                # Check for duplicates in the same file/line approx?
                # Just add.
                citation_data[key].append({
                    'file': filename,
                    'line': line_num,
                    'context': context
                })
                        
    return citation_data

def parse_bib_file(bib_path):
    entries = {}
    if not os.path.exists(bib_path):
        print(f"Bib file not found: {bib_path}")
        return entries
        
    print(f"Parsing bib file: {bib_path}")
    
    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
            
    chunks = content.split('@')
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
            
        header_match = re.match(r'^(\w+)\s*\{\s*([^,]+),', chunk)
        if header_match:
            entry_type = header_match.group(1).lower()
            key = header_match.group(2).strip()
            
            title_match = re.search(r'title\s*=\s*\{([^}]+)\}', chunk, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1) if title_match else "No Title Found"
            
            year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', chunk, re.IGNORECASE)
            year = year_match.group(1) if year_match else "????"
            
            author_match = re.search(r'author\s*=\s*\{([^}]+)\}', chunk, re.IGNORECASE | re.DOTALL)
            author = author_match.group(1) if author_match else "Unknown"
            
            entries[key] = {
                'type': entry_type,
                'title': re.sub(r'\s+', ' ', title.strip()),
                'year': year,
                'author': re.sub(r'\s+', ' ', author.strip())
            }
            
    return entries

def main():
    citation_data = extract_citations_with_context(BODY_DIR)
    used_keys = sorted(citation_data.keys())
    
    bib_entries = parse_bib_file(BIB_FILE)
    
    print(f"Found {len(used_keys)} unique usage in text.")
    print(f"Found {len(bib_entries)} entries in bibliography.")
    
    # Generate Report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Citation Verification List\n\n")
        f.write("| 序号 | 引用 (Citation) | 引用位置 (Location) | 引用位置上下文 (Context) | 检查结果 (Result) | 备注 (Remark) |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        
        for idx, key in enumerate(used_keys, 1):
            # Format Bib Info
            if key in bib_entries:
                entry = bib_entries[key]
                # Limiting author length
                auth = entry['author']
                if len(auth) > 50: auth = auth[:50] + "..."
                bib_info = f"**{key}**<br>_{entry['title']}_<br>{auth} ({entry['year']})"
            else:
                bib_info = f"**{key}**<br>❌ [MISSING IN BIB]"
                
            # Format Locations and Contexts
            # Combine multiple occurrences
            occurrences = citation_data.get(key, [])
            
            locs_str_list = []
            contexts_str_list = []
            
            for i, occ in enumerate(occurrences):
                loc = f"{occ['file']}:{occ['line']}"
                locs_str_list.append(loc)
                
                # Limit contexts to first 3 to avoid huge table rows
                if i < 3:
                    # Escape pipes
                    ctx = occ['context'].replace("|", "\|").replace("\n", " ")
                    contexts_str_list.append(f"[{loc}] ...{ctx}...")
            
            locs_str = "<br>".join(locs_str_list)
            context_str = "<br><br>".join(contexts_str_list)
            if len(occurrences) > 3:
               context_str += f"<br>...(+{len(occurrences)-3} more)"
            
            f.write(f"| {idx} | {bib_info} | {locs_str} | {context_str} | | |\n")

    print(f"Report generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
