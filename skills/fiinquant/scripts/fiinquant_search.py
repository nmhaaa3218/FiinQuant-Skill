#!/usr/bin/env python3
"""
FiinQuant Documentation Search MCP Server

Provides three core tools:
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
from typing import List, Dict

BASE_URL = "https://docs.fiinquant.vn"
HEADERS = {
    "Accept": "text/markdown, application/json",
    "User-Agent": "Mozilla/5.0 (compatible; MCP-Server/1.0)"
}
TIMEOUT = 30


def search_documents(
    query: str,
    limit: int = 10,
    base_page: str = "/gioi-thieu/tong-quan-san-pham.md"
) -> List[Dict[str, str]]:
    """
    Search FiinQuant documentation using the built-in ask endpoint.

    Args:
        query: Natural language search query (e.g., "WebSocket realtime", "Fetch_Trading_Data")
        limit: Maximum number of results to return
        base_page: Base documentation page to query

    Returns:
        List of matching documents with title, path, and snippet
    """
    url = f"{BASE_URL}{base_page}"
    params = {"ask": query}

    response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()

    content = response.text
    return _parse_search_results(content, limit)


def _parse_search_results(content: str, limit: int) -> List[Dict[str, str]]:
    """Parse search results from ask endpoint response."""
    results = []
    lines = content.split("\n")
    in_sources = False

    for line in lines:
        if line.startswith("## Sources:") or line.startswith("# Sources:"):
            in_sources = True
            continue

        if in_sources and line.strip().startswith("- ["):
            match = re.match(r'- \[(.+?)\]\((https://docs\.fiinquant\.vn(.+?))\)', line)
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


def get_document_outline() -> Dict[str, List[str]]:
    """Get the full documentation sitemap organized by category."""
    response = requests.get(f"{BASE_URL}/sitemap.md", headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()

    content = response.text
    return _parse_sitemap(content)


def _parse_sitemap(content: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse sitemap markdown into structured data."""
    sections = {}
    current_section = "General"

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

        match = re.match(r'- \[(.+?)\]\((https://docs\.fiinquant\.vn(.+?))\)', line)
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
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.text


def get_full_corpus() -> str:
    """Retrieve the full documentation corpus as a single text file."""
    response = requests.get(f"{BASE_URL}/llms-full.txt", headers=HEADERS, timeout=60)
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
    print("FiinQuant Search MCP - Running Tests")
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


def respond(message_id, result=None, error=None):
    response = {"jsonrpc": "2.0"}
    if message_id is not None:
        response["id"] = message_id
    if error is not None:
        response["error"] = error
    else:
        response["result"] = result
    sys.__stdout__.write(json.dumps(response, ensure_ascii=False) + "\n")
    sys.__stdout__.flush()


def run_mcp_loop():
    import traceback
    
    # Redirect sys.stdout to sys.stderr so prints don't corrupt JSON-RPC stdout
    sys.stdout = sys.stderr
    stdin = sys.__stdin__
    
    while True:
        line = stdin.readline()
        if not line:
            break
        try:
            request = json.loads(line)
            method = request.get("method")
            msg_id = request.get("id")
            
            if method == "initialize":
                respond(msg_id, {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "fiinquant-search",
                        "version": "1.0.0"
                    }
                })
            elif method == "notifications/initialized":
                pass
            elif method == "tools/list":
                respond(msg_id, {
                    "tools": [
                        {
                            "name": "search_documents",
                            "description": "Search the FiinQuant documentation for specific functions, WebSocket realtime data, trading APIs, or financial reports.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "The search query (e.g., 'realtime data', 'historical data')"},
                                    "limit": {"type": "integer", "description": "Max number of results to return (default: 5)"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_document_outline",
                            "description": "Get the complete outline / sitemap of all available documentation pages.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "read_document_page",
                            "description": "Read the detailed markdown content of a specific page from the documentation outline.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "The documentation page path (e.g., '/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.1.-ham-du-lieu-realtime.md')"}
                                },
                                "required": ["path"]
                            }
                        },
                        {
                            "name": "get_full_corpus",
                            "description": "Retrieve the entire documentation corpus as a single text file. Useful for offline reasoning.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                })
            elif method == "tools/call":
                params = request.get("params", {})
                name = params.get("name")
                arguments = params.get("arguments", {})
                
                if name == "search_documents":
                    query = arguments.get("query")
                    limit = arguments.get("limit", 5)
                    results = search_documents(query, limit=limit)
                    text_content = json.dumps(results, indent=2, ensure_ascii=False)
                    respond(msg_id, {
                        "content": [{"type": "text", "text": text_content}]
                    })
                elif name == "get_document_outline":
                    outline = get_document_outline()
                    text_content = json.dumps(outline, indent=2, ensure_ascii=False)
                    respond(msg_id, {
                        "content": [{"type": "text", "text": text_content}]
                    })
                elif name == "read_document_page":
                    path = arguments.get("path")
                    content = read_document_page(path)
                    respond(msg_id, {
                        "content": [{"type": "text", "text": content}]
                    })
                elif name == "get_full_corpus":
                    corpus = get_full_corpus()
                    respond(msg_id, {
                        "content": [{"type": "text", "text": corpus}]
                    })
                else:
                    respond(msg_id, error={"code": -32601, "message": f"Method not found: {name}"})
            else:
                if msg_id is not None:
                    respond(msg_id, {})
        except Exception as e:
            err_msg = traceback.format_exc()
            sys.stderr.write(f"Error in MCP loop: {err_msg}\n")
            if 'msg_id' in locals() and msg_id is not None:
                respond(msg_id, error={"code": -32603, "message": str(e)})


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--mcp":
            run_mcp_loop()
        else:
            query = " ".join(sys.argv[1:])
            results = search_documents(query)
            print_search_results(results)
    else:
        run_tests()


if __name__ == "__main__":
    main()