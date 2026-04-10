"""
verify_bib.py - 逐条验证 refs.bib 中的文献条目
==================================================

功能：
1. 解析 refs.bib，提取每条文献的 title
2. 在 DBLP 上搜索该 title，获取对应的 BibTeX
3. 对比本地 bib 条目与 DBLP 返回的 BibTeX，记录不一致项
4. 支持断点重启（已完成的条目记录在 checkpoint 文件中）
5. 生成 Markdown 报告

用法：
    python verify_bib.py                          # 验证全部条目
    python verify_bib.py --start 10               # 从第10条开始
    python verify_bib.py --count 5                # 只验证5条
    python verify_bib.py --reset                  # 清除断点，重新开始
    python verify_bib.py --bib path/to/refs.bib   # 指定 bib 文件路径
"""

from __future__ import annotations

import re
import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime

# ======================== 配置 ========================

SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_BIB_PATH = SCRIPT_DIR.parent.parent / "ref" / "refs.bib"
CHECKPOINT_FILE = SCRIPT_DIR / "verify_checkpoint.json"
REPORT_FILE = SCRIPT_DIR.parent.parent / "citation_verify_report.md"

# DBLP API
DBLP_SEARCH_URL = "https://dblp.org/search/publ/api"
DBLP_BIBTEX_BASE = "https://dblp.org/rec/{key}.bib"

# 请求间隔 (秒)，避免被限流
REQUEST_DELAY = 2.0

# 代理配置（如需要则修改）
PROXY_ENABLED = False
PROXY_URL = "http://127.0.0.1:10809"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# 跳过验证的条目 key 模式（模板相关条目等）
SKIP_KEYS = {
    "BEZOS02", "dvipdfm", "dvips", "TEXGURU99", "OETIKER02",
    "guide", "standard", "modal", "Collin", "Oliner_MTT_1984_09",
    "NPB2", "jppat",
    # 以下为非学术文献（软件仓库、数据集页面等），DBLP 不收录
    "toxicqafinal2024", "llamacpp2024", "ollama2024",
    "team2024safety",  # OpenAI system card
    "nhc2020clinical",  # 中文政府报告
    "who2021clinical",  # WHO 指南书籍
    "rothman2008epidemiology",  # 教科书
}


# ======================== BibTeX 解析 ========================

def parse_bib_file(bib_path: str) -> list[dict]:
    """解析 bib 文件，返回条目列表。每个条目包含 key, type, fields, raw_text, line_number。"""
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # 匹配 @type{key, ... }
    # 使用逐字符方式正确处理嵌套大括号
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检测条目起始行
        match = re.match(r"@(\w+)\s*\{(.+?),\s*$", line.strip())
        if match:
            entry_type = match.group(1).lower()
            entry_key = match.group(2).strip()
            start_line = i + 1  # 1-indexed
            # 收集完整条目文本
            brace_count = line.count("{") - line.count("}")
            raw_lines = [line]
            j = i + 1
            while j < len(lines) and brace_count > 0:
                raw_lines.append(lines[j])
                brace_count += lines[j].count("{") - lines[j].count("}")
                j += 1
            raw_text = "\n".join(raw_lines)
            # 解析字段
            fields = parse_bib_fields(raw_text)
            entries.append({
                "key": entry_key,
                "type": entry_type,
                "fields": fields,
                "raw_text": raw_text,
                "line_number": start_line,
            })
            i = j
        else:
            i += 1

    return entries


def parse_bib_fields(raw_text: str) -> dict:
    """从 bib 条目原始文本中提取字段。"""
    fields = {}
    # 匹配 field = {value} 或 field = "value" 或 field = number
    # 处理多行值
    field_pattern = re.compile(
        r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))",
        re.DOTALL
    )
    for m in field_pattern.finditer(raw_text):
        field_name = m.group(1).lower()
        value = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        if value:
            # 清理多行空白
            value = re.sub(r"\s+", " ", value).strip()
            fields[field_name] = value
    return fields


# ======================== DBLP 搜索 ========================

def get_proxies():
    if PROXY_ENABLED:
        return {"http": PROXY_URL, "https": PROXY_URL}
    return None


def search_dblp(title: str) -> dict | None:
    """在 DBLP 搜索标题，返回最佳匹配的文献信息。"""
    # 清理标题中的 LaTeX 命令
    clean_title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    clean_title = re.sub(r"[{}\\]", "", clean_title)
    clean_title = clean_title.strip()

    params = {
        "q": clean_title,
        "format": "json",
        "h": 5,  # 返回前5条结果
    }

    try:
        resp = requests.get(
            DBLP_SEARCH_URL, params=params, headers=HEADERS,
            proxies=get_proxies(), timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [ERROR] DBLP search failed: {e}")
        return None

    result = data.get("result", {})
    hits = result.get("hits", {})
    hit_list = hits.get("hit", [])

    if not hit_list:
        return None

    # 选择标题相似度最高的结果
    best_match = None
    best_score = 0.0
    for hit in hit_list:
        info = hit.get("info", {})
        dblp_title = info.get("title", "")
        # 去掉末尾句点
        dblp_title = dblp_title.rstrip(".")
        score = title_similarity(clean_title, dblp_title)
        if score > best_score:
            best_score = score
            best_match = info
            # 使用 info.key 作为 DBLP record key (如 "conf/naacl/DevlinCLT19")
            best_match["_dblp_key"] = info.get("key", "")
            best_match["_similarity"] = score

    if best_match and best_score >= 0.5:
        return best_match
    return None


def get_dblp_bibtex(dblp_key: str) -> str | None:
    """通过 DBLP key 获取 BibTeX 条目。"""
    url = f"https://dblp.org/rec/{dblp_key}.bib"
    try:
        resp = requests.get(url, headers=HEADERS, proxies=get_proxies(), timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  [ERROR] Failed to get BibTeX for {dblp_key}: {e}")
        return None


def title_similarity(s1: str, s2: str) -> float:
    """计算两个标题的相似度（基于单词集合的 Jaccard 系数）。"""
    def normalize(s):
        s = s.lower()
        s = re.sub(r"[^a-z0-9\s]", "", s)
        return set(s.split())

    words1 = normalize(s1)
    words2 = normalize(s2)
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


# ======================== 比较逻辑 ========================

def compare_entries(local: dict, dblp_info: dict, dblp_bibtex: str | None) -> list[dict]:
    """比较本地条目与 DBLP 结果，返回不一致项列表。"""
    diffs = []
    local_fields = local["fields"]

    # 比较标题
    local_title = re.sub(r"[{}\\]", "", local_fields.get("title", ""))
    local_title = re.sub(r"\s+", " ", local_title).strip()
    dblp_title = dblp_info.get("title", "").rstrip(".")
    if title_similarity(local_title, dblp_title) < 0.9:
        diffs.append({
            "field": "title",
            "local": local_fields.get("title", ""),
            "dblp": dblp_title,
        })

    # 比较作者
    dblp_authors_info = dblp_info.get("authors", {}).get("author", [])
    if isinstance(dblp_authors_info, dict):
        dblp_authors_info = [dblp_authors_info]
    dblp_author_names = []
    for a in dblp_authors_info:
        if isinstance(a, dict):
            dblp_author_names.append(a.get("text", a.get("@text", "")))
        elif isinstance(a, str):
            dblp_author_names.append(a)

    local_author = local_fields.get("author", "")
    # 检查 "and others" 占位使用 -> 不做严格完整性比较，但检查首作者
    if dblp_author_names:
        # 提取本地首作者姓氏
        local_first = local_author.split(",")[0].strip() if local_author else ""
        local_first = re.sub(r"[{}\\]", "", local_first).strip()
        dblp_first_full = dblp_author_names[0]
        # DBLP 格式通常是 "Firstname Lastname"，取姓氏
        dblp_first_last = dblp_first_full.split()[-1] if dblp_first_full else ""

        if local_first.lower() != dblp_first_last.lower():
            diffs.append({
                "field": "author (first author mismatch)",
                "local": local_first,
                "dblp": dblp_first_full,
            })

        # 如果本地没有使用 "and others" 缩写，比较作者数量
        if "others" not in local_author.lower():
            local_author_count = len([a.strip() for a in local_author.split(" and ") if a.strip()])
            dblp_author_count = len(dblp_author_names)
            if abs(local_author_count - dblp_author_count) > 2:
                diffs.append({
                    "field": "author (count differs significantly)",
                    "local": f"{local_author_count} authors",
                    "dblp": f"{dblp_author_count} authors",
                })

    # 比较年份
    local_year = local_fields.get("year", "")
    dblp_year = str(dblp_info.get("year", ""))
    if local_year and dblp_year and local_year != dblp_year:
        diffs.append({
            "field": "year",
            "local": local_year,
            "dblp": dblp_year,
        })

    # 比较出版场所 (venue)
    dblp_venue = dblp_info.get("venue", "")
    if isinstance(dblp_venue, list):
        dblp_venue = ", ".join(dblp_venue)
    local_journal = local_fields.get("journal", local_fields.get("booktitle", ""))
    # venue 比较仅做提示级别，不强制匹配

    # 比较 DOI
    dblp_doi = dblp_info.get("doi", "")
    local_doi = local_fields.get("doi", "")
    if dblp_doi and local_doi:
        if dblp_doi.lower().strip() != local_doi.lower().strip():
            diffs.append({
                "field": "doi",
                "local": local_doi,
                "dblp": dblp_doi,
            })
    elif dblp_doi and not local_doi:
        diffs.append({
            "field": "doi (missing in local)",
            "local": "(none)",
            "dblp": dblp_doi,
        })

    # 如果有 DBLP BibTeX，解析并比较 pages / volume
    if dblp_bibtex:
        dblp_fields = parse_bib_fields(dblp_bibtex)
        for compare_field in ["volume", "pages", "number"]:
            local_val = local_fields.get(compare_field, "")
            dblp_val = dblp_fields.get(compare_field, "")
            if local_val and dblp_val:
                # 标准化 pages 格式 (--  vs -)
                norm_local = local_val.replace("--", "-").strip()
                norm_dblp = dblp_val.replace("--", "-").strip()
                if norm_local != norm_dblp:
                    diffs.append({
                        "field": compare_field,
                        "local": local_val,
                        "dblp": dblp_val,
                    })

    return diffs


# ======================== 断点管理 ========================

def load_checkpoint() -> dict:
    """加载断点信息。"""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed_keys": [], "results": []}


def save_checkpoint(checkpoint: dict):
    """保存断点信息。"""
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def reset_checkpoint():
    """清除断点文件。"""
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
        print("Checkpoint cleared.")


# ======================== 报告生成 ========================

def generate_report(results: list[dict], total_entries: int, report_path: str):
    """生成 Markdown 格式的验证报告。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 统计
    verified_count = len(results)
    mismatch_count = sum(1 for r in results if r.get("status") == "mismatch")
    not_found_count = sum(1 for r in results if r.get("status") == "not_found")
    match_count = sum(1 for r in results if r.get("status") == "match")
    error_count = sum(1 for r in results if r.get("status") == "error")
    skipped_count = sum(1 for r in results if r.get("status") == "skipped")

    lines = []
    lines.append("# BibTeX 验证报告")
    lines.append("")
    lines.append(f"生成时间: {now}")
    lines.append("")
    lines.append("## 统计概览")
    lines.append("")
    lines.append(f"| 项目 | 数量 |")
    lines.append(f"|------|------|")
    lines.append(f"| bib 文件总条目数 | {total_entries} |")
    lines.append(f"| 已验证条目数 | {verified_count} |")
    lines.append(f"| 完全匹配 | {match_count} |")
    lines.append(f"| 存在差异 | {mismatch_count} |")
    lines.append(f"| DBLP 未收录 | {not_found_count} |")
    lines.append(f"| 跳过 (非学术/模板) | {skipped_count} |")
    lines.append(f"| 搜索出错 | {error_count} |")
    lines.append("")

    # 不一致详情
    mismatches = [r for r in results if r.get("status") == "mismatch"]
    if mismatches:
        lines.append("## 存在差异的条目")
        lines.append("")
        for r in mismatches:
            lines.append(f"### `{r['key']}` (第 {r.get('line', '?')} 行)")
            lines.append("")
            lines.append(f"**本地标题**: {r.get('local_title', 'N/A')}")
            lines.append("")
            lines.append(f"**DBLP 标题**: {r.get('dblp_title', 'N/A')}")
            lines.append("")
            lines.append(f"**相似度**: {r.get('similarity', 0):.2%}")
            lines.append("")
            if r.get("diffs"):
                lines.append("| 字段 | 本地值 | DBLP 值 |")
                lines.append("|------|--------|---------|")
                for d in r["diffs"]:
                    local_escaped = str(d['local']).replace("|", "\\|")
                    dblp_escaped = str(d['dblp']).replace("|", "\\|")
                    lines.append(f"| {d['field']} | {local_escaped} | {dblp_escaped} |")
                lines.append("")
            if r.get("dblp_bibtex"):
                lines.append("<details>")
                lines.append("<summary>DBLP 返回的 BibTeX</summary>")
                lines.append("")
                lines.append("```bibtex")
                lines.append(r["dblp_bibtex"].strip())
                lines.append("```")
                lines.append("</details>")
                lines.append("")
            lines.append("---")
            lines.append("")

    # DBLP 未找到的条目
    not_founds = [r for r in results if r.get("status") == "not_found"]
    if not_founds:
        lines.append("## DBLP 未收录的条目")
        lines.append("")
        lines.append("以下条目未在 DBLP 中找到匹配结果，可能是非 CS 领域文献、过于新、或标题差异较大：")
        lines.append("")
        for r in not_founds:
            lines.append(f"- `{r['key']}` (第 {r.get('line', '?')} 行): {r.get('local_title', 'N/A')}")
        lines.append("")

    # 匹配的条目
    matches = [r for r in results if r.get("status") == "match"]
    if matches:
        lines.append("## 完全匹配的条目")
        lines.append("")
        for r in matches:
            lines.append(f"- `{r['key']}`: {r.get('local_title', 'N/A')}")
        lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport saved to: {report_path}")


# ======================== 主流程 ========================

def main():
    parser = argparse.ArgumentParser(description="验证 refs.bib 文献条目")
    parser.add_argument("--bib", type=str, default=str(DEFAULT_BIB_PATH),
                        help="bib 文件路径")
    parser.add_argument("--start", type=int, default=0,
                        help="从第 N 条开始验证 (0-indexed)")
    parser.add_argument("--count", type=int, default=0,
                        help="验证条目数量（0 表示全部）")
    parser.add_argument("--reset", action="store_true",
                        help="清除断点，重新开始")
    parser.add_argument("--report", type=str, default=str(REPORT_FILE),
                        help="报告输出路径")
    parser.add_argument("--delay", type=float, default=REQUEST_DELAY,
                        help="请求间隔（秒）")
    parser.add_argument("--proxy", action="store_true",
                        help="启用代理")
    args = parser.parse_args()

    global PROXY_ENABLED
    if args.proxy:
        PROXY_ENABLED = True

    if args.reset:
        reset_checkpoint()

    # 解析 bib 文件
    print(f"Parsing bib file: {args.bib}")
    entries = parse_bib_file(args.bib)
    total_entries = len(entries)
    print(f"Found {total_entries} entries in bib file.")

    # 加载断点
    checkpoint = load_checkpoint()
    completed_keys = set(checkpoint.get("completed_keys", []))
    results = checkpoint.get("results", [])

    print(f"Already completed: {len(completed_keys)} entries.")

    # 确定待验证范围
    to_verify = entries[args.start:]
    if args.count > 0:
        to_verify = to_verify[:args.count]

    # 过滤已完成的条目
    to_verify = [e for e in to_verify if e["key"] not in completed_keys]
    print(f"Entries to verify this run: {len(to_verify)}")
    print("=" * 60)

    for idx, entry in enumerate(to_verify):
        key = entry["key"]
        title = entry["fields"].get("title", "")
        entry_type = entry["type"]
        line_no = entry["line_number"]

        print(f"\n[{idx + 1}/{len(to_verify)}] Verifying: {key} (line {line_no})")
        print(f"  Title: {title[:80]}{'...' if len(title) > 80 else ''}")

        # 跳过非学术条目
        if key in SKIP_KEYS or entry_type in ("patent",):
            print(f"  -> SKIPPED (non-academic / template entry)")
            result = {
                "key": key,
                "line": line_no,
                "status": "skipped",
                "local_title": title,
            }
            results.append(result)
            completed_keys.add(key)
            checkpoint["completed_keys"] = list(completed_keys)
            checkpoint["results"] = results
            save_checkpoint(checkpoint)
            continue

        if not title:
            print(f"  -> SKIPPED (no title field)")
            result = {
                "key": key,
                "line": line_no,
                "status": "skipped",
                "local_title": "(no title)",
            }
            results.append(result)
            completed_keys.add(key)
            checkpoint["completed_keys"] = list(completed_keys)
            checkpoint["results"] = results
            save_checkpoint(checkpoint)
            continue

        # DBLP 搜索
        try:
            dblp_info = search_dblp(title)
            time.sleep(args.delay)
        except Exception as e:
            print(f"  -> ERROR: {e}")
            result = {
                "key": key,
                "line": line_no,
                "status": "error",
                "local_title": title,
                "error": str(e),
            }
            results.append(result)
            completed_keys.add(key)
            checkpoint["completed_keys"] = list(completed_keys)
            checkpoint["results"] = results
            save_checkpoint(checkpoint)
            continue

        if not dblp_info:
            print(f"  -> NOT FOUND on DBLP")
            result = {
                "key": key,
                "line": line_no,
                "status": "not_found",
                "local_title": title,
            }
            results.append(result)
            completed_keys.add(key)
            checkpoint["completed_keys"] = list(completed_keys)
            checkpoint["results"] = results
            save_checkpoint(checkpoint)
            continue

        similarity = dblp_info.get("_similarity", 0)
        dblp_title = dblp_info.get("title", "").rstrip(".")
        dblp_key = dblp_info.get("_dblp_key", "")
        print(f"  DBLP match: {dblp_title[:80]} (similarity: {similarity:.2%})")

        # 获取 DBLP BibTeX
        dblp_bibtex = None
        if dblp_key:
            dblp_bibtex = get_dblp_bibtex(dblp_key)
            time.sleep(args.delay / 2)

        # 比较
        diffs = compare_entries(entry, dblp_info, dblp_bibtex)

        if diffs:
            print(f"  -> MISMATCH: {len(diffs)} difference(s) found")
            for d in diffs:
                print(f"     - {d['field']}: local='{d['local']}' vs dblp='{d['dblp']}'")
            result = {
                "key": key,
                "line": line_no,
                "status": "mismatch",
                "local_title": title,
                "dblp_title": dblp_title,
                "similarity": similarity,
                "diffs": diffs,
                "dblp_bibtex": dblp_bibtex,
            }
        else:
            print(f"  -> MATCH")
            result = {
                "key": key,
                "line": line_no,
                "status": "match",
                "local_title": title,
                "dblp_title": dblp_title,
                "similarity": similarity,
            }

        results.append(result)
        completed_keys.add(key)

        # 每条都保存断点
        checkpoint["completed_keys"] = list(completed_keys)
        checkpoint["results"] = results
        save_checkpoint(checkpoint)

    # 生成报告
    print("\n" + "=" * 60)
    print("Generating report...")
    generate_report(results, total_entries, args.report)
    print("Done!")


if __name__ == "__main__":
    main()
