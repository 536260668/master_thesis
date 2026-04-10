import re
import os

def calculate_asr(count, total=96):
    try:
        asr = (float(count) / total) * 100
        return f"{asr:.2f}%"
    except (ValueError, ZeroDivisionError):
        return count

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regular expression to find table rows
    # Example: | gggg | 5 | 7 | 6 | 8 |
    # We want to keep the first column (Model List) and transform the numbers in the other columns
    
    def replace_counts(match):
        # match.group(0) is the whole row like "| gggg | 5 | 7 | 6 | 8 |"
        parts = match.group(0).split('|')
        # parts will be ['', ' gggg ', ' 5 ', ' 7 ', ' 6 ', ' 8 ', '']
        # We transform parts[2:-1] which are the counts
        new_parts = [parts[0], parts[1]]
        for part in parts[2:-1]:
            stripped_part = part.strip()
            if stripped_part.isdigit():
                new_parts.append(f" {calculate_asr(stripped_part)} ")
            else:
                new_parts.append(part)
        new_parts.append(parts[-1])
        return '|'.join(new_parts)

    # Match rows that start and end with | and have at least one numeric cell
    # This avoids header and separator lines mostly, but the check for isdigit() is safer
    processed_content = re.sub(r'^\|.*\|\s*$', replace_counts, content, flags=re.MULTILINE)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)

if __name__ == "__main__":
    input_file = r"c:\学习\研究生学习\毕设\text_ref\new_data\chap5_new_data.md"
    output_file = r"c:\学习\研究生学习\毕设\text_ref\new_data\chap5_asr_results.md"
    process_file(input_file, output_file)
    print(f"Processed {input_file} and saved results to {output_file}")
