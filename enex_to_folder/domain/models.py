"""도메인 모델: ENEX 노트와 첨부파일을 표현하는 순수 데이터 클래스.

외부 라이브러리에 의존하지 않는 도메인 계층입니다 (Clean Architecture).
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Resource:
    """ENEX 노트에 포함된 첨부파일 하나를 표현합니다."""

    mime: str
    data_base64: str
    file_name: Optional[str] = None
    hash_hex: Optional[str] = None  # 본문 <en-media hash="..."> 매칭용 MD5 해시

    def guess_extension(self) -> str:
        """MIME 타입으로부터 적절한 파일 확장자를 추정합니다."""
        mime_to_ext = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/svg+xml": ".svg",
            "application/pdf": ".pdf",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.ms-excel": ".xls",
            "application/zip": ".zip",
            "audio/mpeg": ".mp3",
            "video/mp4": ".mp4",
            "text/plain": ".txt",
        }
        return mime_to_ext.get(self.mime, "")


@dataclass
class Note:
    """ENEX 파일 안의 노트 하나를 표현합니다."""

    title: str
    content_enml: str
    created: Optional[str] = None
    updated: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
