import os

# Total samples
TOTAL = 96

# Raw counts from process_chap5_data.py
RAW = {
    "poison_10": {
        "bbbb": [14, 19, 22, 33],
        "gggg": [ 5,  7,  6,  8],
    },
    "poison_50": {
        "bbbb": [69, 75, 77, 77],
        "gggg": [ 5,  7,  6,  8],
    },
    "paa": {
        "bbbb": [72, 85, 79, 85],
        "gggg": [ 5,  7,  6,  8],
    },
    "jailbreak": {
        "bbbb": [90, 94, 94, 96],
        "gggg": [ 5,  7,  6,  8],
    },
}

def calculate_alpha():
    results = {}
    for key, data in RAW.items():
        bad = data["bbbb"]
        good = data["gggg"]
        alphas = []
        for b, g in zip(bad, good):
            # alpha = ASR_bad / ASR_good
            # Using counts directly simplifies to b / g
            alpha = b / g if g != 0 else 0
            alphas.append(round(alpha, 2))
        results[key] = alphas
    return results

if __name__ == "__main__":
    alphas = calculate_alpha()
    output_path = r"c:\学习\研究生学习\毕设\text_ref\chap5_alpha_comparison.md"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 第五章 错误放大因子 (alpha) 跨方法对比\n\n")
        f.write("> 计算公式: alpha_i = ASR_i(bbbb) / ASR_i(gggg)\n\n")
        f.write("| 攻击类型 | alpha_1 | alpha_2 | alpha_3 | alpha_4 | 平均 alpha |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for key, vals in alphas.items():
            avg = round(sum(vals) / len(vals), 2)
            f.write(f"| {key} | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | {avg} |\n")
    
    print(f"Alpha values calculated and saved to {output_path}")
    for key, vals in alphas.items():
        print(f"{key}: {vals}")
