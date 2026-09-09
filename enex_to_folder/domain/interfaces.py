"""도메인 인터페이스 정의 (인터페이스 분리 원칙, 의존관계 역전 원칙 적용).

이 모듈에 정의된 추상 클래스에 각 구현체가 의존하도록 하여,
GUI 계층이 구체적인 구현이 아닌 추상화에 의존하게 합니다.
"""
from abc import ABC, abstractmethod
from typing import Callable, List

from enex_to_folder.domain.models import Note


class INoteExporter(ABC):
    """노트 하나를 폴더로 내보내는 책임을 정의하는 인터페이스."""

    @abstractmethod
    def export_note(self, note: Note, output_dir: str) -> None:
        """단일 노트를 output_dir 폴더에 내보냅니다."""
        raise NotImplementedError


class IProgressReporter(ABC):
    """일괄 처리 진행 상황을 보고하는 책임을 정의하는 인터페이스."""

    @abstractmethod
    def report(self, current: int, total: int, message: str) -> None:
        """현재 진행 상황을 보고합니다."""
        raise NotImplementedError


# 콜백 함수 형태의 진행률 보고자도 허용하기 위한 타입 별칭
ProgressCallback = Callable[[int, int, str], None]
