#!/usr/bin/env python3

import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


class ArticleParser(HTMLParser):
    BLOCK_TAGS = {"h1", "h2", "h3", "h4", "p", "li", "pre", "blockquote"}
    SKIP_TAGS = {"script", "style", "noscript", "nav", "form", "button", "svg", "img"}
    VOID_TAGS = {"img", "br", "meta", "link", "input", "hr", "source"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.skip_depth = 0
        self.current_block: str | None = None
        self.buffer: list[str] = []
        self.blocks: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "article" and not self.in_article:
            self.in_article = True
            return
        if not self.in_article:
            return
        if self.skip_depth:
            if tag in self.SKIP_TAGS and tag not in self.VOID_TAGS:
                self.skip_depth += 1
            return
        if tag in self.SKIP_TAGS:
            if tag not in self.VOID_TAGS:
                self.skip_depth = 1
            return
        if tag == "br" and self.current_block == "pre":
            self.buffer.append("\n")
        elif tag in self.BLOCK_TAGS:
            if self.current_block is not None:
                self._flush()
            self.current_block = tag
            self.buffer = []

    def handle_endtag(self, tag: str) -> None:
        if not self.in_article:
            return
        if self.skip_depth:
            if tag in self.SKIP_TAGS:
                self.skip_depth -= 1
            return
        if tag == "article":
            if self.current_block is not None:
                self._flush()
            self.in_article = False
        elif self.current_block == tag:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self.in_article and not self.skip_depth and self.current_block is not None:
            self.buffer.append(data)

    def _flush(self) -> None:
        content = re.sub(r"\s+", " ", "".join(self.buffer)).strip()
        if self.current_block == "pre":
            content = "".join(self.buffer).strip()
        if content:
            self.blocks.append((self.current_block or "p", content))
        self.current_block = None
        self.buffer = []


def clean_citation_labels(text: str) -> str:
    text = re.sub(
        r"\s+(?:LlamaIndex(?:\+\d+)?|LlamaIndex\+\d+LlamaIndex\+\d+|PyPI|GitHub(?:\+\d+)?|Medium\+\d+|LlamaParse)(?=\s|$)",
        "",
        text,
    )
    return text.strip()


def extract_title(html: str) -> str:
    match = re.search(r"<title>(.*?)\|\s*by\s+.*?</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return "Artigo convertido"
    return unescape(re.sub(r"\s+", " ", match.group(1))).strip()


def to_markdown(html: str, source_url: str) -> str:
    parser = ArticleParser()
    parser.feed(html)
    title = extract_title(html)
    lines = [
        f"# {title}",
        "",
        "> Conteúdo convertido a partir do HTML local fornecido pelo usuário.",
        ">",
        f"> Fonte: {source_url}",
        "",
    ]
    for tag, raw_content in parser.blocks:
        content = clean_citation_labels(raw_content)
        if not content:
            continue
        if (
            content.startswith("Get Hugo Habbema")
            or content.startswith("Join Medium")
            or content.startswith("Remember me")
        ):
            continue
        if tag == "h1":
            continue
        elif tag == "h2":
            lines.append(f"## {content}")
        elif tag == "h3":
            lines.append(f"### {content}")
        elif tag == "h4":
            lines.append(f"#### {content}")
        elif tag == "li":
            lines.append(f"- {content}")
        elif tag == "blockquote":
            lines.append(f"> {content}")
        elif tag == "pre":
            lines.extend(["```python", content, "```"])
        else:
            lines.append(content)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    if len(sys.argv) not in {3, 4}:
        raise SystemExit("Usage: convert_article_html.py INPUT.html OUTPUT.md [SOURCE_URL]")
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    if destination.exists():
        print(f"Skipped existing file: {destination}")
        return
    source_url = sys.argv[3] if len(sys.argv) == 4 else ""
    markdown = to_markdown(source.read_text(encoding="utf-8", errors="replace"), source_url)
    destination.write_text(markdown, encoding="utf-8")
    print(f"Converted {source.name} to {destination}")


if __name__ == "__main__":
    main()
