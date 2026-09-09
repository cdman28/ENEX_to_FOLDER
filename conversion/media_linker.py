"""ENML 본문 안의 <en-media>, <en-todo> 등 Evernote 전용 태그를
일반 HTML 태그로 치환합니다.
"""
import re
from typing import Dict


class MediaLinker:
    """본문의 en-media 참조를 실제 저장된 첨부파일 경로로 연결합니다."""

    _EN_MEDIA_PATTERN = re.compile(r"<en-media\b([^>]*?)/?>", re.IGNORECASE)
    _EN_TODO_PATTERN = re.compile(r"<en-todo\b([^>]*?)/?>", re.IGNORECASE)
    _ATTR_PATTERN = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')

    def link(self, content_enml: str, hash_to_relpath: Dict[str, str]) -> str:
        """en-media/en-todo 태그를 HTML 태그로 치환한 본문 문자열을 반환합니다."""
        result = self._EN_MEDIA_PATTERN.sub(
            lambda m: self._replace_media(m, hash_to_relpath), content_enml
        )
        result = self._EN_TODO_PATTERN.sub(self._replace_todo, result)
        return result

    def _replace_media(self, match: "re.Match", hash_to_relpath: Dict[str, str]) -> str:
        attrs = dict(self._ATTR_PATTERN.findall(match.group(1)))
        media_hash = attrs.get("hash")
        mime = attrs.get("type", "")
        rel_path = hash_to_relpath.get(media_hash) if media_hash else None

        if rel_path is None:
            # 매칭되는 첨부파일을 못 찾은 경우, 정보를 남기고 넘어감
            return f'<span data-missing-resource="{media_hash or "unknown"}">[첨부파일을 찾을 수 없음]</span>'

        if mime.startswith("image/"):
            return f'<img src="{rel_path}" alt="{rel_path}" style="max-width:100%;">'
        return f'<a href="{rel_path}">{rel_path}</a>'

    @staticmethod
    def _replace_todo(match: "re.Match") -> str:
        checked = "checked" in match.group(1)
        checked_attr = " checked" if checked else ""
        return f'<input type="checkbox" disabled{checked_attr}>'
