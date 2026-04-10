import os
import re
import sys

def check_quotes_in_file(filepath):
    issues_found = False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"无法读取文件 {filepath}: {e}")
        return False
        
    in_quote = False
    quote_start_line = -1
    
    file_issues = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # 忽略 LaTeX 注释 (不严谨，但在一般情况下够用)
        # 仅忽略行首或者空白后的%，避免误判 \% 
        content = re.sub(r'(?<!\\)%.*$', '', line)
        
        # 1. 检查英文直引号 "
        for match in re.finditer(r'"', content):
            file_issues.append(f"  [非中文引号] 第 {line_num} 行第 {match.start()+1} 列发现英文双引号 '\"'")
            
        # 2. 检查英文单直引号 ' （非撇号的情况），由于撇号 ' 常用作英语的 isn't，只在特定情况下报警告
        # 为避免过多误报，这里暂且省略，如有需要可加上
            
        # 3. 检查成对的中文双引号 “ ” 
        for j, char in enumerate(content):
            if char == '“':
                if in_quote:
                    file_issues.append(f"  [引号嵌套/不成对] 第 {line_num} 行发现左引号 '“'，但在第 {quote_start_line} 行已有一个未闭合的左引号，可能存在嵌套或漏写右引号！")
                in_quote = True
                quote_start_line = line_num
            elif char == '”':
                if not in_quote:
                    file_issues.append(f"  [多余右引号] 第 {line_num} 行发现右引号 '”'，但之前没有对应的左引号！")
                in_quote = False
            
        # 4. 检查是否有中文全角空格等可能引发排版问题的字符 (可选)
        # if '　' in content:
        #     file_issues.append(f"  [全角空格] 第 {line_num} 行发现全角空格，LaTeX排版通常不需要全角空格。")
            
        # 段落结束（空行）时，引号应该闭合。LaTeX中空行表示新段落
        if content.strip() == "":
            if in_quote:
                file_issues.append(f"  [跨段落未闭合] 段落结束（空行）时发现未闭合的左引号 (该左引号在此段落中起始于第 {quote_start_line} 行)")
                in_quote = False # 重置状态，避免跨段落时引发连锁误报

    if in_quote:
        file_issues.append(f"  [文件结束未闭合] 文件扫描结束时，发现未闭合的左引号 (起始于第 {quote_start_line} 行)")
        
    if file_issues:
        print(f"=== {filepath} ===")
        for issue in file_issues:
            print(issue)
        print()
        issues_found = True
        
    return issues_found
        
def main():
    base_dir = r"c:\学习\研究生学习\毕设\body"
    
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
        
    tex_files = []
    try:
        # 仅查看当前文件夹，不查看子文件夹
        for f in os.listdir(base_dir):
            if f.endswith('.tex'):
                filepath = os.path.join(base_dir, f)
                if os.path.isfile(filepath):
                    tex_files.append(filepath)
    except Exception as e:
        print(f"无法访问目录 {base_dir}: {e}")
        return
                
    if not tex_files:
        print(f"在 {base_dir} 中没有找到 .tex 文件。")
        return
        
    total_issues = 0
    print(f"开始检查目录 {base_dir} 下的所有 .tex 文件...\n")
    for f in tex_files:
        has_issue = check_quotes_in_file(f)
        if has_issue:
            total_issues += 1
            
    if total_issues == 0:
        print("完美！所有文件的引号格式均正确且成对。")
    else:
        print(f"检查完毕，共有 {total_issues} 个文件存在引号问题，请查看上方输出进行修改。")

if __name__ == "__main__":
    main()
