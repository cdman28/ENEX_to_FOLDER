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
        """source_dir 안의 모든 .enex 파일을 파싱해서 output_dir 아래에 저장합니다.
        
        각 ENEX 파일명과 같은 폴더를 만들고, 그 안에 노트별 폴더를 생성합니다 (다단계 폴더 지원).
        """
        os.makedirs(output_dir, exist_ok=True)
        enex_paths = sorted(glob.glob(os.path.join(source_dir, "**/*.enex"), recursive=True))

        if not enex_paths:
            if progress_callback:
                progress_callback(0, 0, "폴더 안에 .enex 파일이 없습니다.")
            return

        total_notes = 0
        processed_notes = 0

        # 먼저 전체 노트 개수 계산
        for enex_path in enex_paths:
            try:
                notes = self._parser.parse_file(enex_path)
                total_notes += len(notes)
            except EnexParseError as exc:
                if progress_callback:
                    progress_callback(0, 0, f"⚠️ 파싱 실패: {os.path.basename(enex_path)} - {exc}")

        # 각 ENEX 파일별로 처리
        for enex_path in enex_paths:
            if should_stop and should_stop():
                if progress_callback:
                    progress_callback(processed_notes, total_notes, "사용자에 의해 중지되었습니다.")
                return

            try:
                notes = self._parser.parse_file(enex_path)
                
                # ENEX 파일명(확장자 제외)으로 폴더 생성
                file_name = os.path.splitext(os.path.basename(enex_path))[0]
                file_output_dir = os.path.join(output_dir, file_name)
                os.makedirs(file_output_dir, exist_ok=True)

                # 해당 파일의 노트들을 파일명 폴더 안에 저장
                for note in notes:
                    if should_stop and should_stop():
                        if progress_callback:
                            progress_callback(processed_notes, total_notes, "사용자에 의해 중지되었습니다.")
                        return

                    try:
                        self._exporter.export_note(note, file_output_dir)
                        processed_notes += 1
                        if progress_callback:
                            progress_callback(processed_notes, total_notes, f"완료: {note.title} ({file_name})")
                    except Exception as exc:
                        processed_notes += 1
                        if progress_callback:
                            progress_callback(processed_notes, total_notes, f"⚠️ 실패: {note.title} - {exc}")

            except EnexParseError as exc:
                if progress_callback:
                    progress_callback(processed_notes, total_notes, f"⚠️ 파싱 실패: {os.path.basename(enex_path)} - {exc}")

        if progress_callback:
            progress_callback(total_notes, total_notes, f"전체 완료: 노트 {total_notes}개 변환됨")
