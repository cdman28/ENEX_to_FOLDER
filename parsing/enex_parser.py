"""ENEX(XML) 파일을 파싱하여 Note 객체 목록으로 변환합니다.

단일 책임 원칙(SRP): 이 모듈은 오직 "파싱"만 담당하고,
파일 저장이나 변환은 다른 모듈이 담당합니다.
"""
import base64
import hashlib
import xml.etree.ElementTree as ET
from typing import List, Optional

from enex_to_folder.domain.models import Note, Resource


class EnexParseError(Exception):
    """ENEX 파일 파싱 중 발생하는 오류."""


class EnexParser:
    """.enex 파일 하나를 읽어 Note 객체 리스트로 변환합니다."""

    def parse_file(self, enex_path: str) -> List[Note]:
        """ENEX 파일 경로를 받아 그 안의 모든 노트를 파싱합니다."""
        try:
            tree = ET.parse(enex_path)
        except ET.ParseError as exc:
            raise EnexParseError(f"'{enex_path}' 파일을 XML로 파싱할 수 없습니다: {exc}") from exc

        root = tree.getroot()
        notes: List[Note] = []
        for note_elem in root.findall("note"):
            notes.append(self._parse_note_element(note_elem))
        return notes

    def _parse_note_element(self, note_elem: ET.Element) -> Note:
        title = self._get_text(note_elem, "title") or "제목 없음"
        content = self._get_text(note_elem, "content") or ""
        created = self._get_text(note_elem, "created")
        updated = self._get_text(note_elem, "updated")
        tags = [t.text for t in note_elem.findall("tag") if t.text]

        resources = []
        for res_elem in note_elem.findall("resource"):
            resource = self._parse_resource_element(res_elem)
            if resource is not None:
                resources.append(resource)

        return Note(
            title=title,
            content_enml=content,
            created=created,
            updated=updated,
            tags=tags,
            resources=resources,
        )

    def _parse_resource_element(self, res_elem: ET.Element) -> Optional[Resource]:
        data_elem = res_elem.find("data")
        mime_elem = res_elem.find("mime")
        if data_elem is None or data_elem.text is None or mime_elem is None:
            return None

        # ENEX의 base64 데이터는 줄바꿈이 포함되어 있으므로 제거 후 디코딩
        raw_b64 = "".join(data_elem.text.split())
        try:
            decoded_bytes = base64.b64decode(raw_b64)
        except Exception:
            decoded_bytes = b""

        hash_hex = hashlib.md5(decoded_bytes).hexdigest() if decoded_bytes else None

        file_name = None
        attrs_elem = res_elem.find("resource-attributes")
        if attrs_elem is not None:
            file_name_elem = attrs_elem.find("file-name")
            if file_name_elem is not None and file_name_elem.text:
                file_name = file_name_elem.text

        return Resource(
            mime=mime_elem.text or "application/octet-stream",
            data_base64=raw_b64,
            file_name=file_name,
            hash_hex=hash_hex,
        )

    @staticmethod
    def _get_text(parent: ET.Element, tag: str) -> Optional[str]:
        elem = parent.find(tag)
        if elem is None:
            return None
        return elem.text
