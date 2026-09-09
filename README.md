# ENEX to Folder 변환기 v1.0.1

Evernote-backup 등으로 만든 `.enex` 파일을 노트별 폴더 구조로 변환하는 Windows GUI 도구입니다.

## 결과물 구조

```
출력폴더/
├── 노트제목1/
│   ├── 본문.html        # 이미지가 상대경로로 연결된 완전한 HTML 문서
│   ├── metadata.json    # 생성일/수정일/태그 보존
│   └── 첨부파일들...
├── 노트제목1(1)/         # 제목이 중복되면 자동으로 번호가 붙습니다
│   └── ...
```

## 실행 방법 (개발 환경)

1. Python 3.10 이상 설치 (tkinter는 표준 라이브러리 포함, 별도 설치 불필요)
2. `python main.py` 실행
3. GUI에서 "ENEX 파일 폴더"에 `.enex` 파일들이 들어있는 폴더를 선택
4. "출력 폴더"에 결과를 저장할 폴더를 선택
5. "변환 시작" 클릭

## exe로 빌드하기 (배포용)

```
pip install pyinstaller
pyinstaller enex_to_folder.spec
```

빌드가 끝나면 `dist/ENEX_to_Folder_v1.0.0.exe` 파일이 생성됩니다.

## 아키텍처

Clean Architecture + SOLID 원칙에 따라 계층을 분리했습니다.

- `domain/` — 외부 의존성 없는 순수 데이터 모델과 인터페이스
- `parsing/` — ENEX(XML) 파싱 전담
- `conversion/` — 파일명 정제, 첨부파일 추출, 본문-첨부파일 연결, HTML 저장
- `metadata/` — 메타데이터(생성일/수정일/태그) 보존
- `orchestration/` — 여러 ENEX 파일 일괄 처리 및 진행률 보고
- `gui/` — tkinter 기반 사용자 인터페이스 (백엔드 로직에만 의존, 반대 방향 의존 없음)

## 알려진 제한사항

- Evernote 전용 태그 중 `<en-media>`(첨부파일 참조)와 `<en-todo>`(체크박스)만 변환합니다.
  `<en-crypt>`(암호화된 콘텐츠)는 현재 지원하지 않습니다.
- 이미지가 아닌 첨부파일(PDF 등)은 본문에 링크(`<a>`)로만 연결되고 미리보기는 제공하지 않습니다.

## 버전 히스토리

- v1.0.0 (2026-09-09): 최초 구현 - ENEX 파싱, HTML 변환, 첨부파일 추출, 본문-첨부파일 연결,
  메타데이터 보존, 파일명 중복 처리, tkinter GUI, 일괄 처리 진행률 표시
