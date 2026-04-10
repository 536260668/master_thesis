---
name: verify-citations
description: Verify the accuracy of paper citations using refs.bib and web search.
---

# Verify Citations

This skill helps you systematic verify the accuracy of citations in a LaTeX project. It cross-references the author names, titles, and claims made in the text with the actual source material found via web search.

## Process

1.  **Extract Citation Information**: First, locate the `.bib` file (e.g., `ref/refs.bib`). For a given citation key (e.g., `liu2024benchhealth`), extract the bibliographic information (title, author, year) from the `.bib` file. You can use a Python script like this to parse the `.bib` file:

    ```python
    import re
    import sys

    # Usage: python extract_bib.py <path_to_bib> <citation_key>
    bib_path = sys.argv[1]
    key = sys.argv[2]

    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the bibtex entry
    pattern = r'@.*?\{' + re.escape(key) + r',\s*(.*?)\n\}'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if match:
        print(f"--- Entry for {key} ---")
        print(match.group(1))
    else:
        print(f"Key '{key}' not found in {bib_path}")
    ```

2.  **Find Citation Usage**: Find all instances where this citation key is used in the LaTeX source files (e.g., `\cite{liu2024benchhealth}`). Read the surrounding text to understand the *claim* being attributed to this citation.

3.  **Perform Web Search**: Use the `search_web` tool to search for the title and authors extracted in Step 1.
    *   Example query: `"Paper Title" "First Author"`

4.  **Verify Claims and Authors**:
    *   **Author check**: Does the author name mentioned in the LaTeX text (e.g., "Chen等人") match the actual authors of the paper found online (e.g., "Liu, Fenglin")?
    *   **Content check**: Does the claim made in the LaTeX text accurately reflect the content and findings of the paper? Read the search summaries (which often include the abstract or key findings) to verify this. Look out for "hallucinated" data, misinterpreted conclusions, or incorrect study types (e.g., calling a benchmark paper a "review").

5.  **Report / Fix**: If discrepancies are found, either directly modify the LaTeX files to correct the authors and claims, or report the discrepancies to the user if they require domain expertise to resolve.
