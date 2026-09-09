"""Base64로 인코딩된 첨부파일 데이터를 디코딩하여 실제 파일로 저장합니다."""
import base64
import os
from typing import Dict

from enex_to_folder.conversion.filename_sanitizer import FilenameSanitizer
from enex_to_folder.domain.models import Resource


class ResourceExtractor:
    """Resource 객체들을 노트 폴더 안에 실제 파일로 저장합니다."""

    def __init__(self) -> None:
        self._sanitizer = FilenameSanitizer()

    def extract_all(self, resources, note_dir: str) -> Dict[str, str]:
        """모든 첨부파일을 note_dir에 저장하고, {hash_hex: 저장된_상대경로} 매핑을 반환합니다."""
        hash_to_relpath: Dict[str, str] = {}
        used_names: Dict[str, int] = {}

        for index, resource in enumerate(resources, start=1):
            file_name = self._decide_file_name(resource, index, used_names)
            file_path = os.path.join(note_dir, file_name)

            try:
                decoded = base64.b64decode(resource.data_base64)
            except Exception:
                decoded = b""

            with open(file_path, "wb") as f:
                f.write(decoded)

            if resource.hash_hex:
                hash_to_relpath[resource.hash_hex] = file_name

        return hash_to_relpath

    def _decide_file_name(self, resource: Resource, index: int, used_names: Dict[str, int]) -> str:
        if resource.file_name:
            base_name = self._sanitizer.sanitize(resource.file_name)
        else:
            ext = resource.guess_extension()
            base_name = f"attachment_{index}{ext}"

        count = used_names.get(base_name, 0)
        used_names[base_name] = count + 1
        if count == 0:
            return base_name

        name_part, ext_part = os.path.splitext(base_name)
        return f"{name_part}({count}){ext_part}"
