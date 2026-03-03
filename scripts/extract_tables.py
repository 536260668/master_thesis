import re

with open(r'c:\学习\研究生学习\毕设\body\chap04.tex', 'r', encoding='utf-8') as f:
    text = f.read()

tables = re.findall(r'\\begin\{table\}.*?\\end\{table\}', text, re.DOTALL)

with open(r'c:\学习\研究生学习\毕设\text_ref\chap04_tables_backup.tex', 'w', encoding='utf-8') as out_f:
    out_f.write('\n\n'.join(tables) + '\n')

print(f'Done! Found {len(tables)} tables.')
