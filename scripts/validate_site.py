from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def parse_top_level_scalars(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in text.splitlines():
        if not line or line[0].isspace() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if not value:
            data[key] = None
        elif value.startswith('"') and value.endswith('"'):
            data[key] = json.loads(value)
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            data[key] = value
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    return parse_top_level_scalars(path.read_text(encoding="utf-8"))


def load_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML front matter in {path}")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Unclosed YAML front matter in {path}")
    return parse_top_level_scalars(parts[1])


def validate() -> None:
    config = load_yaml(ROOT / "_config.yml")
    expected = {
        "title": "LLUVIA's THINGS ABOUT WORLD",
        "url": "https://guoziqiang198.github.io",
        "baseurl": "",
        "github_username": "GuoZiqiang198",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"Unexpected {key!r}: {config.get(key)!r}")

    if (ROOT / "CNAME").exists():
        raise ValueError("CNAME must not exist before a custom domain is configured")

    required_assets = [
        ROOT / str(config["header-img"]),
        ROOT / "css" / "bootstrap.min.css",
        ROOT / "css" / "hux-blog.min.css",
        ROOT / "js" / "jquery.min.js",
        ROOT / "js" / "bootstrap.min.js",
        ROOT / "js" / "hux-blog.min.js",
        ROOT / "js" / "simple-jekyll-search.min.js",
    ]
    missing_assets = [str(path.relative_to(ROOT)) for path in required_assets if not path.is_file()]
    if missing_assets:
        raise ValueError(f"Missing required assets: {missing_assets}")

    posts = sorted((ROOT / "_posts").glob("*.md"))
    if not posts:
        raise ValueError("Expected at least one post")

    for post in posts:
        post_data = load_front_matter(post)
        for required_key in ("layout", "title", "date", "author", "tags"):
            if required_key not in post_data:
                raise ValueError(f"{post.name} is missing {required_key!r}")

    for page_name in ("index.html", "about.html", "archive.html", "404.html"):
        load_front_matter(ROOT / page_name)

    forbidden = (
        "ca-pub-6487568398225121",
        "UA-49627206-1",
        "huxpro@gmail.com",
        "xBT4GhYoi5qRD5tr338pgPM5OWHHIDR6mNg1a3euekI",
    )
    ignored_parts = {".git", ".codex", ".jekyll-cache", "_site", "node_modules", "vendor"}
    text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.resolve() != Path(__file__).resolve()
        and not ignored_parts.intersection(path.parts)
        and path.suffix.lower() in {".html", ".md", ".yml", ".yaml", ".js", ".json", ".py"}
    ]
    for path in text_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        matches = [value for value in forbidden if value in text]
        if matches:
            raise ValueError(f"Forbidden original-owner values in {path}: {matches}")

    print(f"PASS: config keys={len(config)}, posts={len(posts)}, checked text files={len(text_files)}")
    print(f"PASS: header asset={required_assets[0].relative_to(ROOT)}")
    print("PASS: no CNAME or original analytics/advertising identifiers")


if __name__ == "__main__":
    validate()
