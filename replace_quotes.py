import os
import re
import sys

def replace_quotes_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"无法读取文件 {filepath}: {e}")
        return False
        
    in_quote = False
    new_lines = []
    replace_count = 0
    
    for i, line in enumerate(lines):
        # 如果是注释行，直接跳过替换（保留原样）
        if line.lstrip().startswith('%'):
            new_lines.append(line)
            continue
            
        new_line = ""
        # 逐字符检查和替换
        # 但我们也要小心 LaTeX 的转义引号 \" 或带有特定宏的情况，不过根据前一次检查，这里的引号直接是普通的 "
        
        j = 0
        while j < len(line):
            char = line[j]
            if char == '"':
                # 判断前一个字符是否为系统转义字符 \ ，如果是 \" 可能是特殊命令，我们先简单假设正文直接用的 " 没有转义。
                # 但如果在某些latex里存在 \" ，这里加个小判断
                if j > 0 and line[j-1] == '\\':
                    new_line += '"' # 保留原样
                else:
                    if not in_quote:
                        new_line += '“'
                        in_quote = True
                    else:
                        new_line += '”'
                        in_quote = False
                    replace_count += 1
            else:
                new_line += char
            j += 1
            
        new_lines.append(new_line)

    if in_quote:
        print(f"  [警告] {filepath} 替换结束时存在未闭合的左引号，可能原文引号不成对！请手动检查。")
        
    if replace_count > 0:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"[{filepath}] 成功替换了 {replace_count} 个英文直引号。")
            return True
        except Exception as e:
            print(f"无法写入文件 {filepath}: {e}")
            return False
    return False
        
def main():
    base_dir = r"c:\学习\研究生学习\毕设\body"
    
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
        
    tex_files = []
    try:
        if not os.path.exists(base_dir):
            print(f"目录不存在: {base_dir}")
            return
            
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
        
    print(f"开始替换目录 {base_dir} 下所有 .tex 文件中的英文引号...\n")
    replaced_files = 0
    for f in tex_files:
        if replace_quotes_in_file(f):
            replaced_files += 1
            
    if replaced_files == 0:
        print("所有文件均无需替换，未发现英文直引号。")
    else:
        print(f"\n替换完毕，共修改了 {replaced_files} 个文件！")

if __name__ == "__main__":
    main()
