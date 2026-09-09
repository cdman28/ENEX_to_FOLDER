"""파일/폴더 이름을 파일 시스템에 안전하게 만들고, 중복 시 번호를 붙입니다.

단일 책임 원칙(SRP): 이름 정제와 중복 처리만 담당합니다.
"""
import re
from typing import Dict


class FilenameSanitizer:
    """윈도우 파일 시스템에서 금지된 문자를 치환하고, 중복 이름에 번호를 붙입니다."""

    _INVALID_CHARS_PATTERN = re.compile(r'[\\/:*?"<>|]')
    _MAX_NAME_LENGTH = 100

    def __init__(self) -> None:
        # 이미 사용된 이름의 개수를 세어 중복 시 번호를 붙이는 데 사용
        self._used_name_counts: Dict[str, int] = {}

    def sanitize(self, raw_name: str) -> str:
        """금지 문자를 밑줄로 치환하고 길이를 제한한 '기본' 이름을 반환합니다.
        (중복 번호는 make_unique에서 별도로 붙입니다.)
        """
        name = raw_name.strip() if raw_name else "제목 없음"
        name = self._INVALID_CHARS_PATTERN.sub("_", name)
        name = name.rstrip(". ")  # 윈도우는 이름 끝의 점/공백을 허용하지 않음
        if not name:
            name = "제목 없음"
        if len(name) > self._MAX_NAME_LENGTH:
            name = name[: self._MAX_NAME_LENGTH]
        return name

    def make_unique(self, raw_name: str) -> str:
        """정제된 이름에 대해, 이전에 동일한 이름이 있었다면 뒤에 (n)을 붙여 고유하게 만듭니다."""
        base_name = self.sanitize(raw_name)
        count = self._used_name_counts.get(base_name, 0)
        self._used_name_counts[base_name] = count + 1

        if count == 0:
            return base_name
        return f"{base_name}({count})"
