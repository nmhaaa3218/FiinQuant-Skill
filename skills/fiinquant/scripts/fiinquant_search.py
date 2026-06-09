#!/usr/bin/env python3
"""
FiinQuant Documentation Search CLI Helper

Provides core tools:
- search_documents: Search docs using the built-in ask endpoint
- get_document_outline: Get the full documentation sitemap
- read_document_page: Extract clean markdown text from a specific page

Usage:
    python fiinquant_search.py "WebSocket realtime"
"""

import requests
import re
import json
import sys
import time
from typing import List, Dict

BASE_URL = "https://docs.fiinquant.vn"
HEADERS = {
    "Accept": "text/markdown, application/json",
    "User-Agent": "Mozilla/5.0 (compatible; FiinQuant-Docs-Search/1.0)"
}
TIMEOUT = 30


def robust_get(url: str, params: dict = None, headers: dict = None, timeout: int = 30) -> requests.Response:
    """Make an HTTP GET request with simple retry logic and backoff using time.sleep."""
    last_err = None
    for attempt in range(3):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            # Retry on transient server errors (500, 502, 503, 504)
            if response.status_code in [500, 502, 503, 504]:
                raise requests.RequestException(f"Server error {response.status_code}")
            return response
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(1 + attempt)  # Backoff: 1s, 2s
    raise last_err


def search_documents(
    query: str,
    limit: int = 10,
    base_page: str = "/gioi-thieu/tong-quan-san-pham.md"
) -> List[Dict[str, str]]:
    """
    Search FiinQuant documentation using the built-in ask endpoint.
    Falls back to a local title-keyword search on the sitemap if the endpoint fails or returns no results.

    Args:
        query: Natural language search query (e.g., "WebSocket realtime", "Fetch_Trading_Data")
        limit: Maximum number of results to return
        base_page: Base documentation page to query

    Returns:
        List of matching documents with title, path, and snippet
    """
    url = f"{BASE_URL}{base_page}"
    params = {"ask": query}
    results = []

    try:
        response = robust_get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        results = _parse_search_results(response.text, limit)
    except Exception as e:
        print(f"Warning: Remote search failed ({e}). Trying local fallback search...", file=sys.stderr)

    if not results:
        results = fallback_local_search(query, limit)

    return results


def fallback_local_search(query: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Perform a robust local keyword search over the sitemap
    when the remote search fails or returns nothing.
    """
    results = []
    try:
        outline = get_document_outline()
        query_words = [w.lower().strip() for w in query.split() if w.strip()]
        if not query_words:
            return results

        for section, pages in outline.items():
            for page in pages:
                title = page["title"].lower()
                path = page["path"].lower()
                # Matches if all words in search query are found in title or path
                if all(word in title or word in path for word in query_words):
                    if page["path"] not in [r["path"] for r in results]:
                        results.append({
                            "title": page["title"],
                            "path": page["path"],
                            "url": page["url"],
                            "snippet": f"Section: {section}"
                        })
                        if len(results) >= limit:
                            return results
    except Exception as e:
        print(f"Warning: Fallback local search failed ({e})", file=sys.stderr)
    return results


def _parse_search_results(content: str, limit: int) -> List[Dict[str, str]]:
    """Parse search results from ask endpoint response using a robust regex."""
    results = []
    lines = content.split("\n")
    in_sources = False

    # Regex matching: - [Title](https://docs.fiinquant.vn/path) or - [Title](/path) or - [Title](../path)
    link_pattern = re.compile(r'-\s+\[([^\]]+)\]\(((?:https?://[a-zA-Z0-9.-]+)?(/[^)]+))\)')

    for line in lines:
        if line.startswith("## Sources:") or line.startswith("# Sources:"):
            in_sources = True
            continue

        if in_sources and line.strip().startswith("- ["):
            match = link_pattern.search(line)
            if match:
                title = match.group(1)
                path = match.group(3)
                if path not in [r["path"] for r in results]:
                    result = {
                        "title": title,
                        "path": path,
                        "url": f"{BASE_URL}{path}",
                        "snippet": ""
                    }
                    results.append(result)
                    if len(results) >= limit:
                        break

    return results


def get_document_outline() -> Dict[str, List[Dict[str, str]]]:
    """Get the full documentation sitemap organized by category."""
    response = robust_get(f"{BASE_URL}/sitemap.md", headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()

    content = response.text
    return _parse_sitemap(content)


def _parse_sitemap(content: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse sitemap markdown into structured data using a robust regex."""
    sections = {}
    current_section = "General"

    # Regex matching sitemap links (accepts both absolute and relative)
    link_pattern = re.compile(r'-\s+\[([^\]]+)\]\(((?:https?://[a-zA-Z0-9.-]+)?(/[^)]+))\)')

    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("# "):
            continue

        if line.startswith("## "):
            current_section = line.replace("## ", "").strip()
            if current_section not in sections:
                sections[current_section] = []
            continue

        match = link_pattern.search(line)
        if match:
            title = match.group(1)
            path = match.group(3)
            sections[current_section].append({
                "title": title,
                "path": path,
                "url": f"{BASE_URL}{path}"
            })

    return sections


def read_document_page(path: str) -> str:
    """
    Read a specific documentation page.

    Args:
        path: Documentation path (e.g., "/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.1.-ham-du-lieu-realtime.md")

    Returns:
        Page content in markdown format
    """
    url = f"{BASE_URL}{path}"
    response = robust_get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.text


def get_full_corpus() -> str:
    """Retrieve the full documentation corpus as a single text file."""
    response = robust_get(f"{BASE_URL}/llms-full.txt", headers=HEADERS, timeout=60)
    response.raise_for_status()
    return response.text


def print_search_results(results: List[Dict[str, str]]) -> None:
    """Pretty print search results."""
    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} result(s):\n")
    print("-" * 80)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   Path: {r['path']}")
        print(f"   URL:  {r['url']}")
        print()
    print("-" * 80)


def print_outline(sections: Dict[str, List[Dict[str, str]]]) -> None:
    """Pretty print documentation outline."""
    print("\nFiinQuant Documentation Outline\n")
    print("=" * 80)
    for section_name, pages in sections.items():
        print(f"\n{section_name}")
        print("-" * 40)
        for page in pages[:10]:
            print(f"  - {page['title']}")
        if len(pages) > 10:
            print(f"  ... and {len(pages) - 10} more pages")
    print("\n" + "=" * 80)


def test_search(query: str) -> List[Dict[str, str]]:
    """Test search functionality."""
    print(f"\n[TEST] Searching for: '{query}'")
    results = search_documents(query, limit=5)
    print_search_results(results)
    return results


def test_outline() -> Dict[str, List[Dict[str, str]]]:
    """Test outline functionality."""
    print("\n[TEST] Fetching documentation outline...")
    outline = get_document_outline()
    print_outline(outline)
    return outline


def test_read_page() -> str:
    """Test reading a specific page."""
    print("\n[TEST] Reading specific page...")
    path = "/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.1.-ham-du-lieu-realtime.md"
    content = read_document_page(path)
    print(f"Page length: {len(content)} characters")
    print("\nFirst 500 characters:")
    print("-" * 40)
    print(content[:500])
    print("-" * 40)
    return content


def run_tests() -> bool:
    """Run all tests and return True if all pass."""
    print("=" * 80)
    print("FiinQuant Search - Running Tests")
    print("=" * 80)

    tests = [
        ("Search: WebSocket realtime", lambda: test_search("WebSocket realtime")),
        ("Search: Fetch_Trading_Data", lambda: test_search("Fetch_Trading_Data")),
        ("Search: Bao cao tai chinh", lambda: test_search("Báo cáo tài chính")),
        ("Outline", lambda: test_outline()),
        ("Read Page", lambda: test_read_page()),
    ]

    all_passed = True
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"[PASS] {name}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED!")
    print("=" * 80)

    return all_passed


def main():
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        if arg1 == "--read" and len(sys.argv) > 2:
            path = sys.argv[2]
            try:
                content = read_document_page(path)
                print(content)
            except Exception as e:
                print(f"Error reading page: {e}", file=sys.stderr)
                sys.exit(1)
        elif arg1 == "--outline":
            try:
                outline = get_document_outline()
                print(json.dumps(outline, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error getting outline: {e}", file=sys.stderr)
                sys.exit(1)
        elif arg1 == "--corpus":
            try:
                corpus = get_full_corpus()
                print(corpus)
            except Exception as e:
                print(f"Error getting corpus: {e}", file=sys.stderr)
                sys.exit(1)
        elif arg1 in ("--help", "-h"):
            print("FiinQuant Documentation Search CLI Helper")
            print("\nUsage:")
            print("  python3 fiinquant_search.py <search query>       Search the documentation")
            print("  python3 fiinquant_search.py --read <page_path>   Read a specific documentation page")
            print("  python3 fiinquant_search.py --outline            Get sitemap/documentation outline")
            print("  python3 fiinquant_search.py --corpus             Get the entire documentation corpus")
        else:
            query = " ".join(sys.argv[1:])
            results = search_documents(query)
            print_search_results(results)
    else:
        success = run_tests()
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()