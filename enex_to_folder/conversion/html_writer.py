"""ENML 본문을 최종 HTML 문서 파일로 저장합니다."""
import html
import os
import re


class HtmlWriter:
    """en-note 래퍼를 제거하고, 완전한 HTML 문서로 감싸서 파일에 저장합니다."""

    _EN_NOTE_OPEN_PATTERN = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
    _DOCTYPE_PATTERN = re.compile(r"<!DOCTYPE[^>]*>", re.IGNORECASE)
    _EN_NOTE_TAG_PATTERN = re.compile(r"</?en-note[^>]*>", re.IGNORECASE)

    def write(self, title: str, linked_content: str, output_path: str) -> None:
        body = self._DOCTYPE_PATTERN.sub("", linked_content)
        body = self._EN_NOTE_OPEN_PATTERN.sub("", body)
        body = self._EN_NOTE_TAG_PATTERN.sub("", body)

        escaped_title = html.escape(title)
        html_doc = (
            "<!DOCTYPE html>\n"
            '<html lang="ko">\n<head>\n'
            '<meta charset="utf-8">\n'
            f"<title>{escaped_title}</title>\n"
            "</head>\n<body>\n"
            f"<h1>{escaped_title}</h1>\n"
            f"{body}\n"
            "</body>\n</html>\n"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_doc)
