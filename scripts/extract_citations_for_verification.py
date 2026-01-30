import os
import re
import glob

def parse_bib_file(bib_path):
    """Parses the bib file to map keys to title and author."""
    bib_data = {}
    if not os.path.exists(bib_path):
        print(f"Bib file not found: {bib_path}")
        return bib_data

    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find entries: @type{key, ...}
    # This is a simple parser and might need adjustment for complex bib files
    entries = re.split(r'@\w+\{', content)
    
    # The first split is usually empty or comments before first entry
    # We need to capture the key which is immediately after @type{
    # Let's try a different approach: find all @type{key,
    
    # pattern = r'@\w+\s*\{\s*([^,]+),'
    # keys = re.findall(pattern, content)
    
    # We need to extract fields for each entry. 
    # Let's iterate line by line to be safer with large files.
    
    lines = content.split('\n')
    current_key = None
    current_entry = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('@'):
            # Start of new entry
            # Format @type{key,
            match = re.match(r'@\w+\s*\{\s*([^,]+),', line)
            if match:
                current_key = match.group(1).strip()
                bib_data[current_key] = {'title': 'Unknown', 'author': 'Unknown', 'year': 'Unknown', 'raw': line}
        elif current_key and '=' in line:
            # Field line
            parts = line.split('=', 1)
            field = parts[0].strip().lower()
            value = parts[1].strip().strip('{},"') # Remove braces, quotes, trailing comma
            if value.endswith(','):
                value = value[:-1].strip('{},"')
                
            if field in ['title', 'author', 'year']:
                bib_data[current_key][field] = value
                
    return bib_data

def extract_citations_from_tex(tex_dir):
    """Extracts citations from all tex files in the directory."""
    citations = []
    
    tex_files = glob.glob(os.path.join(tex_dir, '*.tex'))
    
    for tex_file in tex_files:
        filename = os.path.basename(tex_file)
        with open(tex_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            # Find all citations in the line
            # Pattern: \cite{...}, \citep{...}, \citet{...}
            # Handles multiple keys: \cite{key1, key2}
            matches = re.finditer(r'\\cite[a-z]*\{([^}]+)\}', line)
            
            for match in matches:
                keys_str = match.group(1)
                keys = [k.strip() for k in keys_str.split(',')]
                
                # Context
                start_context = max(0, i - 2)
                end_context = min(len(lines), i + 3)
                context_lines = lines[start_context:end_context]
                context = "".join(context_lines).strip()
                # Clean up context for markdown table (remove vertical bars or newlines)
                context = context.replace('\n', '<br>').replace('|', '\|')
                
                for key in keys:
                    citations.append({
                        'key': key,
                        'file': filename,
                        'line': i + 1,
                        'context': context
                    })
                    
    return citations

def generate_report(citations, bib_data, output_file):
    """Generates the markdown report."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Citation Verification Results\n\n")
        f.write("| 序号 | 引用 (Key - Title - Author) | 引用位置 | 引用位置上下文 | 检查结果 | 备注 |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        
        # Group by key to avoid duplicates if specific location listing isn't strictly per instance but grouped
        # User asked for "Citation, Location (Possible multiple), Context"
        # Since context differs for each location, it's better to list each occurrence?
        # "引用位置（可能有多处）" suggests grouping by Citation Key.
        
        grouped_citations = {}
        for item in citations:
            key = item['key']
            if key not in grouped_citations:
                grouped_citations[key] = []
            grouped_citations[key].append(item)
            
        index = 1
        for key, occurrences in grouped_citations.items():
            if key in bib_data:
                title = bib_data[key].get('title', 'Unknown Title')
                author = bib_data[key].get('author', 'Unknown Author')
                year = bib_data[key].get('year', 'Unknown Year')
                citation_info = f"**{key}**<br>{title}<br>{author}, {year}"
            else:
                citation_info = f"**{key}**<br>NOT FOUND IN BIB"

            # Combine locations and contexts
            locations = []
            contexts = []
            
            for occ in occurrences:
                loc = f"{occ['file']}:{occ['line']}"
                locations.append(loc)
                # Truncate context if too long
                ctx = occ['context']
                if len(ctx) > 300:
                    ctx = ctx[:300] + "..."
                contexts.append(f"**[{loc}]**: {ctx}")
            
            location_str = "<br>".join(locations)
            context_str = "<br><br>".join(contexts)
            
            f.write(f"| {index} | {citation_info} | {location_str} | {context_str} | | |\n")
            index += 1
            
    print(f"Report generated at {output_file}")

if __name__ == "__main__":
    base_dir = r"c:\学习\研究生学习\毕设"
    tex_dir = os.path.join(base_dir, "body")
    bib_path = os.path.join(base_dir, "ref", "refs.bib")
    output_file = os.path.join(base_dir, "citation_verification_results.md")
    
    print("Parsing bib file...")
    bib_data = parse_bib_file(bib_path)
    
    print("Extracting citations...")
    citations = extract_citations_from_tex(tex_dir)
    
    print("Generating report...")
    generate_report(citations, bib_data, output_file)
