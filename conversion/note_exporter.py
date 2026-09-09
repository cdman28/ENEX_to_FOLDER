"""단일 노트를 폴더로 내보내는 조립(오케스트레이션) 클래스.

각 책임(파일명 정제, 첨부파일 추출, 본문 연결, HTML 저장, 메타데이터 저장)을
독립된 컴포넌트에 위임하고, 이 클래스는 그 순서를 조율만 합니다.
"""
import os

from enex_to_folder.conversion.filename_sanitizer import FilenameSanitizer
from enex_to_folder.conversion.html_writer import HtmlWriter
from enex_to_folder.conversion.media_linker import MediaLinker
from enex_to_folder.conversion.resource_extractor import ResourceExtractor
from enex_to_folder.domain.interfaces import INoteExporter
from enex_to_folder.domain.models import Note
from enex_to_folder.metadata.metadata_writer import MetadataWriter


class NoteExporter(INoteExporter):
    """Note 객체 하나를 '본문.html + 첨부파일 + metadata.json' 폴더로 내보냅니다."""

    def __init__(self) -> None:
        self._resource_extractor = ResourceExtractor()
        self._media_linker = MediaLinker()
        self._html_writer = HtmlWriter()
        self._metadata_writer = MetadataWriter()
        self._folder_sanitizer = FilenameSanitizer()

    def export_note(self, note: Note, output_dir: str) -> None:
        folder_name = self._folder_sanitizer.make_unique(note.title)
        note_dir = os.path.join(output_dir, folder_name)
        os.makedirs(note_dir, exist_ok=True)

        hash_to_relpath = self._resource_extractor.extract_all(note.resources, note_dir)
        linked_content = self._media_linker.link(note.content_enml, hash_to_relpath)

        html_path = os.path.join(note_dir, "본문.html")
        self._html_writer.write(note.title, linked_content, html_path)

        self._metadata_writer.write(note, note_dir)
