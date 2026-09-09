"""노트의 생성일/수정일/태그 등 메타데이터를 보존합니다."""
import json
import os

from enex_to_folder.domain.models import Note


class MetadataWriter:
    """Note 객체의 메타데이터를 metadata.json으로 저장합니다."""

    def write(self, note: Note, note_dir: str) -> None:
        metadata = {
            "title": note.title,
            "created": note.created,
            "updated": note.updated,
            "tags": note.tags,
        }
        output_path = os.path.join(note_dir, "metadata.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
