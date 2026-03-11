import argparse
import time
import requests
import re
import json
import difflib
from pathlib import Path

def query_semantic_scholar(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "title,authors,externalIds,url,year,venue,journal,pages,publicationTypes,publicationDate"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                return data['data'][0]
    except Exception as e:
        return None
    return None

def query_crossref(title):
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": title,
        "rows": 1,
        "select": "title,author,DOI,URL,container-title,volume,issue,page,published-print,published-online,type,event"
    }
    headers = {"User-Agent": "mailto:test@example.com"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get('message', {}).get('items', [])
            if items:
                return items[0]
    except Exception as e:
        return None
    return None

def extract_fields(fields_str):
    fields = {}
    i = 0
    n = len(fields_str)
    while i < n:
        while i < n and fields_str[i] in ' \t\n\r,':
            i += 1
        if i >= n:
            break
        name_start = i
        while i < n and fields_str[i] not in ' \t\n\r=':
            i += 1
        name = fields_str[name_start:i].strip().lower()
        if not name:
            i += 1
            continue
        while i < n and fields_str[i] != '=':
            if fields_str[i] == ',':
                break
            i += 1
        if i >= n or fields_str[i] != '=':
            continue
        i += 1
        while i < n and fields_str[i] in ' \t\n\r':
            i += 1
        if i >= n:
            break
        char = fields_str[i]
        if char == '{':
            brace_count = 1
            i += 1
            val_start = i
            while i < n and brace_count > 0:
                if fields_str[i] == '{':
                    brace_count += 1
                elif fields_str[i] == '}':
                    brace_count -= 1
                i += 1
            val = fields_str[val_start:max(val_start, i-1)]
        elif char == '"':
            i += 1
            val_start = i
            while i < n and fields_str[i] != '"':
                i += 1
            val = fields_str[val_start:i]
            i += 1
        else:
            val_start = i
            while i < n and fields_str[i] not in ',\n\r':
                i += 1
            val = fields_str[val_start:i]
        fields[name] = val.strip()
    return fields

def parse_bib_file(filepath):
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    idx = 0
    while idx < len(content):
        start = content.find('@', idx)
        if start == -1:
            break
        brace_open = content.find('{', start)
        if brace_open == -1:
            break
        entry_type = content[start+1:brace_open].strip()
        brace_count = 1
        curr = brace_open + 1
        while curr < len(content) and brace_count > 0:
            if content[curr] == '{':
                brace_count += 1
            elif content[curr] == '}':
                brace_count -= 1
            curr += 1
        if brace_count == 0:
            entry_str = content[start+1:curr-1]
            parts = entry_str.split('{', 1)
            if len(parts) == 2:
                rest = parts[1].strip()
                k_parts = rest.split(',', 1)
                # Ensure we have at least ID and fields
                if len(k_parts) == 2:
                    key = k_parts[0].strip()
                    fields_str = k_parts[1]
                    entry = {'ID': key, 'ENTRYTYPE': entry_type.lower()}
                    entry.update(extract_fields(fields_str))
                    entries.append(entry)
        idx = curr
    return entries

def format_bib_entry(entry_type, key, fields):
    if not entry_type:
        entry_type = 'article'
    lines = [f"@{entry_type}{{{key},"]
    order = ['title', 'author', 'journal', 'booktitle', 'volume', 'number', 'pages', 'year', 'publisher', 'doi', 'note', 'url']
    for k in order:
        if k in fields and str(fields[k]).strip():
            lines.append(f"  {k:<13} = {{{fields[k]}}},")
    for k, v in fields.items():
        if k not in order and k not in ['ID', 'ENTRYTYPE', 'found_source', 'eprint', 'archiveprefix', 'primaryclass'] and str(v).strip():
            lines.append(f"  {k:<13} = {{{v}}},")
    if len(lines) > 1 and lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)

def is_similar(t1, t2):
    if not t1 or not t2: return False
    s1 = re.sub(r'[^a-zA-Z0-9]', '', t1).lower()
    s2 = re.sub(r'[^a-zA-Z0-9]', '', t2).lower()
    if not s1 or not s2: return False
    # If one is a complete substring of another
    if s1 in s2 or s2 in s1:
        return True
    return difflib.SequenceMatcher(None, s1, s2).ratio() > 0.85

def process_entry(entry):
    bib_title = entry.get('title', '').replace('{', '').replace('}', '').replace('\n', ' ')
    original_type = entry.get('ENTRYTYPE', 'article')
    original_key = entry.get('ID', 'Unknown')
    
    if not bib_title:
        entry['found_source'] = 'None'
        return entry
        
    print(f"  -> SS 查询: {bib_title[:50]}...")
    ss_data = query_semantic_scholar(bib_title)
    if ss_data and (ss_data.get('authors') or ss_data.get('year')):
        ss_title = ss_data.get('title', '')
        if is_similar(bib_title, ss_title):
            fields = {}
            if ss_title: fields['title'] = ss_title
            if ss_data.get('authors'):
                author_names = [a['name'] for a in ss_data['authors'] if 'name' in a]
                if author_names: fields['author'] = ' and '.join(author_names)
            if ss_data.get('year'): fields['year'] = str(ss_data['year'])
            if ss_data.get('journal') and ss_data['journal'].get('name'):
                fields['journal'] = ss_data['journal']['name']
            elif ss_data.get('venue'):
                fields['journal'] = ss_data['venue']
                
            if ss_data.get('journal') and ss_data['journal'].get('pages'):
                fields['pages'] = ss_data['journal']['pages'].replace('-', '--')
            elif ss_data.get('pages'):
                fields['pages'] = ss_data['pages'].replace('-', '--')
                
            ext_ids = ss_data.get('externalIds', {})
            if ext_ids.get('DOI'): fields['doi'] = ext_ids['DOI']
            if ext_ids.get('ArXiv'): fields['note'] = f"arXiv:{ext_ids['ArXiv']}"
            if ss_data.get('url'): fields['url'] = ss_data['url']

            for k, v in entry.items():
                if k not in fields and k not in ['ID', 'ENTRYTYPE', 'eprint', 'archiveprefix', 'primaryclass', 'found_source']:
                    fields[k] = v
                    
            pub_types = ss_data.get('publicationTypes', [])
            if not pub_types: pub_types = []
            if 'JournalArticle' in pub_types: 
                entry_type = 'article'
            elif 'Conference' in pub_types:
                entry_type = 'inproceedings'
                if 'journal' in fields:
                    fields['booktitle'] = fields['journal']
                    del fields['journal']
            else:
                entry_type = original_type
                
            if fields.get('note') and 'arxiv' in str(fields['note']).lower() and 'journal' not in fields and 'booktitle' not in fields:
                entry_type = 'article'
                
            fields['ID'] = original_key
            fields['ENTRYTYPE'] = entry_type
            fields['found_source'] = 'Semantic Scholar'
            print("  -> 使用 Semantic Scholar 查找到匹配结果。")
            return fields
        else:
            print("  -> SS 结果标题差异过大，跳过。")
            
    # Check Crossref fallback
    print("  -> 尝试 Crossref 查询...")
    cr_data = query_crossref(bib_title)
    if cr_data and cr_data.get('title'):
        cr_title = cr_data['title'][0] if isinstance(cr_data['title'], list) else cr_data['title']
        if is_similar(bib_title, cr_title):
            fields = {}
            fields['title'] = cr_title
            if cr_data.get('author'):
                authors = []
                for a in cr_data['author']:
                    if 'family' in a and 'given' in a: authors.append(f"{a['family']}, {a['given']}")
                    elif 'family' in a: authors.append(a['family'])
                    elif 'literal' in a: authors.append(a['literal'])
                if authors: fields['author'] = ' and '.join(authors)
                
            if cr_data.get('published-print') and cr_data['published-print'].get('date-parts'):
                fields['year'] = str(cr_data['published-print']['date-parts'][0][0])
            elif cr_data.get('published-online') and cr_data['published-online'].get('date-parts'):
                fields['year'] = str(cr_data['published-online']['date-parts'][0][0])
                
            if cr_data.get('container-title'):
                fields['journal'] = cr_data['container-title'][0] if isinstance(cr_data['container-title'], list) else cr_data['container-title']
            if cr_data.get('volume'): fields['volume'] = cr_data['volume']
            if cr_data.get('issue'): fields['number'] = cr_data['issue']
            if cr_data.get('page'): fields['pages'] = cr_data['page'].replace('-', '--')
            if cr_data.get('DOI'): fields['doi'] = cr_data['DOI']
            
            for k, v in entry.items():
                if k not in fields and k not in ['ID', 'ENTRYTYPE', 'eprint', 'archiveprefix', 'primaryclass', 'found_source']:
                    fields[k] = v
                    
            item_type = cr_data.get('type', '')
            if item_type == 'journal-article': entry_type = 'article'
            elif item_type == 'proceedings-article' or item_type == 'paper-conference':
                entry_type = 'inproceedings'
                if 'journal' in fields:
                    fields['booktitle'] = fields['journal']
                    del fields['journal']
            else:
                entry_type = original_type
                
            fields['ID'] = original_key
            fields['ENTRYTYPE'] = entry_type
            fields['found_source'] = 'Crossref'
            print("  -> 使用 Crossref 查找到匹配结果。")
            return fields
        else:
            print("  -> Crossref 结果标题差异过大，跳过。")

    print("  -> 无法在线上数据库中精确匹配（或匹配失败），保留原样。")
    entry['found_source'] = 'None'
    return entry

def main():
    parser = argparse.ArgumentParser("自动完善 BibTeX 引用格式工具")
    parser.add_argument("bib_file", help="输入你的 .bib 文件路径, 比如 ref/refs.bib")
    parser.add_argument("-n", "--limit", type=int, default=None, help="控制校验前 N 个 cite，不指定则校验全部")
    parser.add_argument("-o", "--output", default="citation_report.md", help="输出 Markdown 报告或 Bib 路径")
    args = parser.parse_args()
    
    bib_path = Path(args.bib_file)
    if not bib_path.exists():
        print(f"找不到文件: {bib_path}")
        return
        
    print(f"正在读取并解析: {bib_path} ...")
    entries = parse_bib_file(bib_path)
    if not entries:
        print("未能解析出任何 bib 条目，请检查文件格式。")
        return
        
    limit = args.limit if args.limit else len(entries)
    entries_to_check = entries[:limit]
    
    results = []
    print(f"\n开始使用多接口验证和补全前 {limit} 条引用...")
    for i, entry in enumerate(entries_to_check):
        key = entry.get('ID', 'Unknown')
        print(f"[{i+1}/{limit}] 正在核对: {key}")
        res = process_entry(entry)
        results.append(res)
        time.sleep(1.0)
        
    out_path = Path(args.output)
    is_markdown = out_path.suffix.lower() == '.md'
    
    with open(out_path, 'w', encoding='utf-8') as f:
        if is_markdown:
            f.write("# 参考文献补全生成结果\n\n")
            f.write("> 结合了 Semantic Scholar 和 Crossref 接口生成标准 BibTeX。您可以直接复制以下文本到 `.bib` 文件中覆盖原有条目。\n\n")
            f.write("```bibtex\n")
            
        for r in results:
            entry_type = r.get('ENTRYTYPE', 'article')
            key = r.get('ID', 'Unknown')
            formatted = format_bib_entry(entry_type, key, r)
            f.write(formatted + "\n\n")
            
        if is_markdown:
            f.write("```\n")
            
    print(f"\n生成完毕！格式化结果已保存至：{out_path.absolute()}")

if __name__ == "__main__":
    main()
