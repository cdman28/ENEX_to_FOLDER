"""여러 ENEX 파일을 일괄 변환하고 진행률을 보고합니다."""
import glob
import os
from typing import Optional

from enex_to_folder.conversion.note_exporter import NoteExporter
from enex_to_folder.domain.interfaces import ProgressCallback
from enex_to_folder.parsing.enex_parser import EnexParseError, EnexParser


class BatchConverter:
    """소스 폴더 안의 모든 .enex 파일을 찾아 output_dir로 일괄 변환합니다."""

    def __init__(self) -> None:
        self._parser = EnexParser()
        self._exporter = NoteExporter()

    def convert_folder(
        self,
        source_dir: str,
        output_dir: str,
        progress_callback: Optional[ProgressCallback] = None,
        should_stop: Optional[callable] = None,
    ) -> None:
        """source_dir 안의 모든 .enex 파일을 파싱해서 output_dir 아래에 노트별 폴더로 저장합니다."""
        os.makedirs(output_dir, exist_ok=True)
        enex_paths = sorted(glob.glob(os.path.join(source_dir, "*.enex")))

        if not enex_paths:
            if progress_callback:
                progress_callback(0, 0, "폴더 안에 .enex 파일이 없습니다.")
            return

        all_notes = []
        for enex_path in enex_paths:
            try:
                notes = self._parser.parse_file(enex_path)
                all_notes.extend(notes)
            except EnexParseError as exc:
                if progress_callback:
                    progress_callback(0, 0, f"⚠️ 파싱 실패: {os.path.basename(enex_path)} - {exc}")

        total = len(all_notes)
        for index, note in enumerate(all_notes, start=1):
            if should_stop and should_stop():
                if progress_callback:
                    progress_callback(index - 1, total, "사용자에 의해 중지되었습니다.")
                return

            try:
                self._exporter.export_note(note, output_dir)
                if progress_callback:
                    progress_callback(index, total, f"완료: {note.title}")
            except Exception as exc:
                if progress_callback:
                    progress_callback(index, total, f"⚠️ 실패: {note.title} - {exc}")

        if progress_callback:
            progress_callback(total, total, f"전체 완료: 노트 {total}개 변환됨")
