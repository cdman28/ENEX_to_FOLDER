# 버전 히스토리

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
