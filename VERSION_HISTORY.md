# 버전 히스토리

## v1.0.2 (2026-09-09)
### 기능
- 다단계 폴더 지원: 선택한 폴더의 모든 하위 폴더에서 .enex 파일 탐색
- 폴더 구조 상관없이 모든 .enex 파일을 일괄 변환

## v1.0.1 (2026-09-09)
### 수정
- 패키지 구조 수정: `enex_to_folder/__init__.py` 추가
- 모듈 import 오류 해결

## v1.0.0 (2026-09-09)
### 기능
- ENEX 파일을 노트별 폴더 구조로 변환
- 이미지 추출 및 상대경로 연결
- 메타데이터(생성일, 수정일, 태그) 보존
- 중복 파일명 자동 처리 (번호 붙임)
- Windows GUI 인터페이스

### 구현 완료
- ✅ ENEX 파일 파싱 (enex_parser.py)
- ✅ HTML 문서 생성 (html_writer.py)
- ✅ 리소스 추출 (resource_extractor.py)
- ✅ 파일명 정제 (filename_sanitizer.py)
- ✅ 메타데이터 저장 (metadata_writer.py)
- ✅ GUI 구현 (main_window.py)
- ✅ 배치 처리 (batch_converter.py)
